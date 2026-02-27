import json
import re
import os

# 定義新題目結構 (ID 49)
new_q49 = {
    "id": 49,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">49. 【CH05-7】你在設計一個 Python 程式遊戲，讓參加的人從 1 到 100 之間猜一個數字，最多有三次機會。",
        "請將正確的程式碼片段配對到對應的遊戲邏輯中：</code></pre>"
    ],
    "left": [
        "(1) 設定重複執行次數 (最多 3 次)",
        "(2) 當猜對時，立即跳出迴圈",
        "(3) 每次猜錯後，將次數加 1"
    ],
    "right": [
        "A. while chance <= 3:",
        "B. break",
        "C. pass",
        "D. chance += 1",
        "E. while chance < 3:",
        "F. chance = 2"
    ],
    "answer": [0, 1, 3],
    "weight": 1,
    "image": None,
    "explanation": [
        "<pre><code class="language-python">● 使用 while chance <= 3: 可確保程式執行 3 次 (1, 2, 3)。",
        "● 當猜中數字時，使用 break 立即結束 while 迴圈。",
        "● 每次迴圈結尾執行 chance += 1 紀錄進度。</code></pre>"
    ],
    "category": "D2_流程控制與判斷"
}

def patch_question(content, q_id, new_data):
    # 精確定位特定 ID 的 JSON 物件
    pattern = re.compile(r'\{\s*"id": ' + str(q_id) + r',.*?\}\,', re.DOTALL)
    replacement = json.dumps(new_data, ensure_ascii=False, indent=8) + ","
    if pattern.search(content):
        return pattern.sub(replacement, content)
    return content

# 執行更新
files = [
    'www/ITS_Python/questions_ITS_python.json',
    'www/ITS_Python/ITS_Python.html',
    'www/ITS_Python/mock_v34.html'
]

for f_path in files:
    if os.path.exists(f_path):
        with open(f_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = patch_question(content, 49, new_q49)
        
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"SUCCESS: Question 49 updated in {f_path}")

