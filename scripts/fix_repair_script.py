import os

file_path = 'final_clean_repair.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定義絕對穩定的 CSS 換行規則
fixed_css = """        pre, code { 
            white-space: pre-wrap !important; 
            word-wrap: break-word !important; 
            word-break: break-all !important; 
            max-width: 100% !important; 
            background-color: transparent !important; 
            border: none !important; 
            font-size: 1.0rem !important;
            line-height: 1.6 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        pre { overflow-x: hidden !important; }
        code[class*="language-"] { color: inherit; }"""

# 尋找並替換原本的 pre, code 樣式區塊
import re
pattern = r'pre, code \{.*?\}'
content = re.sub(pattern, fixed_css, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully patched CSS rules in final_clean_repair.py")
