import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 修正 A-33 的 right 欄位，確保與 left 長度一致以利 multimatching 渲染
for q in data:
    if q['id'] == 33:
        q['right'] = [
            "①public class | ②class | ③final | ④private | ⑤abstract | ⑥protected",
            "①public class | ②class | ③final | ④private | ⑤abstract | ⑥protected",
            "①public class | ②class | ③final | ④private | ⑤abstract | ⑥protected"
        ]
        break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("A-33 渲染結構已修正。")
