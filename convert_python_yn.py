
import json

file_path = 'www/ITS_Python/questions_ITS_python.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for item in data:
    if 'options' in item and isinstance(item['options'], list):
        # 檢查是否為 Yes|No 類型的題目
        if any(opt == "Yes|No" for opt in item['options']):
            new_answer = []
            for ans in item['answer']:
                if ans == "A":
                    new_answer.append("Y")
                elif ans == "B":
                    new_answer.append("N")
                else:
                    new_answer.append(ans)
            
            if new_answer != item['answer']:
                item['answer'] = new_answer
                updated_count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Updated {updated_count} Yes/No questions in {file_path} to Y/N format.")
