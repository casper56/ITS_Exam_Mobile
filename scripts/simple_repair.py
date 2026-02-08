import json

def repair():
    path = 'www/ITS_Python/questions_ITS_python.json'
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    clean_lines = []
    for l in lines:
        s = l.strip()
        if s.startswith('<<<<<<<') or s.startswith('=======') or s.startswith('>>>>>>>'):
            continue
        clean_lines.append(l)
    
    content = "".join(clean_lines)
    
    # 手動修復已知重複點
    bad_part = '"category": "D3_輸入輸出與檔案"
        "category": "D3_輸入與輸出"'
    good_part = '"category": "D3_輸入輸出與檔案"'
    content = content.replace(bad_part, good_part)
    
    # 再修復一次可能的重複
    bad_part2 = '"category": "D3_輸入輸出與檔案" "category": "D3_輸入與輸出"'
    content = content.replace(bad_part2, good_part)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 嘗試載入看看
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("Repair Success!")
    except Exception as e:
        print(f"Still failing: {e}")

repair()
