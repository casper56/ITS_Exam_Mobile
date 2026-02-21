import json

# 從最乾淨的備份讀取
with open('backups/questions_ITS_python_id132_id9_prefix.json.bak', 'r', encoding='utf-8') as f:
    data = json.load(f)

def fix_table_in_explanation(q_id, exp_index):
    for q in data:
        if q['id'] == q_id:
            orig = q['explanation'][exp_index]
            # 尋找表格起始點
            split_point = orig.find('<table')
            if split_point == -1: return
            
            # 第一部分：保留到表格之前，手動閉合 code/pre
            part1 = orig[:split_point].strip()
            # 如果表格前有 <b> 標題，設法保留它在表格上方
            title_point = part1.rfind('<b>')
            if title_point != -1:
                # 把標題移到 part2
                part2_start = part1[title_point:]
                part1 = part1[:title_point].strip()
            else:
                part2_start = ""

            if not part1.endswith('</code></pre>'):
                part1 += '</code></pre>'
            
            # 第二部分：表格區塊，移除多餘的結尾標籤
            part2 = part2_start + orig[split_point:].replace('</code></pre>', '').strip()
            
            # 清理 table 標籤樣式
            old_table_start = "<table border='1' cellpadding='5' style='border-collapse: collapse; width: 100%; text-align: left; font-size: 0.9em;'>"
            part2 = part2.replace(old_table_start, '<table class="q-table w-100 t-left"><thead>')
            part2 = part2.replace("style='background-color: #f2f2f2;'", "")
            part2 = part2.replace('</th><th>', '</th><th class="w-25">', 1) # 簡單處理寬度
            part2 = part2.replace('</th></tr>', '</th></tr></thead><tbody>')
            part2 = part2.replace('</table>', '</tbody></table>')
            
            # 重新賦值
            q['explanation'][exp_index] = part1
            q['explanation'].insert(exp_index + 1, part2)
            break

# 修正 ID 9 (表格在 index 1)
fix_table_in_explanation(9, 1)
# 修正 ID 132 (表格在 index 4)
fix_table_in_explanation(132, 4)

with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 9, 132 編碼中立修正完成！")
