import json
import os

file_path = r'E:\workspace\vscode\ITS_Exam_Mobile-main\www\ITS_Python\questions_ITS_python.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_leading_comma(text):
    if isinstance(text, str) and text.startswith(','):
        return text[1:].lstrip()
    return text

modified_count = 0
for item in data:
    for key in ['questionA', 'questionB', 'questionC', 'questionD']:
        if key in item:
            content = item[key]
            if isinstance(content, list):
                if len(content) > 0:
                    new_val = clean_leading_comma(content[0])
                    if new_val != content[0]:
                        content[0] = new_val
                        modified_count += 1
            elif isinstance(content, str):
                new_val = clean_leading_comma(content)
                if new_val != content:
                    item[key] = new_val
                    modified_count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Cleanup completed. Modified {modified_count} fields.")
