from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import os
import dotenv
import asyncio

dotenv.load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))

SERVER_PARAM = StdioServerParameters(
    command="npx",
    args=["-y", "chrome-devtools-mcp@latest", "--isolated"]
)

async def main():
    async with stdio_client(SERVER_PARAM) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)

            graph = create_agent(model=llm, tools=tools)

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


你可以先分辨哪些是UI操作哪些是其他操作，我希望你可以專注在UI上面，其他操作你可以在最後打api來獲取資訊並寫在程式中

請幫我使用chrome-devtools-mcp執行UI操作相關的內容，並在執行後幫我寫一個playwright code，用於執行這個test plan的automation

            """

            async for chunk in graph.astream(
                {"messages": [HumanMessage(content=goal)]}, 
                stream_mode="updates",
                config={"recursion_limit": 200}
            ):
                print(chunk)

if __name__ == "__main__":
    asyncio.run(main())