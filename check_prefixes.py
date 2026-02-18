import json
import re

file_path = 'www/ITS_softdevelop/questions_ITS_csharp.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

patterns = [
    re.compile(r'^[A-E]\.\s+'), # A. space
    re.compile(r'^\([A-E]\)\s*'), # (A)
    re.compile(r'^[A-E]\s+'), # A space
]

results = {p.pattern: 0 for p in patterns}
others = []

for item in data:
    if 'options' in item and isinstance(item['options'], list):
        for opt in item['options']:
            if not isinstance(opt, str): continue
            matched = False
            for p in patterns:
                if p.match(opt):
                    results[p.pattern] += 1
                    matched = True
                    break
            if not matched and re.match(r'^[A-E][.\)]', opt):
                others.append(opt)

print("Matches found:")
for p, count in results.items():
    print(f"  {p}: {count}")
if others:
    print("Others starting with A-E and . or ):")
    for o in others:
        print(f"  {o}")
