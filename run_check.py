import json

def check():
    with open('www/ITS_Python/questions_ITS_python.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    cats = sorted(list(set(q.get('category', 'None') for q in data)))
    with open('cat_check.txt', 'w', encoding='utf-8') as f_out:
        f_out.write('
'.join(cats))

if __name__ == "__main__":
    check()
