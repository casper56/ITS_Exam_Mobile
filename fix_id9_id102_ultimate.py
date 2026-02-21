import json

# 從備份讀取
with open('backups/CLEAN_ORIGINAL_PYTHON.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 9:
        q['explanation'] = [
            "\u2b50 <b>\u904b\u7b97\u9806\u5e8f\u62c6\u89e3\uff1a</b>",
            r'''<pre><code class="language-python">1. a % b = (24 % 7) = 3
2. 3 * 100 = 300
3. 2.0 ** 3.0 = 8.0
4. 300 // 8.0 = 37.0
5. 37.0 - 7 = 30.0</code></pre>''',
            "<b>\u8aaa\u660e\uff1a// \u6703\u5411\u8ca0\u7121\u7aae\u5927\u65b9\u5411\u53d6\u6574\u3002</b>",
            r'''<table class="q-table w-100 t-left"><thead><tr><th>運算子</th><th class="w-35">規則（向左取整）</th><th>正數範例</th><th>負數範例</th></tr></thead><tbody><tr><td><b>地板除 //</b></td><td>取不大於商的最大整數</td><td>7 // 2 = 3</td><td>-7 // 2 = -4</td></tr><tr><td><b>取餘數 %</b></td><td>r = a - (b * (a // b))</td><td>7 % 3 = 1</td><td>-7 % 3 = 2</td></tr></tbody></table>''',
            "<b>\u8a18\u4f4f\uff1a</b>\u8ca0\u6578\u9664\u6cd5\u6642\uff0c\u9918\u6578\u7684\u6b63\u8ca0\u8207<b>\u9664\u6578</b>\u76d8\u540c\u3002"
        ]
    
    if q['id'] == 102:
        q['explanation'] = [
            r'''<pre><code class="language-python">✅ **random.choices** 可以使用 weights 參數設定機率。
❌ **random.sample** 不支援 weights 參數。</code></pre>''',
            "<b>\u9078\u9805\u8a73\u7d30\u89e3\u6790\uff1a</b>",
            r'''<table class="q-table w-100 t-left"><thead><tr><th>題號</th><th>語法參數</th><th>結果與錯誤</th></tr></thead><tbody><tr><td><b>1 (正確)</b></td><td>choices(..., weights=[...], k=5)</td><td>成功依機率抽取 5 次</td></tr><tr><td><b>2</b></td><td>sample(..., weights=...)</td><td>引發 TypeError</td></tr><tr><td><b>3</b></td><td>choices(..., k=5)</td><td>機率均等（非題意）</td></tr><tr><td><b>4</b></td><td>sample(..., 5)</td><td>引發 ValueError (樣本數不足)</td></tr></tbody></table>'''
        ]

# 寫回
with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 9, 102 修正成功！")
