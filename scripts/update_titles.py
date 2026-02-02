import glob
import os

def update_titles():
    # 1. 處理首頁
    index_path = 'www/index.html'
    if os.path.exists(index_path):
        print(f"Updating {index_path}...")
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替換主標題
        content = content.replace('ITS 認證模擬測驗', '模擬測驗')
        content = content.replace('ITS 認證模擬測試', '模擬測驗')
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # 2. 處理分頁
    files = glob.glob('www/**/*.html', recursive=True)
    for file_path in files:
        if 'index.html' in file_path:
            # 已經處理過根目錄的，但可能 subfolder 也有 (如果結構重複)
            if file_path == 'www/index.html': continue
        
        print(f"Updating titles in {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替換 ITS Database 為指定中文名
        content = content.replace('ITS Database 模擬測驗', 'ITS 資料庫管理核心能力 模擬測驗')
        content = content.replace('<title>ITS Database 模擬測驗</title>', '<title>ITS 資料庫管理核心能力 模擬測驗</title>')
        
        # 將頁面內的 "ITS XXX 模擬測驗" 統一調整為符合首頁風格 (可選)
        # 這裡根據需求，主要是將 ITS Database 更名
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    update_titles()
