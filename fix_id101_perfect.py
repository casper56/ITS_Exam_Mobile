import json

# 從最原始備份讀取文字內容
with open('backups/CLEAN_ORIGINAL_PYTHON.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 101:
        # 手動精確重構 ID 101 的結構
        q['explanation'] = [
            "\u2b50 <b>random \u6a21\u7d44\u62bd\u6a23\u898f\u5247\uff1a</b>",
            r'''<pre><code class="language-python">● random.sample(population, k) -> 「不重覆」抽樣 (Without replacement)
● random.choices(population, k=N) -> 「可重覆」抽樣 (With replacement)</code></pre>''',
            "<b>⭐ 常用隨機方法功能比較表：</b>",
            r'''<table class="q-table w-100 t-left">
<thead>
    <tr>
        <th class="w-20">方法 (Method)</th>
        <th class="w-15">功能簡述</th>
        <th class="w-20">語法範例</th>
        <th class="w-25">參數 k (Count)</th>
        <th class="w-20">抽樣特點</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td><b>sample</b></td>
        <td>抽樣</td>
        <td>sample(seq, 3)</td>
        <td><b>k=3</b> (必填)</td>
        <td>● <b>不重覆</b> (Unique)</td>
    </tr>
    <tr>
        <td><b>choices</b></td>
        <td>抽樣</td>
        <td>choices(seq, k=3)</td>
        <td><b>k=3</b> (選填，預設1)</td>
        <td>● <b>可重覆</b> (Repeats)</td>
    </tr>
    <tr>
        <td><b>choice</b></td>
        <td>隨機挑一</td>
        <td>choice(seq)</td>
        <td>無此參數</td>
        <td>單次 <b>不可重覆</b></td>
    </tr>
    <tr>
        <td><b>pick</b></td>
        <td>(誤導選項)</td>
        <td>N/A</td>
        <td>N/A</td>
        <td>● <b>Python 無此語法</b></td>
    </tr>
</tbody>
</table>'''
        ]
        break

# 寫回 JSON
with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 101 終極精確修復完成！")
