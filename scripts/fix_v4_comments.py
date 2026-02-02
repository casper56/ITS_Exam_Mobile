import glob

def fix_v4_comments():
    files = glob.glob('www/**/*.html', recursive=True)
    
    replacements = [
        ("# Complex Types", "// Complex Types"),
        ("# Check if Quiz", "// Check if Quiz"),
        ("# Quiz Restore", "// Quiz Restore"),
        ("# Disable", "// Disable")
    ]
    
    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: continue
        
        print(f"Fixing V4 comments in {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for old, new in replacements:
            content = content.replace(old, new)
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_v4_comments()
