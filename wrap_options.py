import json
import re
import os

FILE_PATH = 'www/ITS_Python/questions_ITS_python.json'

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_and_wrap(s):
    if not isinstance(s, str):
        return s
    
    # Check if the string is already fully wrapped in <code class="language-python">
    # If it has <code>...</code> or similar, we should probably standardize it.
    original_s = s
    
    # Strip whitespace
    s = s.strip()
    
    # If it is already exactly wrapped, maybe we can skip or re-wrap.
    # To be safe, let's remove existing <code> tags at the VERY beginning and end.
    # But only if they are balancing. Let's do a simple regex strip of leading/trailing code/pre tags.
    s = re.sub(r'^<pre>', '', s).strip()
    s = re.sub(r'</pre>$', '', s).strip()
    
    # Remove leading <code...>
    s = re.sub(r'^<code[^>]*>', '', s).strip()
    # Remove trailing </code>
    s = re.sub(r'</code>$', '', s).strip()
    
    # Now wrap it
    # We will wrap it with <code class="language-python">...</code>
    return f'<code class="language-python">{s}</code>'

count = 0
for q in data:
    if 'options' in q and isinstance(q['options'], list):
        new_options = []
        changed = False
        for opt in q['options']:
            if isinstance(opt, list):
                # Array of strings
                new_opt = [clean_and_wrap(x) for x in opt]
                if new_opt != opt:
                    changed = True
                new_options.append(new_opt)
            elif isinstance(opt, str):
                new_opt = clean_and_wrap(opt)
                if new_opt != opt:
                    changed = True
                new_options.append(new_opt)
            else:
                new_options.append(opt)
        
        if changed:
            q['options'] = new_options
            count += 1

print(f"Updated options in {count} questions.")

# Save backup
backup_path = 'backups/questions_ITS_python_pre_code_wrap.json'
os.makedirs('backups', exist_ok=True)
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Backup saved to {backup_path}")

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Successfully updated {FILE_PATH}")
