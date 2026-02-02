import glob
import re

def remove_debug_display():
    files = glob.glob('www/**/*.html', recursive=True)
    for file_path in files:
        if 'index.html' in file_path: continue
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the div with id zoom-val-display
        content = re.sub(r'<div id="zoom-val-display".*?</div>', '', content, flags=re.DOTALL)
        
        # Remove updateZoomDisplay() calls and function definition
        content = content.replace('updateZoomDisplay();', '')
        content = re.sub(r'function updateZoomDisplay\(\) \{.*?\}', '', content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    remove_debug_display()
