import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_client
import asyncio

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://api.openai.com/v1"  
)
set_default_openai_client(client)


# MySQL = os.getenv("MySQL")
# MySQL_ENV = MySQL.env
# MySQL_ENV_HOST = MySQL.env.MYSQL_HOST
# MySQL_ENV_PORT = MySQL.env.MYSQL_PORT
# MySQL_ENV_USR = MySQL.env.MYSQL_USER
# MySQL_ENV_PASSWORD = MySQL.env.PASSWORD
# MySQL_ENV_DATABASE = MySQL.env.DATABASE


import asyncio
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio, MCPServerSse
from agents.tracing import gen_trace_id

async def main():
    async with MCPServerSse(
        name="Excel MCP Server",
        params={"url": "http://localhost:8000/sse"},
        cache_tools_list=True
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Extra Data from Excel", trace_id=trace_id):
            print(f"🔍 Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            agent = Agent(
                name="DATA",
                instructions="你可以读取，查询来自DouchDB,MySQL,本地EXCEL等文件的内容，同时也可以创建",
                mcp_servers=[server]
            )
            # message = "帮我在绝对相对路径/Users/chenwei/python projekt 2025/AAS_extend/Agents_SDK/tmp_1/AGENT_EXTRA内创建一个名为weights的excel文件并设置sheet的名字为weights-for-battery。"
            # print("\n" + "-" * 40)
            # print(f"Running: {message}")
            # result = await Runner.run(starting_agent=agent, input=message)
            # print(result.final_output)

            # message = '在绝对相对路径/Users/chenwei/python projekt 2025/AAS_extend/Agents_SDK/tmp_1/AGENT_EXTRA/weights.xlsx文件的weights-for-battery内加入数据[{"name": ["W_RawMaterialExtraction","W_MainProduction","W_Distribution","W_Recycling"],"value": [0.5, 0.2, 0.2, 0.1]}]'
            # print("\n" + "-" * 40)
            # print(f"Running: {message}")
            # result = await Runner.run(starting_agent=agent, input=message)
            # print(result.final_output)
                        
            message = '帮我读取绝对相对路径/Users/chenwei/python projekt 2025/AAS_extend/Agents_SDK/tmp_1/AGENT_EXTRA/weights.xlsx文件的weights-for-battery这个sheet中的name为W_Distribution的数值'
            print("\n" + "-" * 40)
            print(f"Running: {message}")
            result = await Runner.run(starting_agent=agent, input=message)
            # print(result.final_output)
            
            # result = await Runner.run(
            #     starting_agent=agent,
            #     input="请查找 battery_1.xml 中 MainProduction 的值，并计算它加上 20 的结果是多少？"
            # )
            print("✅ 最终输出：", result.final_output)

if __name__ == "__main__":
    
    asyncio.run(main())


# async def run(mcp_server: MCPServer, directory_path: str):
#     agent = Agent(
#         name="Assistant",
#         instructions=f"Answer questions about the git repository at {directory_path}, use that for repo_path",
#         mcp_servers=[mcp_server],
#     )

#     message = "Who's the most frequent contributor?"
#     print("\n" + "-" * 40)
#     print(f"Running: {message}")
#     result = await Runner.run(starting_agent=agent, input=message)
#     print(result.final_output)

#     message = "Summarize the last change in the repository."
#     print("\n" + "-" * 40)
#     print(f"Running: {message}")
#     result = await Runner.run(starting_agent=agent, input=message)
#     print(result.final_output)


# async def main():
#     # Ask the user for the directory path
#     directory_path = input("Please enter the path to the git repository: ")

#     async with MCPServerStdio(
#         cache_tools_list=True,  # Cache the tools list, for demonstration
#         params={"command": "uvx", "args": ["mcp-server-git"]},
#     ) as server:
#         with trace(workflow_name="MCP Git Example"):
#             await run(server, directory_path)


# if __name__ == "__main__":
#     if not shutil.which("uvx"):
#         raise RuntimeError("uvx is not installed. Please install it with `pip install uvx`.")

#     asyncio.run(main())