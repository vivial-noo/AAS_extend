import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_client , gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio
# from aas_tools import read_local_xml


# # 配置Client MODEL，GPTAPI_KEY.


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://api.openai.com/v1"  
)

set_default_openai_client(client)

# # AAS_Agent = Agent(
# #     name="AAS(Asset Administration Shell) Agent",
# #     instructions="你是一个熟悉工业4.0和AAS结构的助手,能够查阅处理AAS(Asset Administration Shell)相关内容，还能读取对应的XML和JSON文件,提取子模型信息，并且还能通过python和basyx-python-sdk的库构建子模型服务器并且执行SDK操作。",
# #     model="gpt-4o",
# #     tools=[read_local_xml]  
# # )

  
# # async def main():
# #     result = await Runner.run(agent, input="请读取同一目录下的 ./Simple_Submodel.xml, 并转换成人类可读的文本形式")
# #     print(result.final_output)

# # if __name__ == "__main__":
# #     asyncio.run(main())
# from agents import Agent, Runner
# from agents.mcp import MCPServerHttp
# import asyncio

# async def main():
#     mcp_server = MCPServerHttp(url="http://localhost:8000")  # 连接 server_1.py 中的 mcp 服务

#     agent = Agent(
#         name="AAS Agent",
#         instructions="从 AAS 服务中查询属性值。",
#         mcp_servers=[mcp_server]
#     )

#     result = await Runner.run(
#         starting_agent=agent,
#         input="请帮我查找 battery_1.xml 中 idShort 为 MainProduction 的值"
#     )
#     print(result.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())
import asyncio
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from agents.tracing import gen_trace_id

async def main():
    async with MCPServerStdio(
        name="AAS Multi-tool Server",
        params={"command": "python", "args": ["Agents_SDK/tmp_1/AGENT_AAS/mcp_server_AAS_1.py"]},
        cache_tools_list=True
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Query AAS", trace_id=trace_id):
            print(f"🔍 Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            agent = Agent(
                name="AAS Agent",
                instructions="你可以读取 AAS 文件中的属性、列出它们、或者做数值运算。",
                mcp_servers=[server]
            )
            result = await Runner.run(
                starting_agent=agent,
                input="请查找 battery_1.xml 中 MainProduction 的值，并计算它加上 20 的结果是多少？"
            )
            print("✅ 最终输出：", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
