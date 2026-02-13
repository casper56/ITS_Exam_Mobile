import json
import os
import re
from collections import defaultdict

def scan():
    for root, dirs, files in os.walk('www'):
        for f in files:
            if f.startswith('questions_') and f.endswith('.json'):
                path = os.path.join(root, f)
                print(f"--- Checking {path} ---")
                with open(path, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
                
                m = defaultdict(list)
                for q in data:
                    txt = re.sub(r'<[^>]+>|\s+|^\d+[\.\s]*|【.*?】', '', q['question'])
                    m[txt].append(q['id'])
                
                found = False
                for txt, ids in m.items():
                    if len(ids) > 1:
                        print(f"  Duplicates: {ids}")
                        found = True
                if not found: print("  Clean.")

if __name__ == '__main__': scan()
