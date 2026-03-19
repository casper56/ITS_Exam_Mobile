import json
with open('www/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

for subj in config['subjects']:
    json_path = subj['dir'] + '/' + subj['json']
    try:
        with open(json_path, 'r', encoding='utf-8') as jf:
            qs = json.load(jf)
            total = len(qs)
            supp = sum(1 for q in qs if int(q['id']) > subj['cutoff'])
            off = sum(1 for q in qs if int(q['id']) <= subj['cutoff'])
            print(f"{subj['id']:<10} | Cutoff: {subj['cutoff']:<3} | Total: {total:<4} | Off: {off:<4} | Supp: {supp:<3}")
    except Exception as e:
        print(f"{subj['id']} - Error: {e}")