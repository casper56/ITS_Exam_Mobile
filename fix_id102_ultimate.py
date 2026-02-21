import json

# 從最原始備份讀取
with open('backups/CLEAN_ORIGINAL_PYTHON.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 102:
        # 手動重組 ID 102
        q['explanation'] = [
            r'''<pre><code class="language-python">● random.choices：支援 weights 參數，可用於「可重覆」隨機抽樣。
● random.sample：不支援 weights 參數，且抽樣數 k 不能大於樣本總數。</code></pre>''',
            "<b>選項解析與錯誤原因：</b>",
            r'''<table class="q-table w-100 t-left"><thead><tr><th class="w-20">序號</th><th class="w-40">語法範例</th><th class="w-40">結果與錯誤說明</th></tr></thead><tbody><tr><td><b>1 (正確)</b></td><td>choices(..., weights=[10, 30, 60], k=5)</td><td>● <b>成功</b>：依 1:3:6 權重隨機抽取 5 次（可重覆）。</td></tr><tr><td><b>2</b></td><td>sample(..., weights=[...])</td><td>● <b>錯誤</b>：sample 函式不接受 weights 參數 (TypeError)。</td></tr><tr><td><b>3</b></td><td>choices(..., k=5)</td><td>● <b>不符題意</b>：未設權重，導致機率均等 (各 33.3%)。</td></tr><tr><td><b>4</b></td><td>sample(..., 5)</td><td>● <b>錯誤</b>：樣本只有 3 個，無法不重覆抽取 5 個 (ValueError)。</td></tr></tbody></table>'''
        ]
        break

# 寫回
with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 102 終極手動修正完成！")
