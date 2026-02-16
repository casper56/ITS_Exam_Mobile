
import json
import os
import shutil

# 定義要轉換的科目目錄
target_dirs = [
    'www/AI900',
    'www/AZ900',
    'www/Generative_AI',
    'www/ITS_AI',
    'www/ITS_Database',
    'www/ITS_softdevelop'
]

def int_to_letter(n):
    # 1 -> A, 2 -> B ...
    return chr(64 + int(n))

def convert_json_answers(file_path):
    # 1. 備份
    backup_path = file_path.replace('.json', '_backup_v3.4.json')
    if not os.path.exists(backup_path):
        shutil.copy(file_path, backup_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        is_changed = False
        new_answer = []
        
        # 判斷是否需要轉換：
        # 1. 題組型 (options 包含 |)
        # 2. 複選題 (type == 'multiple')
        # 3. 雖然是單選，但也想統一轉為字母 (可選，這裡我們先只轉題組與複選以降低風險，或統一全轉)
        
        # 這裡我們採取「全轉」策略，只要是數字就轉字母，以統一格式
        # 但為了保險，我們先只針對 "陣列型答案" 進行轉換
        
        if 'answer' in item and isinstance(item['answer'], list):
            # 檢查選項是否包含 A|B|C 模式，若有則必須轉
            has_pipe_options = 'options' in item and any('|' in str(opt) for opt in item['options'])
            
            # 轉換邏輯
            for ans in item['answer']:
                if isinstance(ans, int):
                    new_answer.append(int_to_letter(ans))
                    is_changed = True
                elif isinstance(ans, str) and ans.isdigit():
                    new_answer.append(int_to_letter(int(ans)))
                    is_changed = True
                else:
                    new_answer.append(ans)
            
            if is_changed:
                item['answer'] = new_answer
                updated_count += 1

    if updated_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[{file_path}] Updated {updated_count} questions to letter format.")
    else:
        print(f"[{file_path}] No changes needed.")

# 執行批次轉換
for d in target_dirs:
    json_files = [f for f in os.listdir(d) if f.startswith('questions_') and f.endswith('.json') and 'backup' not in f]
    for jf in json_files:
        convert_json_answers(os.path.join(d, jf))
