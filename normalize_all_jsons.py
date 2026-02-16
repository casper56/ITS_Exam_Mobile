
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

def int_to_letter(n):
    return chr(64 + int(n))

for path in all_jsons:
    if not os.path.exists(path): continue
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        changed = 0
        for item in data:
            if 'answer' in item and isinstance(item['answer'], list):
                new_ans = []
                for a in item['answer']:
                    if isinstance(a, int):
                        new_ans.append(int_to_letter(a))
                    elif isinstance(a, str) and a.isdigit():
                        new_ans.append(int_to_letter(int(a)))
                    else:
                        new_ans.append(a)
                if new_ans != item['answer']:
                    item['answer'] = new_ans
                    changed += 1
        
        if changed > 0:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Updated {path}: {changed} items.")
    except Exception as e:
        print(f"Failed {path}: {e}")

print("All JSONs normalized to letter format.")
