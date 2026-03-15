import re
import json

html_files = {
    r'E:\workspace\vscode\ITS_Exam_Mobile-main\www\ITS_JAVA\ITS_JAVA.html': 'const quizData = ',
    r'E:\workspace\vscode\ITS_Exam_Mobile-main\www\ITS_JAVA\mock_v34.html': 'const allQuestions = '
}

with open(r'E:\workspace\vscode\ITS_Exam_Mobile-main\www\ITS_JAVA\questions_ITS_JAVA.json', 'r', encoding='utf-8') as f:
    json_data = f.read().strip()

for fpath, var_decl in html_files.items():
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        start_idx = content.find(var_decl)
        if start_idx == -1:
            print(f"{var_decl} not found in {fpath}")
            continue
            
        start_array = content.find('[', start_idx)
        
        bracket_count = 0
        end_idx = -1
        in_string = False
        escape = False
        
        for i in range(start_array, len(content)):
            char = content[i]
            if escape:
                escape = False
                continue
            if char == '\\':
                escape = True
                continue
            if char == '"':
                in_string = not in_string
                continue
            
            if not in_string:
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        end_idx = i + 1
                        break
        
        if end_idx != -1:
            new_content = content[:start_array] + json_data + content[end_idx:]
            
            new_content = re.sub(r'const\s+CUTOFF\s*=\s*\d+;', 'const CUTOFF = 78;', new_content)
            new_content = re.sub(r'obj\.id\s*>\s*\d+', 'obj.id > 78', new_content)
            new_content = re.sub(r'代表\s*1-\d+\s*題', '代表 1-78 題', new_content)
            new_content = re.sub(r'1\s*/\s*80', '1 / 78', new_content)
            new_content = re.sub(r'1\s*-\s*80', '1-78', new_content)
            
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Successfully updated {fpath}")
        else:
            print(f"Could not find end of array in {fpath}")
            
    except Exception as e:
        print(f"Error processing {fpath}: {e}")
