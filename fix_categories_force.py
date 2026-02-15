import json

def fix_cs_categories():
    file_path = 'www/ITS_softdevelop/questions_ITS_csharp.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for q in data:
        qid = q['id']
        if qid == 110:
            q['category'] = "D2_物件導向程式設計"
            count += 1
        elif qid in [125, 126, 127]:
            q['category'] = "D3_一般軟體開發"
            count += 1
            
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"成功修正 {count} 題 C# 題目分類。")

if __name__ == "__main__":
    fix_cs_categories()
