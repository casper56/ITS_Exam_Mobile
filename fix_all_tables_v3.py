import json
import re

# 從最乾淨的備份讀取
with open('backups/questions_ITS_python_pre_table_search.json.bak', 'r', encoding='utf-8') as f:
    data = json.load(f)

def standardize_table(html):
    # 清理舊屬性
    html = re.sub(r'<table[^>]*>', '<table class="q-table w-100 t-left">', html)
    html = html.replace("style='background-color: #f2f2f2;'", "").replace('style="background-color: #f2f2f2;"', "")
    
    # 確保 thead/tbody 結構
    if '<tr>' in html and '<thead>' not in html:
        html = html.replace('<tr>', '<thead><tr>', 1)
        tr_end = html.find('</tr>')
        if tr_end != -1:
            html = html[:tr_end+5] + '</thead><tbody>' + html[tr_end+5:]
    
    if '</table>' in html and '</tbody>' not in html:
        html = html.replace('</table>', '</tbody></table>')
    return html

for q in data:
    if 'explanation' not in q: continue
    
    # 合併為大字串
    full_content = "".join(q['explanation'])
    
    # 使用表格標籤進行分割
    parts = re.split(r'(<table.*?</table>)', full_content, flags=re.DOTALL)
    
    new_exps = []
    for p in parts:
        p = p.strip()
        if not p: continue
        
        if p.startswith('<table'):
            # 表格部分：確保不含 pre/code
            clean_table = p.replace('<code>', '').replace('</code>', '').replace('<pre>', '').replace('</pre>', '')
            new_exps.append(standardize_table(clean_table))
        else:
            # 非表格部分：如果是程式碼片段，確保標籤閉合
            # 移除可能殘留的半個標籤
            p = p.replace('</code></pre>', '').replace('<pre><code class="language-python">', '').strip()
            if p:
                # 重新包裝成標準程式碼區塊
                new_exps.append(f'<pre><code class="language-python">{p}</code></pre>')
    
    q['explanation'] = new_exps

with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 9, 102 及所有表格 V3 終極修復完成！")
