import json
import re

# 從最乾淨的備份讀取 (確保最原始)
with open('backups/questions_ITS_python_pre_table_search.json.bak', 'r', encoding='utf-8') as f:
    data = json.load(f)

def standardize_table(html):
    # 移除舊式屬性，套用標準類別
    html = re.sub(r'<table[^>]*>', '<table class="q-table w-100 t-left">', html)
    html = html.replace("style='background-color: #f2f2f2;'", "").replace('style="background-color: #f2f2f2;"', "")
    
    # 強力結構修復：確保 thead 和 tbody 正確對齊
    # 1. 尋找第一個 </tr> (表頭結束)
    if '<tr>' in html and '<thead>' not in html:
        html = html.replace('<tr>', '<thead><tr>', 1)
        first_tr_end = html.find('</tr>')
        if first_tr_end != -1:
            html = html[:first_tr_end+5] + '</thead><tbody>' + html[first_tr_end+5:]
    
    if '</table>' in html and '</tbody>' not in html:
        html = html.replace('</table>', '</tbody></table>')
    
    return html

for q in data:
    if 'explanation' not in q: continue
    
    new_exps = []
    for exp in q['explanation']:
        if '<table' in exp:
            idx = exp.find('<table')
            part1 = exp[:idx].strip()
            
            # 尋找 <b>
            title_idx = part1.rfind('<b>')
            if title_idx != -1:
                part2_start = part1[title_idx:]
                part1 = part1[:title_idx].strip()
            else:
                part2_start = ""
            
            # 確保 part1 閉合
            if '<pre>' in part1:
                if '</code>' not in part1: part1 += '</code>'
                if '</pre>' not in part1: part1 += '</pre>'
            
            # 表格主體
            part2 = part2_start + exp[idx:].strip()
            part2 = part2.replace('</code></pre>', '')
            part2 = standardize_table(part2)
            
            if part1: new_exps.append(part1)
            new_exps.append(part2)
        else:
            # 即使沒有表格，也確保 pre 閉合 (防止 ID 102 這種分散在陣列的情況)
            if '<pre>' in exp and '</pre>' not in exp:
                exp += '</code></pre>'
            new_exps.append(exp)
    
    q['explanation'] = new_exps

with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 102 及所有表格結構強化修正完成！")
