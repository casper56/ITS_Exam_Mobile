import json
import re
import os

def html_table_to_markdown(html):
    rows = re.split(r'</tr>', html, flags=re.IGNORECASE)
    md_rows = []
    for r in rows:
        cells = re.findall(r'<t[dh].*?>(.*?)</t[dh]>', r, re.DOTALL | re.IGNORECASE)
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
    
    categories = {}
    for item in data:
        cat = item.get('category', 'Other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    output = "# ITS Software Development 技術重點 (ITS_SOFTDEVELOP.md)\n\n"
    output += "本文件整理自 `www/ITS_softdevelop/questions_ITS_softdevelop.json`，涵蓋核心程式設計、物件導向、軟體開發流程、Web 與資料庫等技術重點。\n\n---\n\n"
    
    for cat in sorted(categories.keys()):
        output += f"## {cat}\n\n"
        for item in categories[cat]:
            qid = item.get('id')
            explanation = "".join(item.get('explanation', []))
            tables = re.findall(r'<table.*?>(.*?)</table>', explanation, re.DOTALL | re.IGNORECASE)
            if tables:
                output += f"### 題目 ID: {qid}\n\n"
                for table_content in tables:
                    md_table = html_table_to_markdown(table_content)
                    if md_table: output += md_table + "\n\n"
        output += "---\n\n"
    return output

if __name__ == "__main__":
    json_path = os.path.join("www", "ITS_softdevelop", "questions_ITS_softdevelop.json")
    if os.path.exists(json_path):
        md_content = process_json(json_path)
        with open("ITS_SOFTDEVELOP.md", 'w', encoding='utf-8') as f:
            f.write(md_content)
        print("Successfully created ITS_SOFTDEVELOP.md")
    else:
        print(f"Error: {json_path} not found")
