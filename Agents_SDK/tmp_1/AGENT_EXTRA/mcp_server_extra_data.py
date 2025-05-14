import random
from pathlib import Path
from typing import Optional

import requests
from mcp.server.fastmcp import FastMCP
from basyx.aas.adapter.xml import read_aas_xml_file
from basyx.aas import model

# 初始化 FastMCP 服务
mcp = FastMCP("Extra Data Tool Server")

# 本地 XML 存储缓存
BASE_DIR = Path(__file__).resolve().parent
AAS_STORE_CACHE: dict[str, model.DictObjectStore] = {}

def load_aas(filename: str) -> model.DictObjectStore:
    path = BASE_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"找不到文件：{path}")
    if filename not in AAS_STORE_CACHE:
        AAS_STORE_CACHE[filename] = read_aas_xml_file(str(path))
    return AAS_STORE_CACHE[filename]

@mcp.tool()
def query_value(filename: str, id_short: str) -> str:
    """
    查找 XML 文件中指定 idShort 的属性值。
    """
    store = load_aas(filename)
    for obj in store:
        if isinstance(obj, model.Submodel):
            for elem in obj.submodel_element:
                if isinstance(elem, model.Property) and elem.id_short == id_short:
                    return elem.value
    raise ValueError(f"未找到 {id_short} in {filename}")

@mcp.tool()
def list_properties(filename: str) -> list[str]:
    """
    列出文件中所有 Property 的 id_short。
    """
    store = load_aas(filename)
    result = []
    for obj in store:
        if isinstance(obj, model.Submodel):
            for elem in obj.submodel_element:
                if isinstance(elem, model.Property):
                    result.append(elem.id_short)
    return result

@mcp.tool()
def get_secret_word() -> str:
    """
    返回随机单词，作为调试。
    """
    return random.choice(["apple", "banana", "cherry"])

if __name__ == "__main__":
   
    mcp.run(transport='stdio')