import json
import os

json_path = 'www/ITS_Python/questions_ITS_python.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 26:
        q['answer'] = [3, 6, 2, 1] # 1基礎：C, F, B, A
    elif q['id'] == 48:
        q['answer'] = [1, 3, 4]    # 1基礎：A, C, D

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("SUCCESS: JSON answers fixed to 1-based indexing.")
