import glob

files = glob.glob('**/json_to_html.py', recursive=True)

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Change (${subIdx+1}) to ${subIdx+1}. in the label
    # Note: in the f-string source, it looks like (${{subIdx+1}}) because of escaping
    old_pattern = '({{{{subIdx+1}}}}) ${{sub}}'
    new_pattern = '${{subIdx+1}}. ${{sub}}'
    
    if old_pattern in content:
        print(f"Updating sub-option labels in {file_path}...")
        new_content = content.replace(old_pattern, new_pattern)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        # Check for another variant if I missed it
        print(f"Pattern not found in {file_path}")
