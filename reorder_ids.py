import json
import os

file_path = 'www/ITS_softdevelop/questions_ITS_softdevelop.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 按原本的 ID 排序，確保順序正確
data.sort(key=lambda x: x['id'])

# 重新分配 ID
for i, item in enumerate(data, 1):
    item['id'] = i

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Renumbered {len(data)} questions in {file_path}")
