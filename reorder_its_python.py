import json
import os

def reorder_ids():
    json_path = 'www/ITS_Python/questions_ITS_python.json'
    config_path = 'www/config.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 1. 分類題目
    # 現在 1-91 為官方版
    official_old = [q for q in questions if 1 <= q['id'] <= 91]
    others = [q for q in questions if q['id'] > 91]
    
    # 2. 合併並排序
    all_questions = official_old + others
    all_questions.sort(key=lambda x: x['id'])
    
    # 3. 寫回 JSON 題庫 (確保編碼與格式正確)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=4)
    print(f"題庫 ID 重新編排完成！官方題現在為 1-91。")
    
    # 4. 更新 config.json 中的 cutoff
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        for subj in config['subjects']:
            if subj['id'] == 'itspy' or subj['title'] == 'ITS Python':
                subj['cutoff'] = 91
                subj['cutoff_info'] = "1-91 為官方版題數"
                print(f"Config 更新：ITS Python cutoff 已改為 91")
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    reorder_ids()
