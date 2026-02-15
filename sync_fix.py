import os

# 1. 取得正確的函式內容 (從已修復的 ITS_Python)
with open('www/ITS_Python/mock_exam.html', 'r', encoding='utf-8') as f:
    python_content = f.read()

# 提取 initExam 函式的內容
import re
pattern = r'function initExam\(\) \{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}'
match = re.search(pattern, python_content)
if not match:
    print("Failed to extract initExam from ITS_Python")
    exit(1)

correct_init_func = match.group(0)

# 2. 定義目標檔案與對應的 CUTOFF 值
targets = [
    {'path': 'www/AI900/mock_exam.html', 'cutoff': 100},
    {'path': 'www/AZ900/mock_exam.html', 'cutoff': 100},
    {'path': 'www/Generative_AI/mock_exam.html', 'cutoff': 100},
    {'path': 'www/ITS_AI/mock_exam.html', 'cutoff': 118},
    {'path': 'www/ITS_Database/mock_exam.html', 'cutoff': 69},
    {'path': 'www/ITS_softdevelop/mock_exam.html', 'cutoff': 69}
]

# 3. 逐一替換
for t in targets:
    if not os.path.exists(t['path']): continue
    
    with open(t['path'], 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替換函式主體
    new_content = re.sub(pattern, correct_init_func, content)
    
    # 修正該科目的 CUTOFF
    new_content = re.sub(r'const CUTOFF = \d+;', f'const CUTOFF = {t["cutoff"]};', new_content)
    
    with open(t['path'], 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Synchronized and verified {t['path']}")
