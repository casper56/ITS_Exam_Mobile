
import json
import os

all_jsons = [
    'www/AI900/questions_AI900.json',
    'www/AZ900/questions_AZ900.json',
    'www/Generative_AI/questions_Generative_AI_Foundations.json',
    'www/ITS_AI/questions_ITS_AI.json',
    'www/ITS_Database/questions_ITS_Database.json',
    'www/ITS_softdevelop/questions_ITS_csharp.json',
    'www/ITS_Python/questions_ITS_python.json'
]

for path in all_jsons:
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated = 0
    for item in data:
        if 'options' in item and any(opt == "Yes|No" for opt in item['options']):
            new_ans = ["Y" if a == "A" else "N" if a == "B" else a for a in item['answer']]
            if new_ans != item['answer']:
                item['answer'] = new_ans
                updated += 1
    
    if updated > 0:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Updated {path}: {updated} items to Y/N.")

print("All JSONs updated.")
