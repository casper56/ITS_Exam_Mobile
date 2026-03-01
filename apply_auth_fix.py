import os
import re

def fix_html_auth(file_path, base_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 移除任何舊的驗證腳本
    content = re.sub(r'<script>\s*if\s*\(localStorage\.getItem\([\'"]isLoggedIn[\'"]\)\s*!==\s*[\'"]true[\'"]\)\s*\{.*?\}\s*</script>', '', content, flags=re.DOTALL)

    # 插入新的攔截腳本 (在 <html lang="zh-TW"> 之後)
    auth_script = f"""
<script>
    if (localStorage.getItem('isLoggedIn') !== 'true') {{
        window.location.href = '{base_path}index.html';
    }}
</script>"""
    
    if '<html lang="zh-TW">' in content:
        content = content.replace('<html lang="zh-TW">', f'<html lang="zh-TW">{auth_script}')
    elif '<html>' in content:
        content = content.replace('<html>', f'<html>{auth_script}')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed Auth: {file_path}")

# 二級目錄
files2 = [
    "www/ITS_Python/ITS_Python.html",
    "www/ITS_Python/mock_v34.html",
    "www/ITS_softdevelop/ITS_softdevelop.html",
    "www/ITS_softdevelop/mock_v34.html",
    "www/ITS_Database/ITS_Database.html",
    "www/ITS_Database/mock_v34.html",
    "www/ITS_AI/ITS_AI.html",
    "www/ITS_AI/mock_v34.html",
    "www/AI900/AI900.html",
    "www/AI900/mock_v34.html",
    "www/AZ900/AZ900.html",
    "www/AZ900/mock_v34.html",
    "www/Generative_AI/Generative_AI.html",
    "www/Generative_AI/mock_v34.html",
    "www/Generative_AI/Generative_AI_Foundations.html",
    "www/ITS_Python/mock_exam.html"
]

# 一級目錄
files1 = [
    "www/AI900_TECH.html",
    "www/AZ900_TECH.html",
    "www/Generative_AI_TECH.html",
    "www/ITS_AI_TECH.html",
    "www/ITS_DATABASE_TECH.html",
    "www/ITS_Python_TECH.html",
    "www/ITS_SOFTDEVELOP.html"
]

for f in files2:
    fix_html_auth(f, '../../')

for f in files1:
    fix_html_auth(f, '../')
