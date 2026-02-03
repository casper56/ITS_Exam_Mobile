import glob
import os
import subprocess
import sys

def fix_multiple_choice_logic():
    files = glob.glob('**/json_to_html.py', recursive=True)
    
    # Correct search pattern: No comment line
    search_pattern = """        }} else {{
            if (input.checked) {{
                if (correctIndices.includes(optIdx)) {{
                    element.classList.add('correct');
                    element.classList.remove('incorrect');
                }} else {{
                    element.classList.add('incorrect');
                    element.classList.remove('correct');
                }}
            }} else {{
                element.classList.remove('correct');
                element.classList.remove('incorrect');
            }}
        }}"""

    # Replacement logic
    new_logic = """        }} else {{
            if (input.checked) {{
                if (correctIndices.includes(optIdx)) {{
                    element.classList.add('correct');
                    element.classList.remove('incorrect');
                }} else {{
                    element.classList.add('incorrect');
                    element.classList.remove('correct');
                }}
            }} else {{
                element.classList.remove('correct');
                element.classList.remove('incorrect');
            }}

            // Check overall status for Multiple Choice
            const allOptions = document.querySelectorAll(`input[name="q${{qIdx}}"]`);
            let allCorrect = true;
            let anyWrong = false;

            allOptions.forEach((inp, idx) => {{
                if (inp.checked) {{
                    if (!correctIndices.includes(idx)) {{
                        anyWrong = true; // Selected a wrong one
                        allCorrect = false;
                    }}
                }} else {{
                    if (correctIndices.includes(idx)) {{
                        allCorrect = false; // Missed a correct one
                    }}
                }}
            }});

            if (allCorrect) {{
                correctSet.add(qIdx);
                incorrectSet.delete(qIdx);
                document.getElementById('ans-section').style.display = 'block';
            }} else {{
                correctSet.delete(qIdx);
                if (anyWrong) {{
                     incorrectSet.add(qIdx);
                }}
            }}
            saveState();
            updateUI();
        }}"""

    count = 0
    for file_path in files:
        if 'node_modules' in file_path: continue
        
        print(f"Processing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if search_pattern in content:
            content = content.replace(search_pattern, new_logic)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  Updated Multiple Choice logic.")
            count += 1
        elif "Check overall status for Multiple Choice" in content:
            print("  Logic already present.")
        else:
            print("  Pattern not found.")

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
    fix_multiple_choice_logic()