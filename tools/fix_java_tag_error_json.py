import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if 'question' in q:
        q['question'] = [line.replace('<pre><code> class="language-java">', '<pre><code class="language-java">') for line in q['question']]
    if 'explanation' in q:
        q['explanation'] = [line.replace('<pre><code> class="language-java">', '<pre><code class="language-java">') for line in q['explanation']]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("已徹底修復 JSON 內的標籤錯誤")
