import json
import os

def reorder_ids():
    json_path = 'www/ITS_Python/questions_ITS_python.json'
    config_path = 'www/config.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 1. 分類題目
    official_old = [q for q in questions if 1 <= q['id'] <= 69]
    official_new = [q for q in questions if q['id'] in [181, 182]]
    others = [q for q in questions if q['id'] >= 70 and q['id'] not in [181, 182]]
    
    # 2. 分配新 ID
    # 官方版 (1-69) 不動
    
    # 新官方版 (181 -> 70, 182 -> 71)
    for q in official_new:
        if q['id'] == 181: q['id'] = 70
        elif q['id'] == 182: q['id'] = 71
        
    # 其他補充題 (原本 70 開始的往後移 2 位)
    for q in others:
        q['id'] += 2
        
    # 3. 合併並排序
    all_questions = official_old + official_new + others
    all_questions.sort(key=lambda x: x['id'])
    
    # 4. 寫回 JSON 題庫 (確保編碼與格式正確)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=4)
    print(f"題庫 ID 重新編排完成！官方題現在為 1-71。")
    
    # 5. 更新 config.json 中的 cutoff
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        for subj in config['subjects']:
            if subj['id'] == 'itspy' or subj['title'] == 'ITS Python':
                subj['cutoff'] = 71
                print(f"Config 更新：ITS Python cutoff 已改為 71")
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    reorder_ids()
