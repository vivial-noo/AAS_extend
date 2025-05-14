# """
# This example demonstrates a deterministic multi-agent workflow that interacts with an AAS server using Eclipse BaSyx Python SDK.

# 1. Agent 1 fetches external real-world data (e.g., from sensors or APIs).
# 2. Agent 2 queries existing models or submodels from the AAS server.
# 3. Agent 3 fuses and processes the external and AAS data.
# 4. Agent 4 builds a new submodel and registers it into the AAS server.
# """

# import asyncio
# from pydantic import BaseModel
# from agents import Agent, Runner, function_tool
# from basyx.aas import model as aas_model
# from basyx.aas.adapter import aasx, json
# from basyx.aas.client import ConnectedAASManagerHTTP

# # =========================
# # Step 1: External Data Tool
# # =========================
# @function_tool
# def fetch_external_data() -> dict:
#     """Simulate fetching sensor data"""
#     return {
#         "temperature": 23.5,
#         "pressure": 1.02
#     }

# # ============================
# # Step 2: Fetch AAS Submodels
# # ============================
# @function_tool
# def fetch_submodel_data(aas_id: str, submodel_id: str) -> dict:
#     """Use BaSyx SDK to get submodel data from AAS server"""
#     client = ConnectedAASManagerHTTP("http://localhost:4000/shells")
#     sm = client.get_submodel(aas_id, submodel_id)
#     return sm.to_json()

# # ============================
# # Step 3: Fuse and Process Data
# # ============================
# class FusionInput(BaseModel):
#     external: dict
#     aas_model: dict

# @function_tool
# def fuse_and_process(input: FusionInput) -> dict:
#     """Merge and normalize data"""
#     external = input.external
#     model = input.aas_model
#     fused = {
#         "avg_temperature": (external["temperature"] + model.get("temperature", 0)) / 2,
#         "status": "ok" if external["pressure"] < 1.5 else "high"
#     }
#     return fused

# # ============================
# # Step 4: Register Submodel
# # ============================
# @function_tool
# def register_new_submodel(aas_id: str, submodel_id: str, data: dict) -> str:
#     """Register a new submodel using BaSyx SDK"""
#     client = ConnectedAASManagerHTTP("http://localhost:4000/shells")
#     sm = aas_model.Submodel(id_short=submodel_id, identification=submodel_id)
#     for k, v in data.items():
#         sm.submodel_element.append(
#             aas_model.Property(id_short=k, value=v)
#         )
#     client.post_submodel(aas_id, sm)
#     return f"Submodel {submodel_id} registered to AAS {aas_id}"

# # ============================
# # Agents
# # ============================
# agent_1 = Agent(
#     name="ExternalDataAgent",
#     instructions="Fetch external sensor data.",
#     function_tools=[fetch_external_data]
# )

# agent_2 = Agent(
#     name="AASModelAgent",
#     instructions="Fetch submodel data from AAS server.",
#     function_tools=[fetch_submodel_data]
# )

# agent_3 = Agent(
#     name="FusionAgent",
#     instructions="Fuse external and AAS data into a new format.",
#     function_tools=[fuse_and_process]
# )

# agent_4 = Agent(
#     name="RegistrarAgent",
#     instructions="Upload the fused data to AAS as a new submodel.",
#     function_tools=[register_new_submodel]
# )

# # ============================
# # Runner
# # ============================
# async def main():
#     ext_data = await Runner.run(agent_1, input="")
#     aas_data = await Runner.run(agent_2, input={"aas_id": "DemoAsset", "submodel_id": "SensorModel"})
#     fused = await Runner.run(agent_3, input={
#         "external": ext_data.final_output,
#         "aas_model": aas_data.final_output
#     })
#     result = await Runner.run(agent_4, input={
#         "aas_id": "DemoAsset",
#         "submodel_id": "FusedModel",
#         "data": fused.final_output
#     })
#     print(result.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())
