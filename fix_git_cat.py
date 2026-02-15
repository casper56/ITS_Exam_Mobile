import json
import os

def fix_git_category():
    file_path = 'www/ITS_softdevelop/questions_ITS_csharp.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    target_ids = [12, 48, 49, 50, 51]
    count = 0
    for q in data:
        if q['id'] in target_ids:
            q['category'] = "D3_一般軟體開發"
            count += 1
            
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"成功修正 {count} 題 Git 相關題目至 D3_一般軟體開發。")

if __name__ == "__main__":
    fix_git_category()
