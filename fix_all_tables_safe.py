import json
import re

# 從最乾淨的備份讀取
with open('backups/questions_ITS_python_pre_table_search.json.bak', 'r', encoding='utf-8') as f:
    data = json.load(f)

def standardize_table(html):
    # 移除舊式內聯樣式
    html = re.sub(r'<table[^>]*>', '<table class="q-table w-100 t-left"><thead>', html)
    # 移除 th 上的背景色
    html = html.replace("style='background-color: #f2f2f2;'", "")
    html = html.replace('style="background-color: #f2f2f2;"', "")
    # 強制結構
    if '</thead>' in html and '<tbody>' not in html:
        html = html.replace('</th></tr>', '</th></tr></thead><tbody>')
    if '</table>' in html and '</tbody>' not in html:
        html = html.replace('</table>', '</tbody></table>')
    return html

for q in data:
    if 'explanation' not in q: continue
    
    new_exps = []
    for exp in q['explanation']:
        if '<table' in exp:
            # 尋找表格起始點
            idx = exp.find('<table')
            
            # 第一部分：表格前的內容
            part1 = exp[:idx].strip()
            # 嘗試尋找表格前的標題 <b>
            title_idx = part1.rfind('<b>')
            if title_idx != -1:
                part2_start = part1[title_idx:]
                part1 = part1[:title_idx].strip()
            else:
                part2_start = ""
            
            # 閉合 part1 的 pre/code
            if '<pre>' in part1 and ' </pre>' not in part1:
                if not part1.endswith('</code></pre>'):
                    part1 += '</code></pre>'
            
            # 第二部分：表格本體
            part2 = part2_start + exp[idx:].strip()
            # 移除 part2 內部的結尾標籤
            part2 = part2.replace('</code></pre>', '')
            # 標準化表格
            part2 = standardize_table(part2)
            
            if part1: new_exps.append(part1)
            new_exps.append(part2)
        else:
            new_exps.append(exp)
    
    q['explanation'] = new_exps

with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ITS Python 所有表格已完成全自動安全標準化修正！")
