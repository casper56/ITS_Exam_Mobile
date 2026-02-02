import os
import glob

def fix_viewport_and_zoom(content):
    # Fix Viewport
    content = content.replace('content="width=device-width, initial-scale=1.0"', 
                              'content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=5.0, user-scalable=yes"')
    
    # Check if Zoom CSS is already there
    if '.zoom-controls' not in content:
        zoom_css = """
        .zoom-controls {
            position: fixed;
            bottom: 90px;
            right: 20px;
            z-index: 1100;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .zoom-btn {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: #fff;
            color: #0d6efd;
            border: 1px solid #0d6efd;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            font-size: 1.5rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
            padding: 0;
            line-height: 1;
        }
        .zoom-btn:active {
            background: #0d6efd;
            color: #fff;
            transform: scale(0.95);
        }
        """
        content = content.replace('</style>', zoom_css + '\n    </style>')

    # Check if Zoom HTML is already there
    if 'zoom-controls' not in content:
        zoom_html = """
    <!-- Zoom Controls -->
    <div class="zoom-controls">
        <button class="zoom-btn" onclick="adjustZoom(2)">+</button>
        <button class="zoom-btn" onclick="adjustZoom(-2)">-</button>
    </div>
    """
        content = content.replace('<!-- Scripts -->', zoom_html + '\n<!-- Scripts -->')

    # Check if Zoom JS is already there
    if 'function adjustZoom' not in content:
        zoom_js = """
    // Zoom Functionality
    function adjustZoom(step) {
        const html = document.documentElement;
        let currentSize = parseFloat(window.getComputedStyle(html).fontSize);
        let newSize = currentSize + step;
        if (newSize < 12) newSize = 12;
        if (newSize > 32) newSize = 32;
        html.style.fontSize = newSize + 'px';
    }
    """
        content = content.replace('// Init', zoom_js + '\n    // Init')
        
    return content

def repair_files():
    # Only repair the main HTML files which we know are broken
    files = glob.glob('www/**/*.html', recursive=True)
    
    # Known corrupted sequences to fix (mapping garbled back to Chinese)
    # This is a fallback if we can't regenerate
    replacements = {
        '璅⊥皜祇?': '模擬測驗',
        '憿?”': '題目列表',
        '?桅憿?': '單選題',
        '銴憿?': '複選題',
        '憿?': '題組',
        '漎? 銝?憿?': '⬅️ 上一題',
        '銝?憿??∴?': '下一題 ➡️',
        '??儭??蔭?脣漲': '🗑️ 重置進度',
        '??儭?憿舐內蝑? / 閫??': '👁️ 顯示答案 / 解析',
        '甇?Ⅱ蝑?': '正確答案',
        '閫??': '解析',
        '?怎閫????': '暫無解析。'
    }

    for file_path in files:
        print(f"Repairing {file_path}...")
        # Read with a very loose encoding or bytes to avoid crash
        with open(file_path, 'rb') as f:
            raw = f.read()
        
        # Try to decode from UTF-8 (which might have garbage from previous PowerShell)
        try:
            content = raw.decode('utf-8')
        except:
            # If it fails, it's really messed up, try to read as latin-1 and fix
            content = raw.decode('latin-1')

        # Apply common fixes
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        # Fix the viewport and zoom
        content = fix_viewport_and_zoom(content)
        
        # Write back as clean UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    repair_files()