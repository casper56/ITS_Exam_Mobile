import os
import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 統一縮放變數與邏輯 (移除所有舊的 let globalZoom 定義)
# 我們直接在腳本開頭重新定義一個乾淨、全域且具備容錯能力的縮放函式
new_zoom_script = """
    window.itspyZoom = window.itspyZoom || 1.0;
    window.changeZoom = function(delta) {
        try {
            window.itspyZoom = Math.round((window.itspyZoom + delta) * 10) / 10;
            if (window.itspyZoom < 0.6) window.itspyZoom = 0.6;
            if (window.itspyZoom > 2.5) window.itspyZoom = 2.5;
            
            const container = document.getElementById('question-container') || document.getElementById('question-area');
            if (container) {
                container.style.transform = "scale(" + window.itspyZoom + ")";
                container.style.transformOrigin = "top center";
                container.style.transition = "none";
                
                if (window.itspyZoom > 1) {
                    container.style.marginBottom = ((window.itspyZoom - 1) * 100) + "%";
                } else {
                    container.style.marginBottom = "0";
                }
                // 確保連線在縮放後即時更新
                if (typeof window.drawLines === 'function') {
                    window.drawLines();
                }
            }
        } catch (e) { console.error("Zoom Error:", e); }
    };
"""

# 清除所有舊的 zoom 邏輯
content = re.sub(r'let globalZoom =.*?;', '', content)
content = re.sub(r'window\.globalZoom =.*?;', '', content)
content = re.sub(r'window\.changeZoom = function.*?};', '', content, flags=re.DOTALL)

# 將新的縮放邏輯注入到 script 標籤後
content = content.replace('<script>', '<script>
' + new_zoom_script)

# 2. 修正 CSS，加固按鈕層級，並為配對區加入 pointer-events 最佳化
css_fix = """
        #zoom-controls { position: fixed; bottom: 85px; right: 20px; z-index: 2147483647; display: flex; flex-direction: column; gap: 12px; pointer-events: auto; }
        .zoom-btn { width: 50px; height: 50px; border-radius: 50%; background: #212529; color: white; border: 2px solid #fff; font-size: 24px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0,0,0,0.4); cursor: pointer; user-select: none; touch-action: manipulation; }
        #question-container, #question-area { transform-origin: top center; transition: none !important; position: relative; z-index: 1; }
        .matching-wrapper { touch-action: pan-y pinch-zoom; position: relative; z-index: 2; pointer-events: auto; }
"""
# 替換縮放 CSS
content = re.sub(r'#zoom-controls \{.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'\.zoom-btn \{.*?\}', '', content, flags=re.DOTALL)
content = content.replace('</style>', css_fix + '
    </style>')

# 3. 確保 renderMatchingQuestion 最後呼叫正確的函式
content = content.replace('window.changeZoom(0);', 'window.changeZoom(0);')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Full robust zoom fix applied.")
