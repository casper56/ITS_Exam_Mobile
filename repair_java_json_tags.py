import json
import re

def repair_tags(text):
    if not isinstance(text, str):
        return text
    
    # 統計標籤
    pre_open = len(re.findall(r'<pre>', text))
    pre_close = len(re.findall(r'</pre>', text))
    code_open = len(re.findall(r'<code>', text))
    code_close = len(re.findall(r'</code>', text))
    
    # 修正原則：如果只有閉合沒有開口，補開口；如果只有開口沒有閉合，補閉合
    # 針對 ITS 系統常見錯誤：<pre><code> 開頭，結尾卻是 </code></pre>
    
    # 處理 </code> 但沒有 <code> 的情況
    if code_close > code_open:
        # 檢查是否漏了 <code> (常見於 <pre> 後面直接接內容)
        text = text.replace('<pre>', '<pre><code>')
        # 重新計算
        code_open = len(re.findall(r'<code>', text))
        code_close = len(re.findall(r'</code>', text))

    # 如果還是不平，移除多餘的閉合標籤
    while len(re.findall(r'</code>', text)) > len(re.findall(r'<code>', text)):
        text = re.sub(r'</code>(?!.*</code>)', '', text, count=1) # 移除最後一個
        
    while len(re.findall(r'</pre>', text)) > len(re.findall(r'<pre>', text)):
        text = re.sub(r'</pre>(?!.*</pre)', '', text, count=1)
        
    # 補齊未閉合的
    if len(re.findall(r'<pre>', text)) > len(re.findall(r'</pre>', text)):
        text += '</pre>'
    if len(re.findall(r'<code>', text)) > len(re.findall(r'</code>', text)):
        # 確保在 </pre> 之前閉合
        if '</pre>' in text:
            text = text.replace('</pre>', '</code></pre>')
        else:
            text += '</code>'
            
    # 移除重複嵌套
    text = text.replace('<code><code>', '<code>')
    text = text.replace('</code></code>', '</code>')
    return text

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if 'question' in q:
        q['question'] = [repair_tags(line) for line in q['question']]
    if 'explanation' in q:
        q['explanation'] = [repair_tags(line) for line in q['explanation']]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("ITS_JAVA JSON 標籤修復完成。")
