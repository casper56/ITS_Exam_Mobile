import json
import os

json_path = 'www/ITS_Python/questions_ITS_python.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 26:
        q['answer'] = ["C", "F", "B", "A"]
    elif q['id'] == 48:
        q['answer'] = ["A", "C", "D"]

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("SUCCESS: JSON answers restored to Letter format (A, B, C...).")
