import glob
import os
import subprocess

def fix_prism_theme():
    # Find all json_to_html.py files
    files = glob.glob('**/json_to_html.py', recursive=True)
    
    # Target string
    old_theme = 'prism-tomorrow.min.css'
    new_theme = 'prism-solarized-light.min.css'
    
    for file_path in files:
        if 'node_modules' in file_path: continue
        
        print(f"Checking {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if old_theme in content:
            print(f"  Updating theme in {file_path}...")
            new_content = content.replace(old_theme, new_theme)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        else:
            print(f"  Theme already updated or not found in {file_path}")

    # Now regenerate the HTML files
    # We need to call each script with its corresponding JSON and HTML
    # Mapping:
    # ITS_Python -> questions_ITS_python.json -> ITS_Python.html
    # ITS_AI -> questions_ITS_AI.json -> ITS_AI.html
    # ITS_Database -> questions_ITS_Database.json -> ITS_Database.html
    # AI900 -> questions_AI900.json -> AI900.html
    # AZ900 -> questions_AZ900.json -> AZ900.html
    # Generative_AI -> questions_Generative_AI_Foundations.json -> Generative_AI.html
    
    # And same for www/
    
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

import sys
if __name__ == "__main__":
    fix_prism_theme()
