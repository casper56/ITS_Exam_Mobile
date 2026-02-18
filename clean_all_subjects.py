import json
import re
import os

# 待處理的檔案清單
target_files = [
    'www/AI900/questions_AI900.json',
    'www/AZ900/questions_AZ900.json',
    'www/Generative_AI/questions_Generative_AI_Foundations.json',
    'www/ITS_AI/questions_ITS_AI.json',
    'www/ITS_Database/questions_ITS_Database.json'
]

pattern = re.compile(r'^[A-Z]\.\s+')

for file_path in target_files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} (not found)")
        continue
    
    # 建立備份
    backup_path = f"backups/{os.path.basename(file_path)}.bak"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 寫入備份
        with open(backup_path, 'w', encoding='utf-8') as f_bak:
            json.dump(data, f_bak, ensure_ascii=False, indent=4)
            
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
            
        print(f"Processed {file_path}: modified {modified_count} options. Backup: {backup_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
