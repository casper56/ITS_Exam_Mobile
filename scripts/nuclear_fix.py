import os
import json

def nuclear_fix():
    path = 'www/ITS_Python/questions_ITS_python.json'
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # 1. 移除包含 Git 標記的行
    clean_lines = []
    for l in lines:
        s = l.strip()
        if s.startswith('<<<<<<<') or s.startswith('=======') or s.startswith('>>>>>>>'):
            continue
        # 也移除遠端 hash 標記
        if s.startswith('HEAD') or (len(s) == 40 and all(c in '0123456789abcdef' for c in s)):
             continue
        clean_lines.append(l)
    
    content = "".join(clean_lines)
    
    # 2. 暴力補齊可能缺失的逗號
    import re
    # 尋找 "prop": "value" (換行) "prop2": ... 並在中間補逗號
    content = re.sub(r'("[^"]*"\s*:\s*(?:"[^"]*"|\d+|null|\[[^\]]*\]))\s*
?\s*(")', r'\1,
\2', content)
    
    # 3. 移除重複的 category (不分內容)
    content = re.sub(r'("category":\s*"[^"]*"),?\s*
?\s*"category":\s*"[^"]*"', r'\1', content)
    
    # 4. 再次清理多餘逗號 (例如 ,])
    content = content.replace(',]', ']').replace(',}', '}')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Nuclear Fix Applied.")

nuclear_fix()
