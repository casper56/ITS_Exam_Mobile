import os
import re

def fix_zoom_in_file(file_path):
    if not os.path.exists(file_path):
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix CSS for zoom-controls
    # Ensure z-index is max, and pointer-events is auto
    css_pattern = r'#zoom-controls\s*\{.*?\}'
    new_css = '#zoom-controls { position: fixed; bottom: 85px; right: 20px; z-index: 2147483647; display: flex; flex-direction: column; gap: 12px; pointer-events: auto; }'
    if re.search(css_pattern, content):
        content = re.sub(css_pattern, new_css, content, flags=re.DOTALL)
    
    # Also fix zoom-btn to be more button-like
    btn_css_pattern = r'\.zoom-btn\s*\{.*?\}'
    new_btn_css = '.zoom-btn { width: 50px; height: 50px; border-radius: 50%; background: rgba(33, 37, 41, 0.9); color: white; border: 2px solid rgba(255,255,255,0.5); font-size: 24px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.5); cursor: pointer; user-select: none; -webkit-tap-highlight-color: transparent; }'
    if re.search(btn_css_pattern, content):
        content = re.sub(btn_css_pattern, new_btn_css, content, flags=re.DOTALL)

    # 2. Fix HTML structure (use <button> instead of <div> for better mobile click support)
    html_pattern = r'<div id="zoom-controls">.*?</div>\s*</div>'
    new_html = '''<div id="zoom-controls">
        <button class="zoom-btn" type="button" onclick="changeZoom(0.1)" title="放大題目"><b>+</b></button>
        <button class="zoom-btn" type="button" onclick="changeZoom(-0.1)" title="縮小題目"><b>−</b></button>
    </div>'''
    if '<div id="zoom-controls">' in content:
        content = re.sub(html_pattern, new_html, content, flags=re.DOTALL)

    # 3. Fix JS Logic
    js_pattern = r'window\.globalZoom = 1\.0;.*?window\.changeZoom = function\(delta\)\s*\{.*?\};\s*'
    new_js = '''
    window.globalZoom = 1.0;
    window.changeZoom = function(delta) {
        window.globalZoom = (Math.round((window.globalZoom + delta) * 10) / 10);
        if (window.globalZoom < 0.6) window.globalZoom = 0.6;
        if (window.globalZoom > 2.5) window.globalZoom = 2.5;
        
        // Target both practice container and mock exam area
        const container = document.getElementById('question-container') || document.getElementById('question-area') || document.getElementById('review-area');
        if (container) {
            container.style.transform = "scale(" + window.globalZoom + ")";
            container.style.transformOrigin = "top center";
            container.style.transition = "none";
            
            if (window.globalZoom > 1.0) {
                container.style.marginBottom = ((window.globalZoom - 1.0) * 100) + "%";
            } else {
                container.style.marginBottom = "0";
            }
            if (typeof window.drawLines === "function") {
                window.drawLines();
            }
        }
    };
    '''
    if re.search(js_pattern, content, flags=re.DOTALL):
        content = re.sub(js_pattern, new_js, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_zoom_in_file('www/ITS_Python/ITS_Python.html')
fix_zoom_in_file('www/ITS_Python/mock_v34.html')
print("Applied full robust zoom fix using Python.")
