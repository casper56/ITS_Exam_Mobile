import glob
import re

def fix_zoom_v5():
    files = glob.glob('www/**/*.html', recursive=True)
    
    # V5 Logic: HARDCODED INITIAL STATE
    # No reading from DOM to avoid WebView glitches
    state_based_js = """
    # --- ZOOM LOGIC V5 (Hardcoded Init) ---
    var _zoomLevel = 16; // Force start at 16px
    var _zoomInit = false;

    function initZoomState() {
        // Just verify bounds, don't read DOM
        if (_zoomLevel < 12) _zoomLevel = 12;
        updateZoomDisplay();
    }

    function doZoom(change) {
        _zoomLevel += change;
        
        # Safety bounds
        if (_zoomLevel < 10) _zoomLevel = 10;
        if (_zoomLevel > 40) _zoomLevel = 40;
        
        # Apply to both root and body with !important to override Bootstrap
        document.documentElement.style.setProperty('font-size', _zoomLevel + 'px', 'important');
        document.body.style.setProperty('font-size', _zoomLevel + 'px', 'important');
        
        updateZoomDisplay();
    }
    
    function updateZoomDisplay() {
        var disp = document.getElementById('zoom-val-display');
        if (disp) disp.innerText = _zoomLevel + 'px';
    }
    
    # Set initial size on load to match our variable
    window.addEventListener('DOMContentLoaded', function() {
        updateZoomDisplay();
    });
    # ------------------------------------
    """

    for file_path in files:
        if 'index.html' in file_path: continue
        
        print(f"Applying V5 fix to {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace the V4 logic block
        # We search for "ZOOM LOGIC V4" and replace until the end of the block
        # Or simpler: Just replace the JS block again using the function name anchor
        
        # Remove old V4 JS
        content = re.sub(r'// --- ZOOM LOGIC V4.*?// ------------------------------------', '', content, flags=re.DOTALL)
        
        # Inject V5 JS before the last script tag end
        if '</script>' in content:
            last_script_idx = content.rfind('</script>')
            if last_script_idx != -1:
                content = content[:last_script_idx] + "\n" + state_based_js + "\n" + content[last_script_idx:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_zoom_v5()
