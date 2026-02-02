import glob
import re

def refine_ui_v5():
    files = glob.glob('www/**/*.html', recursive=True)
    
    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: continue
        
        print(f"Refining UI in {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. 移除 CSS 中的 .q-node.active 樣式
        content = re.sub(r'\.q-node\.active \{.*?\}', '', content, flags=re.DOTALL)

        # 2. 修改 updateUI 邏輯，移除當前題目的藍色框線與縮放
        content = re.sub(r'if \(i === currentIndex\) \{.*?\}', '', content, flags=re.DOTALL)
        
        # 移除舊版的 .classList.add('active')
        content = content.replace("if (i === currentIndex) node.classList.add('active');", "")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    refine_ui_v5()
