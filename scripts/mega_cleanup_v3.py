import json
import os
import re
import subprocess

def clean():
    for root, dirs, files in os.walk('www'):
        json_file = next((f for f in files if f.startswith('questions_') and f.endswith('.json')), None)
        if not json_file: continue
        
        path = os.path.join(root, json_file)
        print("Cleaning: " + path)
        
        try:
            with open(path, 'r', encoding='utf-8') as f: data = json.load(f)
            seen = {}
            unique = []
            for q in data:
                txt = q['question']
                if isinstance(txt, list): txt = "".join(txt)
                clean_txt = re.sub(r'<[^>]+>|\s+|^\d+[\.\s]*', '', str(txt))
                if clean_txt not in seen:
                    seen[clean_txt] = True
                    unique.append(q)
            
            for i, q in enumerate(unique):
                new_id = i + 1
                q['id'] = new_id
                if isinstance(q['question'], str):
                    q['question'] = re.sub(r'^\d+\.', str(new_id) + '.', q['question'])
            
            with open(path, 'w', encoding='utf-8') as f: json.dump(unique, f, ensure_ascii=False, indent=4)
            
            # Run generators
            for g in ['update_all_generators.py', 'json_to_html.py']:
                if os.path.exists(os.path.join(root, g)):
                    subprocess.run(['python', g], cwd=root)
                    print("  Updated via " + g)
                    break
        except Exception as e: print("  Failed: " + str(e))

if __name__ == '__main__': clean()
