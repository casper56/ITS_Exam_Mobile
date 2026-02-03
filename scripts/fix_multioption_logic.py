import glob
import os
import subprocess
import sys

def fix_multioption_logic():
    # Find all json_to_html.py files
    files = glob.glob('**/json_to_html.py', recursive=True)
    
    # Target block to replace
    # We look for the "if (subIdx === correctSubIdx) {" block in checkSubAnswer
    
    # The indentation in the python file (inside the f-string) looks like:
    #         if (subIdx === correctSubIdx) {{
    #             element.classList.add('correct');
    #         }} else {{
    
    # We will search for this pattern. Note the double curly braces because it's in an f-string in the python file.
    
    search_pattern = """        if (subIdx === correctSubIdx) {{
            element.classList.add('correct');
        }} else {{"""
    
    # We want to inject logic to check if all are correct.
    # We need to escape curly braces for the f-string in the python file.
    # So { becomes {{ and } becomes }}.
    
    new_logic = """        if (subIdx === correctSubIdx) {{
            element.classList.add('correct');
            const totalSub = (quizData[qIdx].quiz || quizData[qIdx].options || []).length;
            const currentCorrect = document.querySelectorAll('.sub-opt-container.correct').length;
            if (currentCorrect === totalSub) {{
                correctSet.add(qIdx);
                incorrectSet.delete(qIdx);
                saveState();
                updateUI();
                document.getElementById('ans-section').style.display = 'block';
            }}
        }} else {{"""

    count = 0
    for file_path in files:
        if 'node_modules' in file_path: continue
        
        print(f"Checking {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if search_pattern in content:
            print(f"  Injecting multioption logic in {file_path}...")
            new_content = content.replace(search_pattern, new_logic)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
        elif 'const totalSub' in content:
             print(f"  Logic already present in {file_path}")
        else:
            print(f"  Pattern not found in {file_path}. Indentation might differ?")
            # Fallback: try to find it with laxer whitespace if strict match fails?
            # Or assume I wrote them consistently. I wrote them with the same function recently.

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
    fix_multioption_logic()
