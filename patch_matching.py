import json
import re

html_path = 'www/ITS_Python/ITS_Python.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定義新的題目資料
new_question_data = {
    "id": 26,
    "type": "matching",
    "question": [
        "<pre><code class=\"language-python\">26. 【CH03-5】你有以下清單結構：alph = \"abcdefghijklmnopqrstuvwxyz\"",
        "以下各個程式碼片段的結果各是如何？",
        "請將右側的執行結果拖拉或點選至左側對應的程式碼中：</code></pre>"
    ],
    "left": [
        "(1) alph[3:15]",
        "(2) alph[3:15:3]",
        "(3) alph[15:3:-3]",
        "(4) alph[::-3]"
    ],
    "right": [
        "A. zwtqnkheb",
        "B. pmjg",
        "C. defghijklmno",
        "D. ponmlkjihgfe",
        "E. defghijklmnop",
        "F. dgjm",
        "G. olif"
    ],
    "answer": [2, 5, 1, 0],
    "weight": 1,
    "image": None,
    "explanation": [
        "<pre><code class=\"language-python\">● alph[3:15] -> 從索引 3 到 14 (d...o)，結果為 C (defghijklmno)",
        "● alph[3:15:3] -> 從索引 3 開始每隔 3 格取一字 (d, g, j, m)，結果為 F (dgjm)",
        "● alph[15:3:-3] -> 從索引 15 (p) 倒退回 3，每隔 3 格取一字 (p, m, j, g)，結果為 B (pmjg)",
        "● alph[::-3] -> 全字串倒退，從最後一字 (z) 開始每隔 3 格取一字，結果為 A (zwtqnkheb)</code></pre>"
    ],
    "category": "D1_資料型別與運算子"
}

# 使用更強力的正則表達式來尋找 ID 26 塊
# 從 { 開始，包含 "id": 26，直到對應的 },
pattern = re.compile(r'\{\s*\"id\": 26,.*?\}\,', re.DOTALL)

def replacement_text(match):
    # 手動構造 JSON 字串以避免編碼問題，並與原檔縮進風格保持一致
    res = json.dumps(new_question_data, ensure_ascii=False, indent=8)
    return res + ","

if pattern.search(content):
    new_content = pattern.sub(replacement_text, content)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: ID 26 updated to matching type in HTML.")
else:
    # 嘗試另一種可能的格式（不帶引號的 ID）
    pattern2 = re.compile(r'\{\s*id: 26,.*?\}\,', re.DOTALL)
    if pattern2.search(content):
        new_content = pattern2.sub(replacement_text, content)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("SUCCESS: ID 26 (unquoted) updated to matching type in HTML.")
    else:
        print("ERROR: Could not find ID 26 block in HTML.")
