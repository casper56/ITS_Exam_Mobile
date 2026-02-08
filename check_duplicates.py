# -*- coding: utf-8 -*-
import json
import re
from collections import defaultdict

def find_duplicates():
    path = 'www/ITS_Python/questions_ITS_python.json'
    with open(path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    # 用來存放標準化後的文字與對應的 ID
    text_map = defaultdict(list)

    print(f"Scanning {len(questions)} questions for duplicates...")
    print("-" * 50)

    for q in questions:
        q_id = q['id']
        raw_text = q['question']
        
        # 標準化處理：
        # 1. 移除開頭的數字編號 (如 "82. ", "【CH01-1】")
        clean_text = re.sub(r'^\d+[\.\s]*', '', raw_text)
        clean_text = re.sub(r'【.*?】', '', clean_text)
        # 2. 移除所有 HTML 標籤
        clean_text = re.sub(r'<[^>]+>', '', clean_text)
        # 3. 移除所有空白、換行與特殊標點
        clean_text = re.sub(r'\s+', '', clean_text)
        
        text_map[clean_text].append(q_id)

    # 找出重複項
    duplicates_found = False
    for text, ids in text_map.items():
        if len(ids) > 1:
            duplicates_found = True
            print(f"Found Duplicate Content (IDs: {ids}):")
            # 顯示一小段內容供參考
            content_snippet = text[:50] + "..." if len(text) > 50 else text
            print(f"  Content: {content_snippet}")
            print("-" * 30)

    if not duplicates_found:
        print("No exact duplicates found based on question text.")

if __name__ == "__main__":
    find_duplicates()
