import os

def patch_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 注入 CSS (使用多行字串)
    css_to_add = """
        /* 縮放工具樣式 */
        #zoom-controls { position: fixed; bottom: 85px; right: 20px; z-index: 10000; display: flex; flex-direction: column; gap: 12px; }
        .zoom-btn { width: 48px; height: 48px; border-radius: 50%; background: rgba(33, 37, 41, 0.85); color: white; border: 1px solid rgba(255,255,255,0.2); font-size: 24px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.25); cursor: pointer; user-select: none; transition: background 0.2s, transform 0.1s; }
        .zoom-btn:active { transform: scale(0.9); background: #000; }
        #question-container { transform-origin: top center; transition: transform 0.1s ease-out; }
    """
    if "/* 縮放工具樣式 */" not in content:
        content = content.replace("</style>", css_to_add + "\n    </style>")

    # 2. 注入 HTML
    html_to_add = """
    <!-- 縮放工具欄 -->
    <div id="zoom-controls">
        <div class="zoom-btn" onclick="changeZoom(0.1)" title="放大題目"><b>+</b></div>
        <div class="zoom-btn" onclick="changeZoom(-0.1)" title="縮小題目"><b>−</b></div>
    </div>
    """
    if 'id="zoom-controls"' not in content:
        content = content.replace('<div class="main-wrapper">', html_to_add + '<div class="main-wrapper">')

    # 3. 注入 JS
    js_to_add = """
    window.globalZoom = 1.0;
    window.changeZoom = function(delta) {
        window.globalZoom = (Math.round((window.globalZoom + delta) * 10) / 10);
        if (window.globalZoom < 0.7) window.globalZoom = 0.7;
        if (window.globalZoom > 2.0) window.globalZoom = 2.0;
        const container = document.getElementById('question-container');
        if (container) {
            container.style.transform = `scale(${window.globalZoom})`;
            container.style.transformOrigin = 'top center';
            if (window.globalZoom > 1) container.style.marginBottom = ((window.globalZoom - 1) * 100) + "%";
            else container.style.marginBottom = "0";
            if (window.drawLines) setTimeout(window.drawLines, 100);
        }
    };
    """
    if 'window.globalZoom = 1.0;' not in content:
        # 在 script 標籤後插入
        content = content.replace('<script>', '<script>\n' + js_to_add)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"SUCCESS: Zoom controls patched to {file_path}")

patch_file('www/ITS_Python/ITS_Python.html')
patch_file('www/ITS_Python/mock_v34.html')
