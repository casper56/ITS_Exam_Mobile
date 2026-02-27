import json

with open('q48.json', 'r', encoding='utf-8') as f:
    q48_data = json.load(f)

json_path = 'www/ITS_Python/questions_ITS_python.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in range(len(data)):
    if data[i]['id'] == 48:
        data[i] = q48_data
        break

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("JSON SYNC SUCCESS")
