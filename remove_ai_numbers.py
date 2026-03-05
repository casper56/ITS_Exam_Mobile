
import json
import os
import re

def remove_leading_numbers(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Pattern to match: <pre><code> followed by numbers and dot/space
    # Also handles cases without pre/code tags just in case
    pattern = re.compile(r'^(<pre><code>)?\d+[.\s、]+')
    
    modified = False
    for item in data:
        if "question" in item and isinstance(item["question"], list) and len(item["question"]) > 0:
            first_line = item["question"][0]
            # Try to remove the number
            new_line = pattern.sub(r'\1', first_line)
            if new_line != first_line:
                item["question"][0] = new_line
                modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Removed numbers from {file_path}")
    else:
        print(f"No numbers found to remove in {file_path}")

# Target files
json_files = [
    'json_backup_test/questions_ITS_AI.json',
    'www/ITS_AI/questions_ITS_AI.json'
]

for jf in json_files:
    if os.path.exists(jf):
        remove_leading_numbers(jf)
