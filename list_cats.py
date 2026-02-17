
import json
from collections import Counter

file_path = r'www\ITS_softdevelop\questions_ITS_csharp.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

stats = Counter()
for item in data:
    stats[item.get('category', 'None')] += 1

for cat, count in stats.items():
    print(f"{cat}: {count}")
