import glob

files = [
    'www/Generative_AI/mock_exam.html',
    'www/ITS_AI/mock_exam.html',
    'www/ITS_Database/mock_exam.html',
    'www/ITS_softdevelop/mock_exam.html'
]

target_str = 'let examQuestions = [], userAnswers = {},'
replace_str = 'let examQuestions = [];\n    let userAnswers = {},'

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if target_str in content:
        new_content = content.replace(target_str, replace_str)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed variable declaration in {fpath}")
    else:
        print(f"Target string not found in {fpath}")
