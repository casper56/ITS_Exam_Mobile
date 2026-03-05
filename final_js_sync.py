
import json
import os
import glob

def sync_all_data():
    config_path = 'www/config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    for subj in config['subjects']:
        json_file = os.path.join(subj['dir'], subj['json'])
        if not os.path.exists(json_file):
            continue
            
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data_json = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Update JS files if they exist
        js_files = [
            os.path.join(subj['dir'], 'questions_practice.js'),
            os.path.join(subj['dir'], 'questions_data.js')
        ]
        
        for js_file in js_files:
            if os.path.exists(js_file):
                # We need to preserve the "const quizData =" or "const allQuestions =" part
                var_name = "quizData" if "practice" in js_file else "allQuestions"
                with open(js_file, 'w', encoding='utf-8') as f:
                    f.write(f"const {var_name} = {data_json};")
                print(f"Updated {js_file}")

# Execute sync
sync_all_data()
