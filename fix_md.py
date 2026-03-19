import os

files_to_fix = [
    'www/analysis_bundle.js',
    'www/ITS_Python/ITS_Python.md'
]

for file_path in files_to_fix:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Python 總題數變成 189
    content = content.replace('總題數**：187 題', '總題數**：189 題')
    content = content.replace('確保 187 題 ID', '確保 189 題 ID')
    content = content.replace('(1-187)', '(1-189)')
    content = content.replace('核心流出題 (1-98)**：98 題', '核心流出題 (1-98)**：98 題')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Updated {file_path}")
