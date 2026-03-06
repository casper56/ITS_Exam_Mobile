import os
import glob

# Using double quotes to handle the single quotes inside
polluted_str = "<style>.q-table td { vertical-align: middle; } .header-bg { background: #f8f9fa; font-weight: bold; text-align: center; } .category-title { background: #e2e3e5; font-weight: bold; color: #383d41; } .code-font { font-family: 'Cascadia Code', Consolas, monospace; color: #0056b3; font-size: 13px; }</style>"

# Find all JSON files in the workspace
json_files = glob.glob('**/*.json', recursive=True)

count = 0
for file_path in json_files:
    if 'node_modules' in file_path:
        continue
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if polluted_str in content:
            new_content = content.replace(polluted_str, '')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Cleaned pollution from {file_path}")
            count += 1
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"Total JSON files cleaned: {count}")
