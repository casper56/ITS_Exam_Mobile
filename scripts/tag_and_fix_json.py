import json
import os
import re

def tag_and_fix():
    path = 'www/ITS_Python/questions_ITS_python.json'
    if not os.path.exists(path):
        print("File not found")
        return

    with open(path, 'rb') as f:
        raw = f.read()
    
    # 嘗試解決編碼問題
    content = None
    for enc in ['utf-8', 'utf-8-sig', 'cp950', 'big5']:
        try:
            content = json.loads(raw.decode(enc))
            print(f"Decoded with {enc}")
            break
        except:
            continue
    
    if not content:
        print("Failed to decode")
        return

    # 分類對照表
    cat_map = {
        'CH01': 'D1_資料型別與運算子',
        'CH02': 'D1_資料型別與運算子',
        'CH03': 'D1_資料型別與運算子',
        'CH04': 'D3_輸入輸出與檔案',
        'CH05': 'D2_流程控制與判斷',
        'CH06': 'D4_函式與註解',
        'CH07': 'D6_模組與常用工具',
        'CH08': 'D5_錯誤處理與測試'
    }

    count = 0
    for item in content:
        q_text = item.get('question', '')
        
        # 1. 根據 【CHxx】 標籤自動分類
        found_cat = False
        for ch, cat_name in cat_map.items():
            if ch in q_text:
                item['category'] = cat_name
                found_cat = True
                break
        
        if not found_cat:
            # 沒找到標籤的，給一個預設分類
            if not item.get('category'):
                item['category'] = 'D7_其他進階題型'
        
        # 2. 修復常見標籤錯誤 (特別是 ID 27 或類似的)
        if 'language-python>' in q_text:
            item['question'] = q_text.replace('language-python>', 'language-python">')
        
        count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully tagged {count} questions.")

if __name__ == "__main__":
    tag_and_fix()
