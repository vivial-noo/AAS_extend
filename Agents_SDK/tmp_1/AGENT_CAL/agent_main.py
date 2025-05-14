import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_client
import asyncio
from aas_tools import read_local_xml

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://api.openai.com/v1"  
)

set_default_openai_client(client)

# triage_agent = Agent(
#     name="Triage Agent",
#     instructions="如果用户问题是关于数据融合，交给DateintegrationAgent；如果是关于AAS(Asset Administration Shell)的模版内容，交给 TemplatesearchAgent。",
#     model="gpt-4-turbo",
#     handoff_agents=[Dateintegration_Agent, Templatesearch_Agent]。)

# Dateintegration_Agent.handoffs.append(triage_agent)
# Templatesearch_Agent.handoffs.append(triage_agent)

# Dateintegration_Agent = Agent(
#     name="AAS(Asset Administration Shell) Data Agent",
#     instructions="你是一个熟悉工业4.0和AAS结构的助手,能够查阅处理AAS(Asset Administration Shell) Shell文件,提取子模型信息，并且还能通过python和basyx-python-sdk的库构建子模型服务器并且执行SDK操作。",
#     model="gpt-4-turbo",
#     tools=[read_local_xml]  
# )

# Templatesearch_Agent = Agent(
#     name="AAS(Asset Administration Shell) Data Agent",
#     instructions="你是一个熟悉工业4.0和AAS结构的助手,能够查阅处理AAS(Asset Administration Shell) Shell文件,提取子模型信息，并且还能通过python和basyx-python-sdk的库构建子模型服务器并且执行SDK操作。",
#     model="gpt-4-turbo",
#     tools=[read_local_xml]  
# )

# async def main():
#     result = await Runner.run(agent, input="请读取同一目录下的 ./Simple_Submodel.xml, 并转换成人类可读的文本形式")
#     print(result.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())
