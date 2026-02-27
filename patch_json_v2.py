import json
import os

json_path = 'www/ITS_Python/questions_ITS_python.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 定義新題目 (ID 48)
q48_new = {
    "id": 48,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">48. 【CH05-7】你在設計一個 Python 程式遊戲，讓參加的人從 1 到 100 之間猜一個數字，最多有三次機會。",
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

# 定義新題目 (ID 49)
q49_new = {
    "id": 49,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">49. 【CH05-8】你有兩個 Python 列表 aList 和 bList，你需要進行各種邏輯判斷。",
        "請將正確的判斷表達式配對到對應的邏輯需求中：</code></pre>"
    ],
    "left": [
        "(1) 檢查數值 x 是否存在於 aList 中",
        "(2) 檢查 aList 的第一個元素是否等於 1",
        "(3) 檢查 aList 與 bList 的內容是否完全相同"
    ],
    "right": [
        "A. x in aList",
        "B. aList[0] == 1",
        "C. aList == bList",
        "D. aList is bList",
        "E. aList.count(x) > 0"
    ],
    "answer": [0, 1, 2],
    "weight": 1,
    "image": None,
    "explanation": [
        "<pre><code class="language-python">● 使用 'in' 運算子可以快速檢查成員資格。",
        "● 使用索引 [0] 可以存取第一個元素並進行比較。",
        "● 使用 == 可以比較兩個列表的內容是否一致。</code></pre>"
    ],
    "category": "D2_流程控制與判斷"
}

# 更新資料
for i in range(len(data)):
    if data[i]['id'] == 48:
        data[i] = q48_new
    elif data[i]['id'] == 49:
        data[i] = q49_new

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("SUCCESS: JSON ID 48 and 49 updated to matching format.")
