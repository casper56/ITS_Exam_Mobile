import json

# 讀取目前最新的 JSON
path = 'www/ITS_softdevelop/questions_ITS_softdevelop.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 22:
        # 將 ID 22 的解析重組為細緻的字串陣列 (逐行表格標籤)
        q['explanation'] = [
            "<b>⭐ 顯式介面實作與方法覆寫：</b>",
            "題目考點在於如何同時處理「類別繼承的覆寫」與「介面顯式實作」。",
            "<b>實作細節對照：</b>",
            '<table class="q-table w-100 t-left">',
            '  <thead>',
            '    <tr><th>實作方式</th><th>技術名稱</th><th>存取與行為</th></tr>',
            '  </thead>',
            '  <tbody>',
            '    <tr><td>override Display()</td><td>方法覆寫</td><td>取代父類別行為。</td></tr>',
            '    <tr><td>DisplayRaw()</td><td>一般方法</td><td>類別專屬新功能。</td></tr>',
            '    <tr><td>IDisplayResult.Display()</td><td>顯式介面實作</td><td><b>必須轉型為介面</b>才能呼叫。</td></tr>',
            '  </tbody>',
            '</table>',
            "<b>執行結果解析：</b>",
            r'''<pre><code class="language-csharp">r1.Display() -> 執行 override -> 99
r2.Display() -> 執行介面實作 -> 99 seconds
r1.DisplayRaw() -> 執行新方法 -> 1.65 minutes</code></pre>'''
        ]
        break

# 寫回
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 22 表格已改為字元陣列換行表示！")
