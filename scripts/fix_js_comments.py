import glob

def fix_js_comments():
    files = glob.glob('www/**/*.html', recursive=True)
    
    replacements = [
        ("# Save Answer", "// Save Answer"),
        ("# Collect all checked", "// Collect all checked"),
        ("# Multiple Choice - Visual Feedback", "// Multiple Choice - Visual Feedback"),
        ("# Restore User Answer", "// Restore User Answer"),
        ("# Single Choice", "// Single Choice"),
        ("# Visuals", "// Visuals"),
        ("# Show correct", "// Show correct"),
        ("# Multiple Choice", "// Multiple Choice"),
        ("# Disable inputs", "// Disable inputs"),
        ("# Show Explanation", "// Show Explanation"),
        ("wrongSet.add(qIdx); # Mark as wrong", "wrongSet.add(qIdx); // Mark as wrong"),
        ("saveState(); # Save wrong set", "saveState(); // Save wrong set"),
        ("wrongSet.add(qIdx); # Mark as wrong if ANY wrong option selected", "wrongSet.add(qIdx); // Mark as wrong if ANY wrong option selected")
    ]
    
    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: continue
        
        print(f"Fixing comments in {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for old, new in replacements:
            content = content.replace(old, new)
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_js_comments()
