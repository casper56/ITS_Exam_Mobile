import json
import re

def fix_json_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove any remaining Git markers just in case
    content = re.sub(r'<{7,}.*?
', '', content)
    content = re.sub(r'={7,}.*?
', '', content)
    content = re.sub(r'>{7,}.*?
', '', content)
    
    # 2. Fix duplicated category and missing commas
    # This looks for: "category": "..." (no comma) "category": "..."
    # And keeps only the first one while ensuring proper JSON syntax
    content = re.sub(r'("category":\s*"[^"]*")\s*"category":\s*"[^"]*"', r'\1', content)
    
    # 3. Try to load and save to prettify
    try:
        data = json.loads(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Successfully structuralized {file_path}")
        return True
    except Exception as e:
        print(f"Failed to fix JSON structure: {e}")
        # Secondary fallback: find common issues
        return False

fix_json_structure('www/ITS_Python/questions_ITS_python.json')
