import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替換錯誤的標籤寫法
content = content.replace('<pre><code> class="language-java">', '<pre><code class="language-java">')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("已修復所有錯誤的 <pre><code> class=... 標籤")
