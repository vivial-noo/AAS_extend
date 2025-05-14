# # server.py
# import os
# from typing import Optional, List

# # ── FastMCP / Pydantic ─────────────────────────────────────────────────────────
# from mcp.server.fastmcp import FastMCP
# from pydantic import BaseModel, Field

# # ── BaSyx AAS SDK ──────────────────────────────────────────────────────────────
# from basyx.aas.adapter.xml import read_aas_xml_file
# from basyx.aas import model


# # ───────────────────────────────────────────────────────────────────────────────
# XML_PATH = "Agents_SDK/tmp_1/AGENT_AAS/battery_1.xml"           # ← 根据需要调整
# AAS_DATA: model.DictObjectStore      # 全局缓存，用于查询


# def load_aas_xml(path: str) -> model.DictObjectStore:
#     """一次性读取 XML 并缓存到内存。"""
#     local_path = os.getcwd()
#     return read_aas_xml_file(path)

# def get_property_value(id_short: str) -> str | None:
#     i = 0
#     for identifiable in store:  
#         print(f'第{i}次，{identifiable}')
#         if isinstance(identifiable, model.Submodel):
#             for elem in identifiable.submodel_element:
#                 print(elem.id_short)
#                 if isinstance(elem, model.Property) and elem.id_short == id_short:
#                     return elem.value
#     return None

# # ── FastMCP Server 实例 ────────────────────────────────────────────────────────
# mcp = FastMCP("Local AAS query")

# # 在启动时加载 XML
# AAS_DATA = load_aas_xml(XML_PATH)     # type: ignore[assignment]


# # --------------------------  Resource  ----------------------------------------
# class AASResourceRequest(BaseModel):
#     """输入模型：请求一个 idShort 对应的值"""
#     id_short: str = Field(..., description="Property idShort to query")


# @mcp.resource("aas://local/{id_short}")
# def get_value_resource(id_short: str) -> str | None:
#     """
#     Resource 形式（GET 语义）：
#     • URL 形如  aas://local/MainPro duction
#     • 返回字符串数值或 None
#     """
#     return find_property_value(id_short)


# -----------------------------  Tool  -----------------------------------------
# @mcp.tool(name="get_value", description="Query value in local AAS by idShort")
# def get_value_tool(id_short: str) -> str:
#     """
#     Tool 形式（POST 语义，可在 ChatGPT Function Calling / Agents 中调用）
#     """
#     value = find_property_value(id_short)
#     if value is None:
#         raise ValueError(f"idShort '{id_short}' not found")
#     return value


# -------------------------  入口点  -------------------------------------------
# if __name__ == "__main__":
#     # FastAPI + Uvicorn。FastMCP 自带 run()，便于本地调试
#     mcp.run(host="0.0.0.0", port=8000, reload=True)
# if __name__ == "__main__":
#     print("当前工作目录:", os.getcwd())
#     store: model.DictObjectStore[model.Identifiable] = read_aas_xml_file(XML_PATH)

#     value = get_property_value("MainProduction")
#     print("✅ MainProduction 的值是:", value)

# server.py
import os
import uvicorn
from typing import Optional
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from basyx.aas.adapter.xml import read_aas_xml_file
from basyx.aas import model

BASE_DIR = Path(__file__).resolve().parent
AAS_DIR = BASE_DIR 

AAS_STORE_CACHE: dict[str, model.DictObjectStore] = {}

def load_store_from_file(filename: str) -> model.DictObjectStore:
    filepath = AAS_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"❌ 文件不存在: {filepath}")
    if filename not in AAS_STORE_CACHE:
        AAS_STORE_CACHE[filename] = read_aas_xml_file(str(filepath))
    return AAS_STORE_CACHE[filename]

def get_property_value_from_file(filename: str, id_short: str) -> Optional[str]:
    store = load_store_from_file(filename)
    for obj in store:
        if isinstance(obj, model.Submodel):
            for elem in obj.submodel_element:
                if isinstance(elem, model.Property) and elem.id_short == id_short:
                    return elem.value
    return None

mcp = FastMCP("Multi-file AAS Query")

@mcp.resource("aas://{filename}/{id_short}")
def query_property_value(filename: str, id_short: str) -> str | None:
    return get_property_value_from_file(filename, id_short)

@mcp.tool(name="query_value", description="Get value from AAS XML by filename and idShort")
def query_value_tool(filename: str, id_short: str) -> str:
    value = get_property_value_from_file(filename, id_short)
    if value is None:
        raise ValueError(f"Property '{id_short}' not found in '{filename}'")
    return value


if __name__ == "__main__":
    print("✅ 当前目录:", os.getcwd())
    print("📂 AAS 文件目录:", AAS_DIR)

    print(query_property_value("battery_1.xml", "MainProduction"))

    uvicorn.run("server:mcp", host="0.0.0.0", port=8000, reload=True)
    # mcp.run(host="0.0.0.0", port=8000, reload=True)
