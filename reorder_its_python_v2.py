
import json
import os

json_path = 'www/ITS_Python/questions_ITS_python.json'
with open(json_path, 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Official questions: 1-91 and 183-190
# Supplementary: 92-182

official = [q for q in questions if q['id'] <= 91 or q['id'] >= 183]
supplementary = [q for q in questions if 92 <= q['id'] <= 182]

# Sort official by their current ID (optional but good for order)
official.sort(key=lambda x: x['id'])
# Sort supplementary
supplementary.sort(key=lambda x: x['id'])

new_list = []
# New IDs for official: 1 to len(official)
for i, q in enumerate(official):
    q['id'] = i + 1
    new_list.append(q)

# New IDs for supplementary: len(official) + 1 onwards
start_supp = len(official) + 1
for i, q in enumerate(supplementary):
    q['id'] = start_supp + i
    new_list.append(q)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=4)

print(f"Renumbering complete. Official: 1-{len(official)}, Supp: {len(official)+1}-{len(official)+len(supplementary)}")

# Update config.json
config_path = 'www/config.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

for subj in config['subjects']:
    if subj['id'] == 'itspy':
        subj['cutoff'] = len(official)
        subj['cutoff_info'] = f"1-{len(official)} 為官方版題數"

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

print("Updated config.json cutoff to", len(official))
