import json
import os
import re

def sync_data(json_file, target_file, var_name):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data_json = json.dumps(data, indent=2, ensure_ascii=False)
    
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use a simpler replacement strategy to avoid regex complexity
    start_marker = f'const {var_name} = ['
    if start_marker not in content:
        start_marker = f'{var_name} = ['
    
    if start_marker in content:
        # Find the end of the array
        start_idx = content.find(start_marker)
        # Assuming the array ends with ]; and is followed by some JS
        # This is a bit risky but common in these files
        end_marker = '];'
        end_idx = content.find(end_marker, start_idx)
        
        if end_idx != -1:
            new_content = content[:start_idx] + f'const {var_name} = {data_json};' + content[end_idx + 2:]
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {var_name} in {target_file}")
        else:
            print(f"End marker not found for {var_name} in {target_file}")
    else:
        print(f"Start marker {start_marker} not found in {target_file}")

# Paths
json_src = 'www/ITS_AI/questions_ITS_AI.json'

# Update ITS_AI.html (quizData)
sync_data(json_src, 'www/ITS_AI/ITS_AI.html', 'quizData')

# Update mock_v34.html (allQuestions)
sync_data(json_src, 'www/ITS_AI/mock_v34.html', 'allQuestions')

# Update questions_practice.js
if os.path.exists('www/ITS_AI/questions_practice.js'):
    with open(json_src, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data_json = json.dumps(data, indent=2, ensure_ascii=False)
    with open('www/ITS_AI/questions_practice.js', 'w', encoding='utf-8') as f:
        f.write(f"const quizData = {data_json};")
    print("Updated questions_practice.js")
