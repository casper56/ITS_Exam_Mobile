# -*- coding: utf-8 -*-
import json
import re

def patch_categories():
    path = 'www/ITS_Python/questions_ITS_python.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 官方分類映射
    cat_map = {
        'D1': 'D1_資料型別與運算子',
        'D2': 'D2_流程控制',
        'D3': 'D3_輸入與輸出',
        'D4': 'D4_程式碼文件與結構',
        'D5': 'D5_錯誤處理與測試',
        'D6': 'D6_模組與工具'
    }

    for q in data:
        text = q['question']
        
        # 根據 CH 標籤判定 (這是最準確的)
        if 'CH01' in text or 'CH02' in text or 'CH03' in text:
            q['category'] = cat_map['D1']
        elif 'CH05' in text:
            q['category'] = cat_map['D2']
        elif 'CH04' in text:
            # CH04 在 ITS 中通常包含 格式化輸出 與 檔案處理，屬於 D3 或 D1
            # 這裡暫時歸類為 D3
            q['category'] = cat_map['D3']
        elif 'CH06' in text:
            q['category'] = cat_map['D4']
        elif 'CH08' in text:
            q['category'] = cat_map['D5']
        elif 'CH07' in text:
            q['category'] = cat_map['D6']
        
        # 兜底判斷 (如果沒有 CH 標籤，則根據關鍵字)
        if 'category' not in q or not q['category']:
            if 'import' in text or 'random' in text or 'math' in text:
                q['category'] = cat_map['D6']
            elif 'try' in text or 'except' in text or 'unittest' in text:
                q['category'] = cat_map['D5']
            elif 'input' in text or 'open' in text or 'print' in text:
                q['category'] = cat_map['D3']
            elif 'if ' in text or 'while' in text or 'for ' in text:
                q['category'] = cat_map['D2']
            else:
                q['category'] = cat_map['D1']

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Categories patched.")

if __name__ == '__main__':
    patch_categories()
