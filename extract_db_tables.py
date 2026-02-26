import json
import re
import os

def html_table_to_markdown(html):
    rows = re.split(r'</tr>', html, flags=re.IGNORECASE)
    md_rows = []
    for r in rows:
        cells = re.findall(r'<td.*?>(.*?)</td>', r, re.DOTALL | re.IGNORECASE)
        if not cells: continue
        clean_cells = []
        for cell in cells:
            cell = re.sub(r'<.*?>', '', cell)
            cell = cell.replace('\r', '').replace('\n', ' ').strip()
            clean_cells.append(cell)
        md_rows.append("| " + " | ".join(clean_cells) + " |")
    if not md_rows: return ""
    cols_count = md_rows[0].count('|') - 1
    separator = "|" + " --- |" * cols_count
    md_rows.insert(1, separator)
    return "\n".join(md_rows)

def process_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    output = "# ITS Database 技術重點 - 表格彙整 (ITS_DATABASE_TECH.md)\n\n"
    output += "本文件整理自 `www/ITS_Database/questions_ITS_Database.json`，提取其中包含的技術對照表與語法說明。\n\n---\n\n"
    for item in data:
        qid = item.get('id')
        explanation = "".join(item.get('explanation', []))
        tables = re.findall(r'<table.*?>(.*?)</table>', explanation, re.DOTALL | re.IGNORECASE)
        if tables:
            output += f"## 題目 ID: {qid}\n\n"
            for table_content in tables:
                md_table = html_table_to_markdown(table_content)
                if md_table: output += md_table + "\n\n"
            output += "---\n\n"
    return output

if __name__ == "__main__":
    json_path = os.path.join("www", "ITS_Database", "questions_ITS_Database.json")
    if os.path.exists(json_path):
        md_content = process_json(json_path)
        with open("ITS_DATABASE_TECH.md", 'w', encoding='utf-8') as f:
            f.write(md_content)
        print("Successfully created ITS_DATABASE_TECH.md")
    else:
        print(f"Error: {json_path} not found")
