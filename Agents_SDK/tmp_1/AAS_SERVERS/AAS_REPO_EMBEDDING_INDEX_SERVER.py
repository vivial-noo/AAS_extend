import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import json
from pathlib import Path

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

mcp = FastMCP("IDTA Template Search via ChromaDB")

# 加载文件为 metadata
META_PATH = Path("Agents_SDK/tmp_1/AAS_SERVERS/idta_templates_index.json")
with open(META_PATH, "r", encoding="utf-8") as f:
    templates = json.load(f)

#创建了本地持久化的向量库，而不是储存在内存中，不需要每次重新构建
chroma_client = chromadb.PersistentClient(path="Agents_SDK/tmp_1/AAS_SERVERS/chroma_storage") 
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=API_KEY,  
    model_name="text-embedding-3-small"
)
try:
    # 尝试获取已有 collection
    collection = chroma_client.get_collection(
        name="idta_templates",
        embedding_function=openai_ef
    )
except:
    # 如果不存在才创建
    collection = chroma_client.create_collection(
        name="idta_templates",
        embedding_function=openai_ef
    )
# 此处的collection 自动索引，不需要像faiss 一样手动index 
# 如果空则填充
if len(collection.get()["ids"]) == 0:
    documents = [f"{t['title']}. {t['scope']}" for t in templates]
    ids = [t["id"] for t in templates]
    metadatas = [
        {"title": t["title"], "template_file": t["template_file"], "folder_path": t["folder_path"]}
        for t in templates
    ]
    collection.add(documents=documents, ids=ids, metadatas=metadatas)

# 定义 tool 输入模型
class SearchInput(BaseModel):
    query: str
    top_k: int = 3

# 定义 MCP tool
@mcp.tool(name="search_templates", description="根据用户描述搜索最相关的 IDTA 子模型")
def search_templates_tool(input: SearchInput) -> list[dict]:
    results = collection.query(query_texts=[input.query], n_results=input.top_k)
    response = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        response.append({
            "id": results["ids"][0][i],
            "title": meta["title"],
            "template_file": meta["template_file"],
            "folder_path": meta["folder_path"]
        })
    return response

# # 可选 resource (如果使用resource )
# @mcp.resource("template://search/{query}")
# def search_templates_resource(query: str) -> list[dict]:
#     return search_templates_tool(query, top_k=3)

# 启动 server 
if __name__ == "__main__":
    mcp.run(transport="stdio")
