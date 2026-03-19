import json
import os

# 1. Update questions JSON
json_path = 'www/ITS_Python/questions_ITS_python.json'
with open(json_path, 'r', encoding='utf-8') as f:
    qs = json.load(f)

# Re-index IDs sequentially
for i, q in enumerate(qs):
    q['id'] = i + 1

# Save updated JSON
os.makedirs('backups', exist_ok=True)
with open('backups/questions_ITS_python_pre_reid.json', 'w', encoding='utf-8') as f:
    json.dump(qs, f, indent=2, ensure_ascii=False)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(qs, f, indent=2, ensure_ascii=False)

print(f"Re-indexed {len(qs)} questions in {json_path}.")

# 2. Update config.json
config_path = 'www/config.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

for subj in config['subjects']:
    if subj['id'] == 'itspy':
        old_cutoff = subj.get('cutoff', 96)
        new_cutoff = old_cutoff + 2
        subj['cutoff'] = new_cutoff
        subj['cutoff_info'] = f"1-{new_cutoff} 為官方版題數"
        print(f"Updated cutoff for itspy from {old_cutoff} to {new_cutoff}.")
        break

with open('backups/config_pre_cutoff.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# 3. Update analysis_bundle.js (since it contains hardcoded text)
analysis_path = 'www/analysis_bundle.js'
try:
    with open(analysis_path, 'r', encoding='utf-8') as f:
        analysis_content = f.read()
    
    # Replace '96' with '98' for itspy where it makes sense
    analysis_content = analysis_content.replace('核心流出題 (1-96)：96 題', '核心流出題 (1-98)：98 題')
    analysis_content = analysis_content.replace('核心 1-96 題', '核心 1-98 題')
    analysis_content = analysis_content.replace('CUTOFF = 96', 'CUTOFF = 98')
    analysis_content = analysis_content.replace('進階補充題 (97-187)', '進階補充題 (99-189)') # total is 189 now maybe?
    
    with open(analysis_path, 'w', encoding='utf-8') as f:
        f.write(analysis_content)
    print(f"Updated {analysis_path}.")
except Exception as e:
    print(f"Could not update {analysis_path}: {e}")

# 4. Update ITS_Python.md
md_path = 'www/ITS_Python/ITS_Python.md'
try:
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    md_content = md_content.replace('核心流出題 (1-96)：96 題', '核心流出題 (1-98)：98 題')
    md_content = md_content.replace('核心 1-96 題', '核心 1-98 題')
    md_content = md_content.replace('CUTOFF = 96', 'CUTOFF = 98')
    md_content = md_content.replace('進階補充題 (97-187)', '進階補充題 (99-189)')
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Updated {md_path}.")
except Exception as e:
    print(f"Could not update {md_path}: {e}")

