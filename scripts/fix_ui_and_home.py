import glob
import os
import subprocess
import sys

def fix_ui_and_home():
    files = glob.glob('**/json_to_html.py', recursive=True)
    
    # Correct Pattern to find in python f-string: double curly braces
    stats_search = "document.getElementById('progress-stats').innerText = `C:${{correctSet.size}} / W:${{incorrectSet.size}}`;"
    stats_replace = "document.getElementById('progress-stats').innerText = `C:${{correctSet.size}} W:${{incorrectSet.size}} / All:${{quizData.length}}`;"

    header_search = '<h5 class="m-0">題目列表</h5>'
    header_replace = '<a href="../index.html" class="text-decoration-none text-white me-2" title="回首頁">🏠</a><h5 class="m-0">題目列表</h5>'

    count = 0
    for file_path in files:
        if 'node_modules' in file_path: continue
        
        print(f"Processing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # Update Stats
        if stats_search in content:
            content = content.replace(stats_search, stats_replace)
            modified = True
            print("  Updated Stats logic.")
        elif "All:${{quizData.length}}" in content:
            print("  Stats logic already updated.")
        else:
            # Fallback: maybe it's single braces if I messed up earlier or if it's not an f-string?
            # But the file content I wrote definitely had double braces.
            # Let's try searching for single braces just in case, but warn.
            single_search = "document.getElementById('progress-stats').innerText = `C:${correctSet.size} / W:${incorrectSet.size}`;"
            if single_search in content:
                 content = content.replace(single_search, stats_replace.replace('{{', '{').replace('}}', '}'))
                 modified = True
                 print("  Updated Stats logic (found single braces).")
            
        # Add Home Button (if not present)
        if 'title="回首頁">🏠</a>' not in content:
            if header_search in content:
                content = content.replace(header_search, header_replace)
                modified = True
                print("  Added Home Button.")
        else:
            print("  Home Button already present.")

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

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
    fix_ui_and_home()