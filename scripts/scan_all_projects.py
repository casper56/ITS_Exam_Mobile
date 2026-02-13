# -*- coding: utf-8 -*-
import json
import os
import re
from collections import defaultdict

def scan_all_subjects():
    base_www = 'www'
    subjects = ['AI900', 'AZ900', 'Generative_AI', 'ITS_AI', 'ITS_Csharp', 'ITS_Database', 'ITS_Python']
    
    for sub in subjects:
        # 尋找 JSON 檔案
        sub_dir = os.path.join(base_www, sub)
        if not os.path.exists(sub_dir): continue
        
        json_files = [f for f in os.listdir(sub_dir) if f.endswith('.json') and f.startswith('questions_')]
        if not json_files: continue
        
        json_path = os.path.join(sub_dir, json_files[0])
        print(f"
[Scanning {sub}] file: {json_files[0]}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
            
        text_map = defaultdict(list)
        for q in questions:
            # 標準化內容比對
            clean = re.sub(r'<[^>]+>', '', q['question'])
            clean = re.sub(r'^\d+[\.\s]*', '', clean)
            clean = re.sub(r'【.*?】', '', clean)
            clean = re.sub(r'\s+', '', clean)
            text_map[clean].append(q['id'])
            
        found_dup = False
        for text, ids in text_map.items():
            if len(ids) > 1:
                print(f"  !!! Found Duplicates: {ids}")
                found_dup = True
        
        if not found_dup:
            print("  ✓ No duplicates.")

if __name__ == "__main__":
    scan_all_subjects()
