import json

path = 'www/ITS_Python/questions_ITS_python.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 找到 ID 106 的題目
for q in data:
    if q['id'] == 106:
        # 修正 explanation 的字串陣列結構，分離 pre 標籤與表格標籤
        q['explanation'] = [
            '<pre><code class="language-python"> assertTrue(x) (賊1)  unittest 皞瘜\n assertIsTrue (賊2) 銝璅寞嚗銵梢</code></pre>',
            '<b>迤蝣箏扯”</b><table class="q-table w-100 t-left"><thead><tr><th class="w-25">瑼Ｘ格</th><th class="w-35"> 航炊撖急 (銝)</th><th class="w-40"> 甇Ⅱ撖急</th></tr></thead><tbody><tr><td>撽 True</td><td>assertIsTrue</td><td><b>assertTrue</b></td></tr><tr><td>撽 False</td><td>assertIsFalse</td><td><b>assertFalse</b></td></tr></tbody></table>'
        ]
        break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 106 JSON 修正成功！")
