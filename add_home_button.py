import glob
import re

def add_home_button():
    files = glob.glob('www/**/*.html', recursive=True)
    
    for file_path in files:
        if 'index.html' in file_path: continue
        
        print(f"Processing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if button already exists
        if '回首頁' in content:
            print(f"  Skipping {file_path}, button already exists.")
            continue

        # Look for the sidebar footer div
        # We target the opening tag and the start of the button
        target = '<div class="sidebar-footer">\n            <button'
        
        if target in content:
            replacement = '<div class="sidebar-footer">\n            <a href="../index.html" class="btn btn-outline-secondary btn-sm w-100 mb-2">🏠 回首頁</a>\n            <button'
            content = content.replace(target, replacement)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated {file_path}")
        else:
            print(f"  Warning: Sidebar footer pattern not found in {file_path}")

if __name__ == "__main__":
    add_home_button()
