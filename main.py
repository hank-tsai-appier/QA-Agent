# Standard library related
import os
import dotenv
import asyncio
import uuid
import json
from pathlib import Path
import re
# Typing related
from typing import Annotated, Sequence, TypedDict, List
from pydantic import BaseModel, Field

# Utils
from src.utils.json_fommatter import JsonFormatter
from src.utils.prompt_loader import load_prompts

# Custom tools
from src.tools.files import update_file

# Langchain related
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_google_genai import ChatGoogleGenerativeAI

# MCP related
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Langgraph related
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages


dotenv.load_dotenv()

# using chrome-devtools-mcp
# has better execution speed, but hard to gen code for the last part
# SERVER_PARAM = StdioServerParameters(
#     command="npx",
#     args=["-y", "chrome-devtools-mcp@latest", "--isolated"]
# )

# using playwright-mcp
# --isolated for brand new browser instance every time
SERVER_PARAM = StdioServerParameters(
    command="npx",
    args=["@playwright/mcp@latest", "--isolated"]
)

# 'js-playwright', 'python-playwright' or 'cypress'
GOAL_LANGUAGE = "python-playwright"
FEATURE_NAME = "sync_to_salesforce"

GOAL = f"""
1. 用track/ce api打資料到nxl6ldktnc, 以下是api的指令，請幫我使用GET方法打資料https://www.woopra.com/track/ce?project=aiquasdk.prd.com&event=update/insert_any_object&cv_user_id=u0091&cv_name=hank&cv_phone=U53297d8d527739ce4e80cbe200a55478&cv_email=hank@email.abc.com
2. 用logger.info設定印出回傳的status code
3. 打開https://airis.appier.com進行登入，帳號是qa.test@appier.com，密碼是aaAA1234
4. go_to_url: https://airis.appier.com/project/aiquasdk.prd.com/profiles/nxl6ldktnc
5. 點擊畫面右側的more button
6. 點擊Sync
7. 在filter輸入Salesforce
8. 點擊sync to Salesforce
9. 點擊Object type的下拉選單並在Filter輸入Contact
10. 點擊Contact並Wait_for_networkidle
11. 接下來點擊Add Salesforce Field

請幫我使用playwright-map執行以上內容，並在執行後幫我寫一個{GOAL_LANGUAGE} code，用於執行這個test plan的automation
"""

SAVE_FILE_PATH = f"results/{FEATURE_NAME}.{'py' if GOAL_LANGUAGE == 'python-playwright' else 'js'}"
os.makedirs(os.path.dirname(SAVE_FILE_PATH), exist_ok=True)

class Todo(BaseModel):
    """
    Todo model for the todos list
    """
    id: int = Field(description="The id of the todo")
    type: str = Field(description="api or ui")
    description: str = Field(description="The description of the todo")
    status: str = Field(description="pending or done")


