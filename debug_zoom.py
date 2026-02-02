import glob

files = glob.glob('www/**/*.html', recursive=True)

for file_path in files:
    if 'index.html' in file_path: continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    count = content.count('function adjustZoom')
    print(f"{file_path}: adjustZoom definitions: {count}")
    
    if 'adjustZoom(-2)' in content:
        print(f"  Found adjustZoom(-2)")
    else:
        print(f"  MISSING adjustZoom(-2) or malformed minus sign")
        # Print surrounding context
        idx = content.find('adjustZoom(')
        if idx != -1:
            print(f"  Context: {content[idx:idx+20]}")
