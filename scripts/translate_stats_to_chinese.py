import glob
import os
import subprocess
import sys

def translate_stats():
    files = glob.glob('**/json_to_html.py', recursive=True)
    
    # Target: The line we just added in the previous step
    # In the python file, it looks like:
    # document.getElementById('progress-stats').innerText = `C:${{correctSet.size}} W:${{incorrectSet.size}} / All:${{quizData.length}}`;
    
    search_pattern = "document.getElementById('progress-stats').innerText = `C:${{correctSet.size}} W:${{incorrectSet.size}} / All:${{quizData.length}}`;"
    
    # Replacement with Chinese
    replace_pattern = "document.getElementById('progress-stats').innerText = `答對:${{correctSet.size}} 答錯:${{incorrectSet.size}} / 共:${{quizData.length}}`;"

    count = 0
    for file_path in files:
        if 'node_modules' in file_path: continue
        
        print(f"Processing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if search_pattern in content:
            content = content.replace(search_pattern, replace_pattern)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  Translated stats to Chinese.")
            count += 1
        elif "答對:${{correctSet.size}}" in content:
            print("  Already translated.")
        else:
            print("  Pattern not found. Checking for variations...")
            # Debug: print a snippet if not found?
            pass

    print(f"Updated {count} files.")

    # Regenerate HTMLs
    base_dirs = ['.', 'www']
    modules = {
        'ITS_Python': 'questions_ITS_python.json',
        'ITS_AI': 'questions_ITS_AI.json',
        'ITS_Database': 'questions_ITS_Database.json',
        'AI900': 'questions_AI900.json',
        'AZ900': 'questions_AZ900.json',
        'Generative_AI': 'questions_Generative_AI_Foundations.json'
    }
    
    for base in base_dirs:
        for module, json_name in modules.items():
            script_path = os.path.join(base, module, 'json_to_html.py')
            json_path = os.path.join(base, module, json_name)
            html_path = os.path.join(base, module, f"{module}.html")
            
            if os.path.exists(script_path) and os.path.exists(json_path):
                print(f"Regenerating {html_path}...")
                cmd = [sys.executable, script_path, json_path, html_path]
                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running {script_path}: {e}")

if __name__ == "__main__":
    translate_stats()
