import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修正 CSS 層級與縮放屬性
css_update = """
    #zoom-controls { position: fixed; bottom: 85px; right: 20px; z-index: 999999; display: flex; flex-direction: column; gap: 12px; pointer-events: auto; }
    .zoom-btn { width: 52px; height: 52px; border-radius: 50%; background: #212529; color: white; border: 2px solid #fff; font-size: 26px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5); cursor: pointer; user-select: none; -webkit-tap-highlight-color: transparent; }
    #question-container { transform-origin: top center; transition: none !important; }
    .matching-wrapper { touch-action: pan-y pinch-zoom; position: relative; z-index: 10; }
"""
# 移除所有舊的 zoom 相關 CSS
content = re.sub(r'#zoom-controls\s*\{.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'\.zoom-btn\s*\{.*?\}', '', content, flags=re.DOTALL)
content = content.replace('</style>', css_update + '
    </style>')

# 2. 移除所有混亂的 JS 變數定義，重新注入乾淨的縮放與渲染邏輯
# 我們尋找 <script> 標籤後的內容並進行重置
js_header = """
<script>
    window.itspyZoom = 1.0;
    window.changeZoom = function(delta) {
        window.itspyZoom = Math.round((window.itspyZoom + delta) * 10) / 10;
        if (window.itspyZoom < 0.6) window.itspyZoom = 0.6;
        if (window.itspyZoom > 2.5) window.itspyZoom = 2.5;
        const container = document.getElementById('question-container');
        if (container) {
            container.style.transform = "scale(" + window.itspyZoom + ")";
            if (window.itspyZoom > 1) {
                container.style.marginBottom = ((window.itspyZoom - 1) * 100) + "%";
            } else {
                container.style.marginBottom = "0";
            }
            if (typeof window.drawLines === 'function') window.drawLines();
        }
    };
"""

# 清除所有舊的 window.changeZoom, globalZoom 定義
content = re.sub(r'window\.itspyZoom =.*?;', '', content)
content = re.sub(r'window\.changeZoom = function\(delta\)\s*\{.*?\}\s*;', '', content, flags=re.DOTALL)
content = re.sub(r'let globalZoom =.*?;', '', content)
content = re.sub(r'window\.globalZoom =.*?;', '', content)

# 注入新 Header
content = content.replace('<script>', js_header)

# 3. 修正上一題按鈕偵測 (確保使用 try-catch 防止報錯導致後續腳本失效)
content = content.replace("document.getElementById('side-btn-prev').style.display", "if(document.getElementById('side-btn-prev')) document.getElementById('side-btn-prev').style.display")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Full system recovery and zoom reinforcement completed.")
