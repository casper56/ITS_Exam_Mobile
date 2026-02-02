import glob

def inject_debug_alert():
    files = glob.glob('www/**/*.html', recursive=True)
    
    debug_js = """
    // Zoom Functionality - DEBUG VERSION
    function zoomIn() {
        adjustZoom(2);
    }
    
    function zoomOut() {
        adjustZoom(-2);
    }

    function adjustZoom(step) {
        try {
            const html = document.documentElement;
            // Get computed style
            let style = window.getComputedStyle(html, null).getPropertyValue('font-size');
            let currentSize = parseFloat(style);
            
            // Debug alert
            // alert(`Current: ${currentSize}, Step: ${step}, Type: ${typeof step}`);
            
            if (!currentSize || isNaN(currentSize)) currentSize = 16;
            
            let newSize = currentSize + Number(step);
            
            // Ensure bounds
            if (newSize < 12) newSize = 12;
            if (newSize > 48) newSize = 48; // Increased max for visibility
            
            html.style.fontSize = newSize + 'px';
            
            // Verify
            // setTimeout(() => {
            //    let newStyle = window.getComputedStyle(html, null).getPropertyValue('font-size');
            //    alert(`Applied: ${newSize}px, Read back: ${newStyle}`);
            // }, 100);
            
        } catch (e) {
            alert("Error: " + e.message);
        }
    }
    """
    
    # Actually, let's try a different approach.
    # Maybe 'html' element font-size isn't propagating to 'body' correctly in this WebView
    # or 'rem' units are being used weirdly.
    # Let's set it on BOTH html and body.
    
    stronger_js = """
    // Zoom Functionality - STRONGER VERSION
    function zoomIn() {
        applyZoom(2);
    }
    
    function zoomOut() {
        applyZoom(-2);
    }

    function applyZoom(step) {
        const els = [document.documentElement, document.body];
        
        // Use body as reference if html fails
        let style = window.getComputedStyle(document.body, null).getPropertyValue('font-size');
        let currentSize = parseFloat(style);
        if (!currentSize || isNaN(currentSize)) currentSize = 16;
        
        let newSize = currentSize + Number(step);
        if (newSize < 10) newSize = 10;
        if (newSize > 40) newSize = 40;
        
        els.forEach(el => {
            if(el) el.style.fontSize = newSize + 'px';
        });
    }
    """

    for file_path in files:
        if 'index.html' in file_path: continue
        
        print(f"Injecting stronger zoom logic into {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace the existing JS block
        # We look for the start of the previous function
        import re
        # Regex to find the block from "function zoomIn" down to the closing brace of adjustZoom
        # This is a bit risky with regex, so we'll matching the specific function names we added last time
        
        if "function zoomIn()" in content:
            # Replace the whole block we added last time
            pattern = r"function zoomIn\(\)\s*\{.*?function adjustZoom\(step\)\s*\{.*?}"
            # Use DOTALL to match newlines
            # But python's re.sub with DOTALL and greedy * might eat too much.
            # Let's just append the NEW function names (applyZoom) and change the HTML onclicks.
            # This is safer than trying to delete the old JS perfectly.
            
            content = content.replace("function zoomIn()", "function old_zoomIn()")
            content = content.replace("function zoomOut()", "function old_zoomOut()")
            
            # Append new JS before End of script
            content = content.replace('// Init', stronger_js + '\n    // Init')
            
            # Update HTML onclicks
            content = content.replace('onclick="zoomIn()"', 'onclick="zoomIn()"') # Keeps same name, but we redefined the function above? No, wait.
            
            # Let's overwrite the onclicks to be sure
            content = content.replace('onclick="zoomIn()"', 'onclick="applyZoom(2)"')
            content = content.replace('onclick="zoomOut()"', 'onclick="applyZoom(-2)"')
            
            # Also replace the old adjustZoom calls if any remain
            content = content.replace('onclick="adjustZoom(2)"', 'onclick="applyZoom(2)"')
            content = content.replace('onclick="adjustZoom(-2)"', 'onclick="applyZoom(-2)"')
            
        else:
            print("  Warning: Could not find previous zoom logic to replace.")
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    inject_debug_alert()
