import json
import re

# 從最乾淨的原始備份讀取
with open('backups/CLEAN_ORIGINAL_PYTHON.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_html_content(text):
    # 移除可能存在的殘留標籤
    return text.replace('<code>', '').replace('</code>', '').replace('<pre>', '').replace('</pre>', '').strip()

def standardize_table(table_html):
    # 1. 套用標準 CSS 類別，移除舊屬性
    table_html = re.sub(r'<table[^>]*>', '<table class="q-table w-100 t-left">', table_html)
    # 2. 移除內聯背景色
    table_html = table_html.replace("style='background-color: #f2f2f2;'", "").replace('style="background-color: #f2f2f2;"', "")
    # 3. 確保 thead/tbody 結構
    if '<tr>' in table_html and '<thead>' not in table_html:
        table_html = table_html.replace('<tr>', '<thead><tr>', 1)
        tr_end = table_html.find('</tr>')
        if tr_end != -1:
            table_html = table_html[:tr_end+5] + '</thead><tbody>' + table_html[tr_end+5:]
    if '</table>' in table_html and '</tbody>' not in table_html:
        table_html = table_html.replace('</table>', '</tbody></table>')
    return table_html

target_ids = [9, 101, 102, 106, 108, 110, 112, 115, 116, 117, 120, 124, 132]

for q in data:
    if q['id'] in target_ids:
        # 合併所有 explanation 陣列內容
        full_content = "".join(q['explanation'])
        
        # 使用表格標籤進行拆分，保留表格標籤本身
        parts = re.split(r'(<table.*?</table>)', full_content, flags=re.DOTALL)
        
        new_exps = []
        for p in parts:
            if not p.strip(): continue
            
            if p.startswith('<table'):
                # 處理表格：分離並標準化
                table_clean = clean_html_content(p)
                new_exps.append(standardize_table(table_clean))
            else:
                # 處理非表格：處理加粗標題與代碼塊
                # 1. 拆分 <b> 標題
                sub_parts = re.split(r'(<b>.*?</b>)', p, flags=re.DOTALL)
                for sp in sub_parts:
                    sp_clean = clean_html_content(sp)
                    if not sp_clean: continue
                    
                    if sp.startswith('<b>'):
                        # 標題獨立成一行 HTML
                        new_exps.append(sp_clean)
                    else:
                        # 代碼部分包回標準標籤
                        new_exps.append(f'<pre><code class="language-python">{sp_clean}</code></pre>')
        
        q['explanation'] = new_exps

# 儲存
with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ITS Python 全題庫表格與結構已全面標準化完成！")
