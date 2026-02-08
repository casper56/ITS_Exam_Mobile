# -*- coding: utf-8 -*-
import json
import re
import os

def fix_questions():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'www', 'ITS_Python', 'questions_ITS_python.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    fixed_count = 0

    for q in questions:
        q_id = q['id']
        
        # --- Fix 1: Yes/No List Questions (ID 19, 65, 68, 69, 71, 82, 87, 88) ---
        if q_id in [19, 65, 68, 69, 71, 82, 87, 88]:
            print(f"Fixing ID {q_id} (Yes/No structure)...")
            
            # Using Unicode for "選項" (\u9078\u9805) to avoid encoding issues
            # Matches: "選項 1. text", "選項 A. text", "A. text"
            pattern = r'(?:\u9078\u9805\s*\d+\.|\u9078\u9805\s*[A-Z]\.|[A-Z]\.)\s*([^\n<]+)'
            matches = re.findall(pattern, q['question'])
            
            # Specific manual fixes for complex cases if regex fails
            if q_id == 69 and not matches: 
                # ID 69 text might be formatted differently
                matches = ["計算薪資 (calculate_salary)", "計算獎金 (calculate_bonus)", "計算總額 (calculate_total)"]
            
            if len(matches) < len(q['options']):
                 # Fallback: try splitting by newlines if it looks like a list
                 lines = [line.strip() for line in q['question'].split('<br>') if re.match(r'^\d+\.', line.strip())]
                 if len(lines) == len(q['options']):
                     matches = [re.sub(r'^\d+\.\s*', '', line) for line in lines]

            if len(matches) >= len(q['options']):
                new_options = []
                for i in range(len(q['options'])):
                    text = matches[i].strip()
                    orig_opt = q['options'][i]
                    if 'Yes' in orig_opt or 'True' in orig_opt or 'Correct' in orig_opt:
                        new_options.append(f"{text}|Yes|No")
                    else:
                        new_options.append(f"{text}|{orig_opt}")
                
                q['options'] = new_options
                
                # Truncate question text
                split_marker = '\u9078\u9805' # "選項"
                if split_marker in q['question']:
                    q['question'] = q['question'].split(split_marker)[0].strip()
                
                fixed_count += 1
            else:
                print(f"  [Warn] ID {q_id}: Extracted {len(matches)} items, but expected {len(q['options'])}. Skipping.")

        # --- Fix 2: Length Mismatch (ID 26) ---
        if q_id == 26:
            print(f"Fixing ID {q_id} (Length mismatch)...")
            q['options'] = q['options'][:4]
            fixed_count += 1

        # --- Fix 3: Type Error (ID 108) ---
        if q_id == 108:
            print(f"Fixing ID {q_id} (Type mismatch)...")
            q['type'] = 'multiple'
            fixed_count += 1

        # --- Fix 4: ID 29 (Fill-in formatting) ---
        if q_id == 29:
             print(f"Fixing ID {q_id} (Fill-in descriptions)...")
             q['options'][0] = "選項 1 (檢查 None)|" + q['options'][0]
             q['options'][1] = "選項 2 (檢查 Zero)|" + q['options'][1]
             if '\u9078\u98051' in q['question']:
                 q['question'] = q['question'].split('\u9078\u98051')[0]
             fixed_count += 1

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)
    
    print(f"-" * 30)
    print(f"Total fixed: {fixed_count}")

if __name__ == "__main__":
    fix_questions()