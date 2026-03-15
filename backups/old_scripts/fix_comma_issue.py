import json
import os

file_path = r'E:\workspace\vscode\ITS_Exam_Mobile-main\www\ITS_Python\questions_ITS_python.json'
backup_path = r'E:\workspace\vscode\ITS_Exam_Mobile-main\backups\questions_ITS_python_pre_comma_fix.json'

# Backup first
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def clean_commas(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key.startswith('question'):
                obj[key] = clean_commas(value)
            else:
                clean_commas(value)
    elif isinstance(obj, list):
        return [clean_commas(item) for item in obj]
    elif isinstance(obj, str):
        # Remove leading comma if it exists
        if obj.startswith(','):
            return obj[1:].lstrip()
    return obj

clean_commas(data)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Comma cleanup completed for all question fields.")
