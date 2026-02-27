import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 加入 RWD 響應式樣式：針對手機縮小間距與字體
rwd_css = """
        /* 手機版 RWD 優化 */
        @media (max-width: 768px) {
            .matching-columns { gap: 30px !important; padding-left: 5px !important; }
            .match-col { min-width: 140px !important; gap: 20px !important; }
            .match-title { font-size: 1rem !important; }
            .match-title-right { padding-left: 45px !important; }
            .match-item { font-size: 0.9rem !important; }
            .match-dot { width: 18px !important; height: 18px !important; margin: 0 10px !important; }
            .match-dot::after { width: 8px !important; height: 8px !important; }
        }
"""
# 插入到 style 標籤末尾
content = content.replace('</style>', rwd_css + '
    </style>')

# 2. 強化手機拖曳時的「防止滾動」邏輯
# 在 handleDragStart 加入阻止預設行為
content = content.replace('isDragging = true;', 'isDragging = true; if(e.cancelable) e.preventDefault();')

# 3. 確保 drawLines 在縮放後立即執行 (且不延遲)
content = content.replace('setTimeout(drawLines, 150);', 'drawLines();')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Mobile RWD and touch-scrolling prevention applied.")
