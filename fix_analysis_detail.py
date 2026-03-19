import os

file_path = 'www/analysis_bundle.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace exact numbers based on script output
content = content.replace('**單選題 (Single Choice)**：119 題', '**單選題 (Single Choice)**：117 題')
content = content.replace('**多重下拉/題組 (Multi-option)**：58 題', '**多重下拉/題組 (Multi-option)**：62 題')
content = content.replace('| D2_流程控制與判斷 | 30 | 16.0% | 6 |', '| D2_流程控制與判斷 | 32 | 16.9% | 6 |')

# The original has a line for updating to V3.8. Let's make sure it's accurate and states total 189
content = content.replace('確保 189 題 ID 完美連續 (1-189)', '確保 189 題 ID 完美連續 (1-189)')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Updated JS")

file_path = 'www/ITS_Python/ITS_Python.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('**單選題 (Single Choice)**：119 題', '**單選題 (Single Choice)**：117 題')
content = content.replace('**多重下拉/題組 (Multi-option)**：58 題', '**多重下拉/題組 (Multi-option)**：62 題')
content = content.replace('| D2_流程控制與判斷 | 30 | 16.0% | 6 |', '| D2_流程控制與判斷 | 32 | 16.9% | 6 |')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Updated MD")