class AgentState(TypedDict):
    """
    AgentState defines the mutable state shared across the agent's workflow.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    todo_list: List[Todo]

class AutomationAgent:
    def __init__(self, planning_model: ChatGoogleGenerativeAI, web_model: ChatGoogleGenerativeAI):
        self.task_id = uuid.uuid4()
        self.planning_model = planning_model
        self.web_model = web_model

        # create todo directory
        self.todo_dir = Path("todo")
        self.todo_dir.mkdir(exist_ok=True)
        self.todo_file = self.todo_dir / f"todo_{self.task_id}.md"
        
        # load prompts
        self.prompt_loader = load_prompts()


    async def plan_agent(self, state: AgentState):
        """
        1. Plan the todos list based on the goal
        2. Save the todos list to a todo_(task_id).md file
        3. Save the todos list to the state
        """
        
        # Load prompt from YAML
        goal = state['messages'][0].content
        planning_prompt = self.prompt_loader.format_prompt("plan_agent", goal=goal)
        
        # Call LLM
        response = await self.planning_model.ainvoke([HumanMessage(content=planning_prompt)])

        # Parse JSON
        try:
            # Use JsonFormatter to remove markdown markers
            print(f"response: {response}")
            content = JsonFormatter.remove_markdown_markers(response.content[0]["text"])
            
            # Parse JSON
            todo_data = json.loads(content)
            todos = [Todo(**todo) for todo in todo_data.get("todos", [])]
            
            # Save to file
            with open(self.todo_file, "w", encoding="utf-8") as f:
                for todo in todos:
                    f.write(f"[{todo.status}] [{todo.id}] ({todo.type}) {todo.description}\n")

            print(f"✅ Created {len(todos)} todos and saved to {self.todo_file}")
            
            # Update state
            state['todo_list'] = todos
            
        except Exception as e:
            print(f"❌ Failed to parse todos: {e}")
            state['todo_list'] = []
        
        return state

    async def web_agent(self, state: AgentState):
        # Load prompt from YAML
        system_prompt_text = self.prompt_loader.format_prompt(
            "web_agent", 
            todo_file=str(self.todo_file)
        )
        system_prompt = SystemMessage(content=system_prompt_text)

        # 確保有最後的human message
        human_msgs = [m for m in state['messages'] if isinstance(m, HumanMessage)]
        recent_msgs = [m for m in state['messages'] if not isinstance(m, HumanMessage)][-9:]

        # Get todo list
        with open(self.todo_file, "r", encoding="utf-8") as f:
            todo_file_content = f.read()

        # Add todo list to the recent messages
        recent_messages = [human_msgs[-1], HumanMessage(content=todo_file_content)] + recent_msgs

        # Invoke the model
        response = await self.web_model.ainvoke([system_prompt] + recent_messages)
        return {"messages": [response]}

    def should_continue(self, state: AgentState):
        messages = state['messages']
        last_message = messages[-1]

        if not last_message.tool_calls:
            return "end"
        else:
            return "continue"

class CodingAgent:
    def __init__(self, coding_model: ChatGoogleGenerativeAI):
        self.coding_model = coding_model
        self.prompt_loader = load_prompts()

    async def coding_agent(self, state: AgentState):
        response = await self.coding_model.ainvoke(state['messages'])
        print(f"response: {response}")

        return {"messages": [response]}

    def get_template_name(self, goal_language: str):
        if goal_language == "js-playwright":
            return "js_playwright_template"
        elif goal_language == "python-playwright":
            return "python_playwright_template"
        elif goal_language == "cypress":
            return "cypress_template"
        else:
            raise ValueError(f"Invalid goal language: {goal_language}")

    def get_template(self, goal_language: str):
        template_name = self.get_template_name(goal_language)

        # Load prompt from coding_agent.yaml
        prompt_data = self.prompt_loader.load_prompt("coding_agent")
        return prompt_data.get(template_name, "")

    def should_continue(self, state: AgentState):
        messages = state['messages']
        last_message = messages[-1]

        if not last_message.tool_calls:
            return "end"
        else:
            return "continue"

async def main():
    async with stdio_client(SERVER_PARAM) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Load MCP tools
            mcp_tools = await load_mcp_tools(session)

            # remove $schema and additionalProperties from args_schema
            # because the bind_tools function not support these keys
            for tool in mcp_tools:
                if hasattr(tool, "args_schema") and isinstance(tool.args_schema, dict):
                    tool.args_schema.pop("$schema", None)
                    tool.args_schema.pop("additionalProperties", None)

            # Add custom tools
            custom_tools = [update_file]
            
            # Combine all tools
            tools = mcp_tools + custom_tools

            planning_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY")).bind_tools(tools)
            web_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY")).bind_tools(tools)
            coding_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY")).bind_tools(custom_tools)
            
            agent = AutomationAgent(planning_model=planning_model, web_model=web_model)

            # add node
            graph = StateGraph(AgentState)
            graph.add_node("plan_agent", agent.plan_agent)
            graph.add_node("web_agent", agent.web_agent)

            # tool nodes
            tool_node = ToolNode(tools=tools)
            graph.add_node("tools", tool_node)

            # set the entry point
            graph.set_entry_point("plan_agent")

            # conditional edges
            graph.add_conditional_edges("web_agent", agent.should_continue, {"continue": "tools", "end": END})

            # add edges
            graph.add_edge("plan_agent", "web_agent")
            graph.add_edge("tools", "web_agent")

            app = graph.compile()

            input = {"messages": [HumanMessage(content=GOAL)]}


            conversation = []
            async for chunk in app.astream(input, stream_mode="updates", config={"recursion_limit": 100}):
                print("\n==================== Conversation ====================")
                print(chunk)
                conversation.append(chunk)


            # ----------------- Parse the result from the conversation -----------------
            # Get Playwright code from conversation
            playwright_code = []

            for item in conversation:
                content = item[list(item.keys())[0]]['messages'][0].content
                # Extract JavaScript code from content in ```js ... ```
                if isinstance(content, str):
                    js_code_blocks = re.findall(r"```js\s*([\s\S]*?)```", content)
                    
                    # check if the js_code_blocks is not empty
                    if js_code_blocks:
                        playwright_code.append(js_code_blocks[0])

            # ----------------- code generation part -----------------
            # Initialize coding agent
            coding_agent = CodingAgent(coding_model=coding_model)

            # Load prompt from coding_agent.yaml
            coding_prompt = coding_agent.get_template(GOAL_LANGUAGE)
            
            # Generate coding code using the loaded prompt
            coding_system_prompt = SystemMessage(content=coding_prompt)

            # add node
            coding_graph = StateGraph(AgentState)
            coding_graph.add_node("coding_agent", coding_agent.coding_agent)

            # add tool node
            coding_tool_node = ToolNode(tools=custom_tools)
            coding_graph.add_node("coding_tools", coding_tool_node)

            # set the entry point
            coding_graph.set_entry_point("coding_agent")

            # add conditional edges
            coding_graph.add_conditional_edges("coding_agent", coding_agent.should_continue, {"continue": "coding_tools", "end": END})

            # add edges
            coding_graph.add_edge("coding_tools", "coding_agent")


            coding_app = coding_graph.compile()

            # Prepare the initial state with messages
            coding_result = await coding_app.ainvoke({
                "messages": [
                    coding_system_prompt,
                    HumanMessage(content=f"Input code fragments:\n{playwright_code}"),
                    HumanMessage(content=f"Original goal:\n{GOAL}"),
                    HumanMessage(content=f"Save the code to {SAVE_FILE_PATH}"),
                ]
            })

            # Get the last message from the result
            final_message = coding_result['messages'][-1]
            print(f"\n==================== Final Coding Result ====================")
            print(final_message.content)



if __name__ == "__main__":
    asyncio.run(main())