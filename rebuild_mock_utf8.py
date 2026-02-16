import json
import os

html_path = 'www/ITS_Python/mock_exam.html'
json_path = 'www/ITS_Python/questions_ITS_python.json'

with open(json_path, 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)
json_str = json.dumps(quiz_data, ensure_ascii=False, indent=2)

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_tag = 'const allQuestions ='
end_tag = '    let examQuestions = [];'

s_idx = content.find(start_tag)
e_idx = content.find(end_tag)

if s_idx != -1 and e_idx != -1:
    before = content[:s_idx]
    after = content[e_idx:]
    
    # 使用 join 拼接避免引號轉義問題
    new_content = "".join([before, "const allQuestions = ", json_str, ";\n", after])
    
    # 進行符號校正
    new_content = new_content.replace('??{', '${')
    new_content = new_content.replace('??${', '✅${')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Rebuild success.")
else:
    print(f"Tags not found: {s_idx}, {e_idx}")
