# Standard library related
import os
import dotenv
import asyncio
import uuid
import json
from pathlib import Path

# Typing related
from typing import Annotated, Sequence, TypedDict, List
from pydantic import BaseModel, Field

# Utils
from src.utils.json_fommatter import JsonFormatter

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
SERVER_PARAM = StdioServerParameters(
    command="npx",
    args=["-y", "chrome-devtools-mcp@latest", "--isolated"]
)

# using playwright-mcp
# SERVER_PARAM = StdioServerParameters(
#     command="npx",
#     args=["@playwright/mcp@latest"]
# )

goal = """
1. 用track/ce api打資料到nxl6ldktnc, 以下是api的指令，請幫我使用GET方法打資料https://www.woopra.com/track/ce?project=aiquasdk.prd.com&event=update/insert_any_object&cv_user_id=u0091&cv_name=hank&cv_phone=U53297d8d527739ce4e80cbe200a55478&cv_email=hank@email.abc.com
2. 用logger.info設定印出回傳的status code
3. 打開https://airis.appier.com進行登入，帳號是qa.test@appier.com，密碼是aaAA1234
4. go_to_url: https://airis.appier.com/project/aiquasdk.prd.com/profiles/nxl6ldktnc
5. 點擊畫面右側的有三個點的button，會跳出一個下拉選單
6. 點擊Sync
7. 在filter輸入Salesforce
8. 點擊sync to Salesforce
9. 點擊Object type的下拉選單並在Filter輸入Contact
10. 點擊Contact並Wait_for_networkidle
11. 接下來點擊Add Salesforce Field三次，會有三個Map Field需要填寫
12. 點選Salesforce的下拉選單，在Filter中輸入Last Name，點擊選單中的Last Name
13. 接下來點擊AIRIS field右側的**(X)**，點擊後會出現下拉選單，點擊Name，請注意不是delete button
14. 點選Salesfoce的下拉選單，在Filter中輸入Mobile Phone，點擊選單中的Mobile Phone
15. 接下來點擊AIRIS field右側的**(X)**，點擊後會出現下拉選單，點擊phone
16. 點選Salesfoce的下拉選單，在Filter中輸入Email，點擊選單中的Email
17. 接下來點擊AIRIS field右側的**(X)**，點擊後會出現下拉選單，點擊email
18. 按下點擊export
19. Wait for import complete的訊息出現
20. 使用/rest/e.10/profiles抓取profile
https://www.woopra.com/rest/3.10/profiles?report_id=nxl6ldktnc&project=aiquasdk.prd.com&force=true&update_mapping=true
21. 使用api抓取salesforce Contact 內容
22. 進行比對
"""

class Todo(BaseModel):
    """
    Todo model for the todos list
    """
    id: int = Field(description="The id of the todo")
    type: str = Field(description="api or ui")
    description: str = Field(description="The description of the todo")
    status: str = Field(description="pending or done")


class AgentState(TypedDict, total=False):
    """
    AgentState defines the mutable state shared across the agent's workflow.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    todo_list: List[Todo]

class AutomationAgent:
    def __init__(self, model: ChatGoogleGenerativeAI):
        self.task_id = uuid.uuid4()
        self.model = model

        # create todo directory
        self.todo_dir = Path("todo")
        self.todo_dir.mkdir(exist_ok=True)
        self.todo_file = self.todo_dir / f"todo_{self.task_id}.md"


    async def plan_agent(self, state: AgentState):
        """
        1. Plan the todos list based on the goal
        2. Save the todos list to a todo_(task_id).md file
        3. Save the todos list to the state
        """
        
        # 创建 prompt
        planning_prompt = f"""
You are a task planner. Break down the user's goal into a list of actionable todos.

User's goal:
{state['messages'][0].content if state['messages'] else ''}

Categorize each todo as either "api" or "ui" type.

Return ONLY a JSON object in this exact format:
{{
    "todos": [
        {{"id": 1, "type": "api", "description": "Clear description", "status": "pending"}},
        {{"id": 2, "type": "ui", "description": "Clear description", "status": "pending"}}
    ]
}}
"""
        
        # Call LLM
        response = await self.model.ainvoke([HumanMessage(content=planning_prompt)])
        
        # Parse JSON
        try:
            # Use JsonFormatter to remove markdown markers
            print(response.content[0]["text"])
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
        system_prompt = SystemMessage(content=
           f"""


<web_agent_rules>
You are a web automation agent.

    - You should first distinguish which steps are UI operations and which are other operations. I want you to focus on the UI operations; for other operations, you can make API calls at the end to fetch information and write it into the script.
    - Please help me execute the steps related to UI operations, and after performing them, write a Playwright code for me to automate this test plan.
    - If, after clicking, you find that the next element cannot be found, please go back to the previous step and try clicking a different button.
</web_agent_rules>
            
<todo_rules>
    - Todo file is located at {self.todo_file}
    - After completing a step, please update its status to "done" from "pending" in the todo_file.
</todo_rules>
            """
        )

        # 確保有最後的human message
        human_msgs = [m for m in state['messages'] if isinstance(m, HumanMessage)]
        recent_msgs = [m for m in state['messages'] if not isinstance(m, HumanMessage)][-9:]

        # Get todo list
        with open(self.todo_file, "r", encoding="utf-8") as f:
            todo_file_content = f.read()

        # Add todo list to the recent messages
        recent_messages = [human_msgs[-1], HumanMessage(content=todo_file_content)] + recent_msgs

        # Invoke the model
        response = await self.model.ainvoke([system_prompt] + recent_messages)
        return {"messages": [response]}

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

            print(tools)

            model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY")).bind_tools(tools)
            agent = AutomationAgent(model=model)

    
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


            input = {"messages": [HumanMessage(content=goal)]}

            async for chunk in app.astream(input, stream_mode="values", config={"recursion_limit": 100}):
                print(chunk)



if __name__ == "__main__":
    asyncio.run(main())