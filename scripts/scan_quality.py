import json
import re
import os

def check_quality():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'www', 'ITS_Python', 'questions_ITS_python.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    suspicious_ids = []
    
    print(f"Total questions: {len(questions)}")
    print("-" * 50)

    for q in questions:
        q_id = q['id']
        q_type = q.get('type', 'single')
        q_text = q.get('question', '')
        options = q.get('options', [])
        answers = q.get('answer', [])

        # 檢查 1: 答案長度不符
        if q_type == 'multioption':
            if len(options) != len(answers):
                print(f"[ID {q_id}] Length Mismatch: Options({len(options)}) vs Answers({len(answers)})")
        
        # 檢查 2: 疑似 ID 27 的結構問題 (Yes/No 題型但缺乏上下文)
        # 判斷標準：選項包含 '|' (是子題組)，且內容極短 (只有選項沒有描述)，且題目文字中包含列表特徵
        if q_type == 'multioption':
            is_simple_bool = all(opt in ['Yes|No', 'True|False', 'Correct|Incorrect', 'O|X'] for opt in options)
            has_list_in_text = bool(re.search(r'\d+\.\s*[\w\W]+Yes[\w\W]+No', q_text))
            
            if is_simple_bool and has_list_in_text:
                print(f"[ID {q_id}] Suspicious 'Yes|No' list format (Like ID 27)")
                suspicious_ids.append(q_id)

        # 檢查 3: 填空題數量不符
        # 統計題目中的空格數
        blanks = len(re.findall(r'_\(選項 \d+\)_', q_text))
        if blanks > 0 and q_type == 'multioption':
            if blanks != len(options):
                print(f"[ID {q_id}] Fill-in-blanks Mismatch: Found {blanks} blanks in text, but {len(options)} options.")

    return suspicious_ids

if __name__ == "__main__":
    check_quality()
