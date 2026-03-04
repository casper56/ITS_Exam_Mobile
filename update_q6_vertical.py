import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 修改 Q6 為 8 行垂直展開版
new_q6 = {
    "id": 6,
    "type": "matching",
    "question": [
        '<pre><code class="language-java">【A-6】請審視下列程式碼片段。(行號僅供參考)',
        '01 byte num=127;',
        '02 num++;',
        '03 System.out.println(num);',
        '04 System.out.println(1.0 / 3.0);',
        '05 System.out.println(1.0f / 3.0f);',
        '06 System.out.println(1 / 3);',
        '',
        '請選取正確的選項來回答問題。</code></pre>'
    ],
    "left": [
        "A. 第 03 行的輸出為何？",
        "&nbsp;",
        "B. 第 04 行的輸出為何？",
        "&nbsp;",
        "C. 第 05 行的輸出為何？",
        "&nbsp;",
        "D. 第 06 行的輸出為何？",
        "&nbsp;"
    ],
    "right": [
        "<code>-128</code>",
        "<code>128</code>",
        "<code>0.3333333333333333</code>",
        "<code>0.33333334</code>",
        "<code>0.3333333333333333</code>",
        "<code>0.33333334</code>",
        "<code>0.33333334</code>",
        "<code>0</code>"
    ],
    "answer": [
        "A",
        "",
        "C",
        "",
        "F",
        "",
        "H",
        ""
    ],
    "weight": 1,
    "image": None,
    "explanation": [
        "A: byte 溢位，127 + 1 = -128。",
        "B: double 精度較高 (0.3333333333333333)。",
        "C: float 精度較低 (0.33333334)。",
        "D: 整數除法結果為 0。"
    ],
    "category": "資料型別與運算子"
}

for i, item in enumerate(data):
    if item['id'] == 6:
        data[i] = new_q6
        break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("JSON split-row update complete.")
