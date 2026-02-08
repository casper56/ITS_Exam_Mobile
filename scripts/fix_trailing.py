import json

def fix_trailing_tags():
    path = 'www/ITS_Python/questions_ITS_python.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    bad_tag = '<pre><code class="language-python">'
    
    for item in data:
        if 'question' in item:
            q = item['question']
            if q.endswith(bad_tag):
                item['question'] = q[:-len(bad_tag)]
                count += 1
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Fixed {count} questions with trailing tags.")

fix_trailing_tags()
