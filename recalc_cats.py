import json
from collections import Counter

file_path = 'www/ITS_softdevelop/questions_ITS_softdevelop.json'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    categories = [item.get('category', 'Unknown') for item in data]
    stats = Counter(categories)
    total = len(data)

    print("Total Questions: " + str(total))
    print("-" * 50)
    for cat, count in sorted(stats.items()):
        percentage = (count / total) * 100
        print(cat + ": " + str(count) + " (" + "{:.1f}".format(percentage) + "%)")
except Exception as e:
    print("Error: " + str(e))
