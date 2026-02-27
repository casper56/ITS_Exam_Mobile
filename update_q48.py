import json
import re

# 定義新題目結構
new_q48 = {
    "id": 48,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">48. 【CH05-6】你設計一個 Python 程式來檢查使用者輸入的數字是 1 位數、 2 位數還是 2 位數以上。",
        "請將正確的 Python 條件判斷式配對到對應的邏輯描述中：</code></pre>"
    ],
    "left": [
        "(1) 判斷是否為 1 位數 ( < 10 )",
        "(2) 判斷是否為 2 位數 ( 10 ~ 99 )",
        "(3) 判斷是否為 2 位數以上 ( >= 100 )"
    ],
    "right": [
        "A. if num < 10:",
        "B. if num < 100:",
        "C. elif num < 100:",
        "D. else:"
    ],
    "answer": [0, 2, 3],
    "weight": 1,
    "image": None,
    "explanation": [
        "<pre><code class="language-python">● 第一步使用 if num < 10: 判斷 1 位數。",
        "● 第二步使用 elif num < 100: 判斷 2 位數 (此時已排除 < 10 的情況)。",
        "● 最後使用 else: 處理所有剩餘情況 (即 100 以上)。</code></pre>"
    ],
    "category": "D2_流程控制與判斷"
}

def patch_question(content):
    # 使用 regex 定位 ID 48 塊並替換
    pattern = re.compile(r'\{\s*"id": 48,.*?\}\,', re.DOTALL)
    replacement = json.dumps(new_q48, ensure_ascii=False, indent=8) + ","
    return pattern.sub(replacement, content)

# 1. 更新 JSON
json_path = 'www/ITS_Python/questions_ITS_python.json'
with open(json_path, 'r', encoding='utf-8') as f:
    json_content = f.read()
with open(json_path, 'w', encoding='utf-8') as f:
    f.write(patch_question(json_content))

# 2. 更新 ITS_Python.html
html_path = 'www/ITS_Python/ITS_Python.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(patch_question(html_content))

# 3. 更新 mock_v34.html
mock_path = 'www/ITS_Python/mock_v34.html'
if os.path.exists(mock_path):
    with open(mock_path, 'r', encoding='utf-8') as f:
        mock_content = f.read()
    with open(mock_path, 'w', encoding='utf-8') as f:
        f.write(patch_question(mock_content))

print("SUCCESS: Question 48 updated to matching type across all files.")
