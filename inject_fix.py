import os

def fix_dependencies_check(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'import sys' in content and 'reportlab' in content and 'subprocess' in content:
        return

    check_code = """import sys
import subprocess
try:
    import reportlab
    from PIL import Image
except ImportError:
    print('[-] 偵測到缺少必要套件：reportlab 或 Pillow')
    print(f'[!] 正在嘗試為您安裝至目前的 Python 環境 ({sys.executable})...')
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'reportlab', 'Pillow'])
        print('[+] 安裝完成，請重新執行腳本。')
    except Exception as e:
        print(f'[X] 自動安裝失敗: {e}')
        print(f'[!] 請手動執行: {sys.executable} -m pip install reportlab Pillow')
    sys.exit(0)

"""
    new_content = check_code + content
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

for root, dirs, files in os.walk('www'):
    for file in files:
        if file == 'json_to_pdf.py':
            file_path = os.path.join(root, file)
            print(f"Adding dependency auto-fix to {file_path}")
            fix_dependencies_check(file_path)