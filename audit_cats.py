import json
import random

def audit_categories(file_path, subject_name):
    print(f"\n===== Category Audit: {subject_name} =====")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cats = {}
    for q in data:
        cat = q.get('category', 'Uncategorized')
        if cat not in cats:
            cats[cat] = []
        cats[cat].append(q)
    
    sorted_cats = sorted(cats.keys())
    for cat in sorted_cats:
        items = cats[cat]
        print(f"\n--- {cat} (Total: {len(items)}) ---")
        samples = random.sample(items, min(3, len(items)))
        for q in samples:
            clean_q = q['question'].replace('<pre>', '').replace('<code>', '').replace('</code>', '').replace('</pre>', '').replace('<br>', '').replace('<br/>', '')
            clean_q = ' '.join(clean_q.split())
            print(f"  ID {q['id']}: {clean_q[:120]}...")

if __name__ == "__main__":
    audit_categories('www/ITS_softdevelop/questions_ITS_csharp.json', 'ITS Software Development')
    audit_categories('www/ITS_Python/questions_ITS_python.json', 'ITS Python Programming')
