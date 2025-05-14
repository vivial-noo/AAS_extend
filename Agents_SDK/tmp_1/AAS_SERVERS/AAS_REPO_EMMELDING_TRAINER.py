import os
import json
import zipfile
import re
from pathlib import Path

def unzip_repo(zip_path: str, extract_to: str) -> str:
    """解压 ZIP 文件，返回解压后的根目录路径"""
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    extracted_dirs = [d for d in Path(extract_to).iterdir() if d.is_dir()]
    return str(extracted_dirs[0]) if extracted_dirs else extract_to

def extract_scope_from_readme(readme_path: Path) -> str:
    """从 README.md 中提取 Scope of the Submodel 段落"""
    text = readme_path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"Scope of the Submodel\s*[:\-]?\s*(.*?)(?=\n\s*\n|\Z)", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else "N/A"

def find_template_json(folder: Path) -> tuple[str, str] | None:
    """找到 template JSON 文件，返回 (id, filename)"""
    json_files = [f for f in folder.glob("*.json") if "template" in f.name.lower()]
    if not json_files:
        return None

    json_file = json_files[0]
    # 提取如 'IDTA 02034-1-0' 的完整前缀
    match = re.match(r"(IDTA\s?\d{5}-\d+-\d+)", json_file.name)
    file_id = match.group(1).replace(" ", "") if match else "UNKNOWN"

    return file_id, json_file.name

def build_index(published_dir: Path) -> list[dict]:
    """从 published 文件夹构建模板索引 JSON"""
    results = []

    for top_dir in published_dir.iterdir():
        if not top_dir.is_dir():
            continue
        title = top_dir.name

        for version_dir in top_dir.rglob("*"):
            if not version_dir.is_dir():
                continue

            json_info = find_template_json(version_dir)
            if json_info:
                file_id, template_file = json_info
                readme_path = version_dir / "README.md"
                scope = extract_scope_from_readme(readme_path) if readme_path.exists() else "N/A"
                folder_rel_path = version_dir.relative_to(published_dir.parent)
                results.append({
                    "id": file_id,
                    "title": title,
                    "scope": scope,
                    "folder_path": str(folder_rel_path),
                    "template_file": template_file
                })
    return results

if __name__ == "__main__":
    # 修改为你的 zip 文件路径
    zip_path = "/Users/chenwei/python projekt 2025/AAS_extend/Agents_SDK/tmp_1/AAS_SERVERS/submodel-templates-main.zip"
    extract_dir = "/Users/chenwei/python projekt 2025/AAS_extend/Agents_SDK/tmp_1/AAS_SERVERS/unzipped"
    output_json = "/Users/chenwei/python projekt 2025/AAS_extend/Agents_SDK/tmp_1/AAS_SERVERS/idta_templates_index.json"

    print("📦 正在解压 ZIP...")
    repo_root = unzip_repo(zip_path, extract_dir)
    published_path = Path(repo_root) / "published"

    print("🔍 正在构建模板索引...")
    index = build_index(published_path)

    print(f"💾 正在保存 JSON 文件到 {output_json}...")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print("✅ 完成！共索引模板数:", len(index))
