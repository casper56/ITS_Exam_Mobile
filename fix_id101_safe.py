import json

# 從備份讀取
with open('backups/questions_ITS_python_id101_prefix.json.bak', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 101:
        # 合併目前的陣列內容
        full_text = "".join(q['explanation'])
        
        # 尋找分割點
        split_point = full_text.find('<b>')
        
        # 拆分
        part1 = full_text[:split_point].strip()
        if not part1.endswith('</code></pre>'):
            part1 += '</code></pre>'
            
        part2 = full_text[split_point:].replace('</code></pre>', '').strip()
        
        # 樣式清理 (編碼中立)
        old_table = "<table border='1' cellpadding='5' style='border-collapse: collapse; width: 100%; text-align: left; font-size: 0.9em;'>"
        new_table = '<table class="q-table w-100 t-left"><thead>'
        part2 = part2.replace(old_table, new_table)
        
        # 標籤補強與類別
        part2 = part2.replace("style='background-color: #f2f2f2;'", "")
        # 將原本的 th 替換為帶寬度的版本
        part2 = part2.replace('<tr><th', '<tr><th class="w-20"', 1)
        part2 = part2.replace('</th><th', '</th><th class="w-15"', 1)
        part2 = part2.replace('</th><th', '</th><th class="w-20"', 1)
        part2 = part2.replace('</th><th', '</th><th class="w-25"', 1)
        part2 = part2.replace('</th><th', '</th><th class="w-20"', 1)
        
        part2 = part2.replace('</th></tr>', '</th></tr></thead><tbody>')
        part2 = part2.replace('</table>', '</tbody></table>')
        
        q['explanation'] = [part1, part2]
        break

# 寫回
with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 101 編碼中立修正完成！")
