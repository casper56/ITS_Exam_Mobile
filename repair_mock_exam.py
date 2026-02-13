import json
import os
import re

def repair_mock_exam():
    subjects = ["AI900", "AZ900", "Generative_AI", "ITS_AI", "ITS_Database", "ITS_Python", "ITS_softdevelop"]
    
    for sub in subjects:
        dir_path = os.path.join('www', sub)
        html_path = os.path.join(dir_path, 'mock_exam.html')
        
        # Find JSON
        json_files = [f for f in os.listdir(dir_path) if f.startswith('questions_') and f.endswith('.json')]
        if not json_files:
            continue
        
        json_path = os.path.join(dir_path, json_files[0])
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                quiz_data = json.load(f)
            
            if not os.path.exists(html_path):
                print(f"Skipping {sub}: mock_exam.html not found")
                continue
                
            with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            # Find the line const allQuestions = ...;
            # and replace it with the new data
            new_json_str = json.dumps(quiz_data, ensure_ascii=False)
            
            start_marker = 'const allQuestions ='
            end_marker = 'let examQuestions = [];' # This usually follows allQuestions
            
            if start_marker in html_content and end_marker in html_content:
                parts = html_content.split(start_marker)
                # Ensure we only split at the first occurrence of end_marker after start_marker
                rest = parts[1].split(end_marker, 1)
                
                new_content = parts[0] + start_marker + " " + new_json_str + ";\n    " + end_marker + rest[1]
                
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Successfully repaired {sub}/mock_exam.html")
            else:
                print(f"Markers not found in {sub}/mock_exam.html")
                
        except Exception as e:
            print(f"Error repairing {sub}: {e}")

if __name__ == "__main__":
    repair_mock_exam()
