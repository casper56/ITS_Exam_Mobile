import json

# 從絕對正確的備份讀取
with open('backups/CLEAN_ORIGINAL_PYTHON.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 106:
        # 取得原始字串
        orig = q['explanation'][0]
        
        # 尋找 <b>標題 的位置
        split_point = orig.find('<b>')
        
        # 第一部分：保留 pre/code 開頭，手動加上結束標籤
        part1 = orig[:split_point].strip()
        if not part1.endswith('</code></pre>'):
            part1 += '</code></pre>'
            
        # 第二部分：從 <b> 開始提取，並清理結尾的 code/pre 標籤
        part2 = orig[split_point:].replace('</code></pre>', '').strip()
        
        # 清理 table 標籤與樣式 (使用 replace 避免手動打字)
        old_table = "<table border='1' cellpadding='5' style='border-collapse: collapse; width: 100%; text-align: left; font-size: 0.9em;'>"
        new_table = '<table class="q-table w-100 t-left"><thead>'
        part2 = part2.replace(old_table, new_table)
        
        part2 = part2.replace("<th style='background-color: #f2f2f2;'>", '<th class="w-25">')
        part2 = part2.replace('</th><th>', '<th class="w-35">', 1)
        part2 = part2.replace('</th><th>', '<th class="w-40">', 1)
        part2 = part2.replace('</th></tr>', '</th></tr></thead><tbody>')
        part2 = part2.replace('</table>', '</tbody></table>')
        
        q['explanation'] = [part1, part2]
        break

# 寫入目標檔案
with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ID 106 編碼中立修正完成！")
