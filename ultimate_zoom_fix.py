import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修正 CSS：放寬縮放控制與容器設定
css_patch = """
    #zoom-controls { position: fixed; bottom: 85px; right: 20px; z-index: 10000; display: flex; flex-direction: column; gap: 12px; }
    .zoom-btn { width: 50px; height: 50px; border-radius: 50%; background: rgba(33, 37, 41, 0.85); color: white; border: 1px solid rgba(255,255,255,0.2); font-size: 24px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3); cursor: pointer; user-select: none; }
    #question-container, #question-area { transform-origin: top center; transition: none !important; }
    .matching-wrapper { touch-action: pan-y pinch-zoom; position: relative; margin: 30px 0; padding: 10px; }
"""
# 移除舊的縮放 CSS 並加入新的
content = re.sub(r'/\* 縮放工具樣式 \*/.*?#question-container \{.*?\}', css_patch, content, flags=re.DOTALL)

# 2. 修正 JavaScript：更強大的縮放邏輯
js_patch = """
    window.globalZoom = window.globalZoom || 1.0;
    window.changeZoom = function(delta) {
        window.globalZoom = Math.round((window.globalZoom + delta) * 10) / 10;
        if (window.globalZoom < 0.6) window.globalZoom = 0.6;
        if (window.globalZoom > 2.5) window.globalZoom = 2.5;
        
        // 自動適配不同的容器 ID
        const container = document.getElementById('question-container') || document.getElementById('question-area');
        if (container) {
            container.style.transform = `scale(${window.globalZoom})`;
            if (window.globalZoom > 1) {
                container.style.marginBottom = ((window.globalZoom - 1) * 100) + "%";
            } else {
                container.style.marginBottom = "0";
            }
            // 縮放後重繪連線
            if (window.drawLines) window.drawLines();
        }
    };
"""

# 替換全域縮放邏輯
content = re.sub(r'window\.globalZoom = window\.globalZoom \|\| 1\.0;.*?window\.changeZoom = function\(delta\) \{.*?\}\s*;', js_patch, content, flags=re.DOTALL)

# 3. 修正 renderMatchingQuestion 中的導覽按鈕與縮放同步
# 確保按鈕顯示邏輯正確
content = content.replace("document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';", 
                         "if(document.getElementById('side-btn-prev')) document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Full fix for Zoom and Navigation applied.")
