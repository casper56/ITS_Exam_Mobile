import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 本地修正對象清單
for q in data:
    if 'question' in q and q['question']:
        # 修正第一行的標籤錯誤 (原本錯誤修復腳本誤加了 </pre>)
        first_line = q['question'][0]
        if '<pre><code' in first_line and first_line.endswith('</pre>'):
            q['question'][0] = first_line.replace('</pre>', '')
            
        # 修正最後一行的標籤閉合
        last_line = q['question'][-1]
        if not last_line.endswith('</code></pre>'):
            # 確保結尾包含完整的閉合
            q['question'][-1] = last_line.rstrip() + '</code></pre>'

    # 處理 explanation 陣列的對稱性
    if 'explanation' in q and q['explanation']:
        exp = q['explanation']
        if len(exp) > 0 and '<pre><code>' in exp[0] and not exp[-1].endswith('</code></pre>'):
             q['explanation'][-1] = exp[-1].rstrip() + '</code></pre>'

# 修正 A-01/A-02 的重複 <code>
for q in data:
    if 'question' in q:
        q['question'] = [line.replace('<code><code', '<code>').replace('</code></code>', '</code>') for line in q['question']]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("ITS_JAVA JSON 手動標籤位移修正完成。")
