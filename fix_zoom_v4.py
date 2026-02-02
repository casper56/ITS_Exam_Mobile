import glob
import re

def clean_and_inject_v4():
    files = glob.glob('www/**/*.html', recursive=True)
    
    # New Robust Logic using Global State
    state_based_js = """
    // --- ZOOM LOGIC V4 (Global State) ---
    var _zoomLevel = 16; // Default baseline
    var _zoomInit = false;

    function initZoomState() {
        if (_zoomInit) return;
        try {
            // Try to read initial, otherwise stick to 16
            var style = window.getComputedStyle(document.body, null).getPropertyValue('font-size');
            var val = parseFloat(style);
            if (val && !isNaN(val)) _zoomLevel = val;
        } catch(e) {}
        _zoomInit = true;
        updateZoomDisplay();
    }

    function doZoom(change) {
        initZoomState();
        _zoomLevel += change;
        
        // Safety bounds
        if (_zoomLevel < 10) _zoomLevel = 10;
        if (_zoomLevel > 40) _zoomLevel = 40;
        
        document.documentElement.style.fontSize = _zoomLevel + 'px';
        document.body.style.fontSize = _zoomLevel + 'px';
        
        updateZoomDisplay();
    }
    
    function updateZoomDisplay() {
        var disp = document.getElementById('zoom-val-display');
        if (disp) disp.innerText = _zoomLevel + 'px';
    }
    
    // Auto init
    window.addEventListener('DOMContentLoaded', initZoomState);
    // ------------------------------------
    """

    # HTML with display
    new_html = """
    <!-- Zoom Controls V4 -->
    <div class="zoom-controls">
        <div id="zoom-val-display" style="background:#212529;color:white;padding:2px 6px;border-radius:4px;font-size:12px;margin-bottom:4px;text-align:center;">16px</div>
        <button class="zoom-btn" type="button" onclick="doZoom(2)">+</button>
        <button class="zoom-btn" type="button" onclick="doZoom(-2)">-</button>
    </div>
    """

    for file_path in files:
        if 'index.html' in file_path: continue
        
        print(f"Applying V4 fix to {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Remove ALL previous zoom JS blocks using strict or fuzzy matching
        # We'll just append the new logic at the end of the script tag, 
        # and rely on the new function names 'doZoom' to avoid conflict.
        # But we should try to strip old <div class="zoom-controls">...</div>
        
        # Remove old HTML block
        content = re.sub(r'<div class="zoom-controls">.*?</div>', '', content, flags=re.DOTALL)
        
        # Inject new HTML before script or body end
        if '<!-- Scripts -->' in content:
            content = content.replace('<!-- Scripts -->', new_html + '\n<!-- Scripts -->')
        else:
            content = content.replace('</body>', new_html + '\n</body>')
            
        # Inject new JS
        # We put it right before the end of the script tag
        if '</script>' in content:
            # Find the LAST script tag end
            last_script_idx = content.rfind('</script>')
            if last_script_idx != -1:
                content = content[:last_script_idx] + "\n" + state_based_js + "\n" + content[last_script_idx:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    clean_and_inject_v4()
