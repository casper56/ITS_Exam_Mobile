import json
import os
import re
import subprocess

def global_cleanup():
    for root, dirs, files in os.walk('www'):
        target_json = None
        for f in files:
            if f.startswith('questions_') and f.endswith('.json'):
                target_json = f
                break
        
        if not target_json: continue
        
        json_path = os.path.join(root, target_json)
        print(f"
Processing {json_path}...")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 1. 移除重複 (根據內容比對)
            seen_texts = {}
            unique_data = []
            removed_count = 0
            
            for q in data:
                # 處理可能是 list 的 question 欄位
                q_text = q['question']
                if isinstance(q_text, list): q_text = "
".join(q_text)
                
                # 標準化內容
                clean = re.sub(r'<[^>]+>|\s+|^\d+[\.\s]*|【.*?】', '', str(q_text))
                
                if clean not in seen_texts:
                    seen_texts[clean] = q['id']
                    unique_data.append(q)
                else:
                    removed_count += 1
            
            if removed_count > 0:
                print(f"  Removed {removed_count} duplicate questions.")
            
            # 2. 重新編號
            for i, q in enumerate(unique_data):
                new_id = i + 1
                q['id'] = new_id
                # 更新題幹編號文字
                if isinstance(q['question'], str):
                    q['question'] = re.sub(r'^\d+\.', f'{new_id}.', q['question'])
            
            # 存回 JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(unique_data, f, ensure_ascii=False, indent=4)
            
            # 3. 執行生成器 (json_to_html.py 或 update_all_generators.py)
            generators = ['update_all_generators.py', 'json_to_html.py', 'gen_balanced_exam.py']
            for gen in generators:
                gen_path = os.path.join(root, gen)
                if os.path.exists(gen_path):
                    print(f"  Running generator: {gen}")
                    # 在該目錄下執行以確保路徑正確
                    subprocess.run(['python', gen], cwd=root, capture_output=True)
                    break
                    
        except Exception as e:
            print(f"  Error processing {json_path}: {e}")

if __name__ == '__main__':
    global_cleanup()
