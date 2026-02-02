import os
import glob

def inject_zoom_features(content):
    # 1. Inject CSS before </style>
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
    if '.zoom-controls' not in content:
        content = content.replace('</style>', zoom_css + '\n    </style>')

    # 2. Inject HTML Buttons before <!-- Scripts --> or </body>
    zoom_html = """
    <!-- Zoom Controls -->
    <div class="zoom-controls">
        <button class="zoom-btn" onclick="adjustZoom(2)">+</button>
        <button class="zoom-btn" onclick="adjustZoom(-2)">-</button>
    </div>
    """
    if 'class="zoom-controls"' not in content:
        if '<!-- Scripts -->' in content:
            content = content.replace('<!-- Scripts -->', zoom_html + '\n<!-- Scripts -->')
        else:
            content = content.replace('</body>', zoom_html + '\n</body>')

    # 3. Inject JS Logic before // Init or inside <script>
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
    if 'function adjustZoom' not in content:
        if '// Init' in content:
            content = content.replace('// Init', zoom_js + '\n    // Init')
        else:
            # Fallback: append to end of script if // Init is missing
            content = content.replace('</script>\n</body>', zoom_js + '\n</script>\n</body>')

    return content

def repair_files():
    # Target only the quiz html files, not index.html (which is a menu)
    files = glob.glob('www/**/*.html', recursive=True)
    
    for file_path in files:
        if 'index.html' in file_path:
            continue

        print(f"Processing {file_path} for Zoom features...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = inject_zoom_features(content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  -> Zoom features injected.")
        else:
            print(f"  -> Zoom features already present.")

if __name__ == "__main__":
    repair_files()
