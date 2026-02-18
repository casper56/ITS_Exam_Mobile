import json
import re
import os

file_path = 'www/ITS_softdevelop/questions_ITS_csharp.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Pattern: A letter A-E followed by a dot and at least one space
# Also handle (A) pattern just in case it's what they mean, but strictly A. first.
# User said A.+"space"
pattern = re.compile(r'^[A-E]\.\s+')

modified_count = 0

for item in data:
    if 'options' in item and isinstance(item['options'], list):
        new_options = []
        for opt in item['options']:
            if isinstance(opt, str):
                new_opt = pattern.sub('', opt)
                if new_opt != opt:
                    modified_count += 1
                new_options.append(new_opt)
            else:
                new_options.append(opt)
        item['options'] = new_options

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Modified {modified_count} options in {file_path}")
