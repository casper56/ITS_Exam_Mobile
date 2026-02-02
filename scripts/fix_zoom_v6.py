import glob
import re

def fix_zoom_v6():
    files = glob.glob('www/**/*.html', recursive=True)
    
    # V6 Logic: FORCE SYNC ON LOAD
    state_based_js = """
    // --- ZOOM LOGIC V6 (Force Sync) ---
    var _zoomLevel = 16; // We decide this is the standard
    
    function doZoom(change) {
        _zoomLevel += change;
        
        // Safety bounds
        if (_zoomLevel < 10) _zoomLevel = 10;
        if (_zoomLevel > 40) _zoomLevel = 40;
        
        applyZoom();
    }
    
    function applyZoom() {
        // Apply to both root and body with !important
        document.documentElement.style.setProperty('font-size', _zoomLevel + 'px', 'important');
        document.body.style.setProperty('font-size', _zoomLevel + 'px', 'important');
        
        // Update display tag
        var disp = document.getElementById('zoom-val-display');
        if (disp) disp.innerText = _zoomLevel + 'px';
    }
    
    // FORCE SYNC ON LOAD
    // This ensures what the user sees MATCHES our variable
    window.addEventListener('DOMContentLoaded', function() {
        applyZoom(); // Force font to 16px immediately
    });
    // ------------------------------------
    """

    for file_path in files:
        if 'index.html' in file_path: continue
        
        print(f"Applying V6 fix to {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove old V5 JS
        content = re.sub(r'// --- ZOOM LOGIC V5.*?// ------------------------------------', '', content, flags=re.DOTALL)
        
        # Remove BROKEN V6 JS (with # comments)
        content = re.sub(r'# --- ZOOM LOGIC V6.*?# ------------------------------------', '', content, flags=re.DOTALL)
        
        # Remove CORRECT V6 JS (if already there, to avoid duplicates)
        content = re.sub(r'// --- ZOOM LOGIC V6.*?// ------------------------------------', '', content, flags=re.DOTALL)
        
        # Clean up empty lines left by removals (optional but nice)
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        # Inject V6 JS before the last script tag end
        
        # Inject V6 JS before the last script tag end
        if '</script>' in content:
            last_script_idx = content.rfind('</script>')
            if last_script_idx != -1:
                content = content[:last_script_idx] + "\n" + state_based_js + "\n" + content[last_script_idx:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_zoom_v6()
