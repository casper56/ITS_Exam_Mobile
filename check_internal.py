import json

def get_internal_cats(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    stats = {}
    for q in data:
        cat = q.get('category', 'None')
        stats[cat] = stats.get(cat, 0) + 1
    return stats

if __name__ == "__main__":
    # 檢查 Python
    py_cats = get_internal_cats('www/ITS_Python/questions_ITS_python.json')
    print("--- ITS Python Internal Categories ---")
    for c, count in sorted(py_cats.items()):
        print(f"[{c}] : {count} 題")
        
    # 檢查 C# (SoftDevelop)
    cs_cats = get_internal_cats('www/ITS_softdevelop/questions_ITS_csharp.json')
    print("
--- ITS SoftDevelop Internal Categories ---")
    for c, count in sorted(cs_cats.items()):
        print(f"[{c}] : {count} 題")
