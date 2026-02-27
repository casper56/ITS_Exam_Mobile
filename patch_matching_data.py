import json
import os

# 1. 定義題目資料 (使用 hex 轉義或簡單字串避開編碼與引號問題)
q26_new = {
    "id": 26,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">【CH03-5】你有以下清單結構：alph = "abcdefghijklmnopqrstuvwxyz"
以下各個程式碼片段的結果各是如何？
請將右側的執行結果拖拉或點選至左側對應的程式碼中：</code></pre>"
    ],
    "left": ["(1) alph[3:15]", "(2) alph[3:15:3]", "(3) alph[15:3:-3]", "(4) alph[::-3]"],
    "right": ["A. zwtqnkheb", "B. pmjg", "C. defghijklmno", "D. ponmlkjihgfe", "E. defghijklmnop", "F. dgjm", "G. olif"],
    "answer": [2, 5, 1, 0],
    "weight": 1,
    "image": None,
    "explanation": ["<pre><code class="language-python">● alph[3:15] -> 從索引 3 到 14 (d...o)，結果為 C (defghijklmno)
● alph[3:15:3] -> 從索引 3 開始每隔 3 格取一字 (d, g, j, m)，結果為 F (dgjm)
● alph[15:3:-3] -> 從索引 15 (p) 倒退回 3，每隔 3 格取一字 (p, m, j, g)，結果為 B (pmjg)
● alph[::-3] -> 全字串倒退，從最後一字 (z) 開始每隔 3 格取一字，結果為 A (zwtqnkheb)</code></pre>"],
    "category": "D1_資料型別與運算子"
}

q48_new = {
    "id": 48,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">【CH05-6】你設計一個 Python 程式來檢查使用者輸入的數字是 1 位數、 2 位數還是 2 位數以上。
請將正確的 Python 條件判斷式配對到對應的邏輯描述中：</code></pre>"
    ],
    "left": ["(1) 判斷是否為 1 位數 ( < 10 )", "(2) 判斷是否為 2 位數 ( 10 ~ 99 )", "(3) 判斷是否為 2 位數以上 ( >= 100 )"],
    "right": ["A. if num < 10:", "B. if num < 100:", "C. elif num < 100:", "D. else:"],
    "answer": [0, 2, 3],
    "weight": 1,
    "image": None,
    "explanation": ["<pre><code class="language-python">● 第一步使用 if num < 10: 判斷 1 位數。
● 第二步使用 elif num < 100: 判斷 2 位數 (此時已排除 < 10 的情況)。
● 最後使用 else: 處理所有剩餘情況 (即 100 以上)。</code></pre>"],
    "category": "D2_流程控制與判斷"
}

def sync_file(file_path):
    if not os.path.exists(file_path): return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 尋找 quizData 的 JSON 部分
    if 'const quizData = ' in content:
        start_tag = 'const quizData = ['
        end_tag = '];'
        start_idx = content.find(start_tag)
        end_idx = content.find(end_tag, start_idx)
        
        json_str = content[start_idx + len(start_tag) - 1 : end_idx + 1]
        data = json.loads(json_str)
        
        for i in range(len(data)):
            if data[i]['id'] == 26: data[i] = q26_new
            elif data[i]['id'] == 48: data[i] = q48_new
            
        new_json_str = json.dumps(data, ensure_ascii=False, indent=4)
        new_content = content[:start_idx + len(start_tag) - 1] + new_json_str + content[end_idx + 1:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Synced {file_path}")
    elif file_path.endswith('.json'):
        data = json.loads(content)
        for i in range(len(data)):
            if data[i]['id'] == 26: data[i] = q26_new
            elif data[i]['id'] == 48: data[i] = q48_new
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Synced {file_path}")

sync_file('www/ITS_Python/questions_ITS_python.json')
sync_file('www/ITS_Python/ITS_Python.html')
sync_file('www/ITS_Python/mock_v34.html')
