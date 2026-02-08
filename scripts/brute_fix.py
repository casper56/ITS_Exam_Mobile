import json

def final_cleanup(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # 移除任何 Git 標記
        if line.strip().startswith('<<<<<<<') or line.strip().startswith('=======') or line.strip().startswith('>>>>>>>'):
            continue
        new_lines.append(line)
    
    content = "".join(new_lines)
    
    # 暴力修正重複的 category 屬性（因為它們通常緊鄰且缺逗號）
    # 尋找 "category": "..." 緊接著 "category": "..." 的情況
    import re
    # 修正缺逗號且重複的情況
    content = re.sub(r'("category":\s*"[^"]*")\s*
?\s*"category":\s*"[^"]*"', r'\1', content)
    
    # 嘗試解析
    try:
        data = json.loads(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("JSON Cleaned and structure fixed!")
    except Exception as e:
        print(f"Still error: {e}")
        # 如果還是錯，就用最原始的 regex 尋找報錯位置
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

final_cleanup('www/ITS_Python/questions_ITS_python.json')
