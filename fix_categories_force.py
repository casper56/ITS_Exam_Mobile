# -*- coding: utf-8 -*-
import json
import os

def fix_mojibake_categories():
    path = 'www/ITS_Python/questions_ITS_python.json'
    if not os.path.exists(path): return

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 暴力修正表
    mapping = {
        'D1': 'D1_資料型別與運算子',
        'D2': 'D2_流程控制',
        'D3': 'D3_輸入與輸出',
        'D4': 'D4_程式碼文件與結構',
        'D5': 'D5_錯誤處理與測試',
        'D6': 'D6_模組與工具'
    }

    count = 0
    for q in data:
        cat = q.get('category', '')
        # 只要開頭是 D1~D6，不管後面是亂碼還是什麼，全部強制覆蓋為正確名稱
        for key, correct_name in mapping.items():
            if cat.startswith(key):
                q['category'] = correct_name
                count += 1
                break
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Fixed {count} category labels.")

if __name__ == "__main__":
    fix_mojibake_categories()
