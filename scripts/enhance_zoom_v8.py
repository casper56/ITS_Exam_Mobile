import glob
import re

def enhance_zoom_v8():
    files = glob.glob('www/**/*.html', recursive=True)
    
    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: 
            # 處理主頁 index.html 的 viewport
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # 允許縮放: user-scalable=yes, maximum-scale=10.0
            content = content.replace('maximum-scale=5.0', 'maximum-scale=10.0')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            continue
        
        print(f"Enhancing zoom in {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. 修改 Viewport 以支援雙指縮放
        # 原本: maximum-scale=5.0, user-scalable=yes (這已經允許了，但可能範圍不夠)
        # 我們將其放寬到 10.0
        content = content.replace('maximum-scale=5.0', 'maximum-scale=10.0')

        # 2. 修改 JS Zoom 邏輯 (降低下限)
        # 原本: if (_zoomLevel < 10) _zoomLevel = 10;
        # 改為: if (_zoomLevel < 8) _zoomLevel = 8;
        content = content.replace('if (_zoomLevel < 10) _zoomLevel = 10;', 'if (_zoomLevel < 8) _zoomLevel = 8;')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    enhance_zoom_v8()
