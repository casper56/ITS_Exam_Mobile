import json

# 從最原始備份讀取文字內容
with open('backups/CLEAN_ORIGINAL_PYTHON.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 9:
        # 手動精確重構 ID 9 的結構
        q['explanation'] = [
            "<b>⭐ 運算順序拆解：</b>",
            r'''<pre><code class="language-python">1. a % b (24 % 7) = 3
2. 3 * 100 = 300
3. 2.0 ** 3.0 = 8.0
4. 300 // 8.0 = 37.0 (註：// 為地板除法，結果為 float)
5. 37.0 - 7 = 30.0</code></pre>''',
            "<b>⭐ 補充：負數的地板除法與取餘數規則</b>",
            r'''<table class="q-table w-100 t-left">
<thead>
    <tr>
        <th class="w-20">運算子</th>
        <th class="w-40">規則（向左取整）</th>
        <th class="w-20">正數範例</th>
        <th class="w-20">負數範例</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td><b>地板除 //</b></td>
        <td>取不大於商的最大整數</td>
        <td>7 // 2 = 3</td>
        <td>-7 // 2 = -4</td>
    </tr>
    <tr>
        <td><b>取餘數 %</b></td>
        <td>r = a - (b * (a // b))</td>
        <td>7 % 3 = 1</td>
        <td>-7 % 3 = 2</td>
    </tr>
</tbody>
</table>''',
            "<b>💡 記住：</b>負數除法時，// 會向負無窮大方向靠攏（-3.5 變成 -4）。"
        ]
        break

# 寫回 JSON
with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 9 終極手動精確修復完成！")
