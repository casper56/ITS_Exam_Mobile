import glob

def fix_zoom_logic():
    files = glob.glob('www/**/*.html', recursive=True)
    
    new_js = """
    // Zoom Functionality
    function zoomIn() {
        adjustZoom(2);
    }
    
    function zoomOut() {
        adjustZoom(-2);
    }

    function adjustZoom(step) {
        const html = document.documentElement;
        let style = window.getComputedStyle(html, null).getPropertyValue('font-size');
        let currentSize = parseFloat(style);
        if (!currentSize || isNaN(currentSize)) currentSize = 16;
        
        let newSize = currentSize + step;
        if (newSize < 12) newSize = 12;
        if (newSize > 32) newSize = 32;
        html.style.fontSize = newSize + 'px';
    }
    """

    new_html = """
    <!-- Zoom Controls -->
    <div class="zoom-controls">
        <button class="zoom-btn" type="button" onclick="zoomIn()">+</button>
        <button class="zoom-btn" type="button" onclick="zoomOut()">-</button>
    </div>
    """

    for file_path in files:
        if 'index.html' in file_path: continue
        
        print(f"Updating zoom logic in {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace the old JS
        # We look for the start of the old function
        start_marker = "// Zoom Functionality"
        end_marker = "// Init"
        
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            # Replace the block
            content = content[:start_idx] + new_js + "\n    " + content[end_idx:]
        else:
            print("  Could not find JS block to replace.")

        # Replace the old HTML
        # We'll use regex or simple string replacement for the div block
        import re
        content = re.sub(r'<div class="zoom-controls">.*?</div>', new_html, content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_zoom_logic()
