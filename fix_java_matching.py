import json
import os

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 定義需要修正的題目處理邏輯
def fix_right_field(q):
    if q.get('type') in ['matching', 'multimatching']:
        new_right = []
        for line in q['right']:
            # 1. 處理帶有 ①②③ 的字串，但沒有 | 的情況
            if '①' in line and '|' not in line:
                # 在 ②, ③, ④, ⑤ 前面加上 |
                line = line.replace('②', ' | ②').replace('③', ' | ③').replace('④', ' | ④').replace('⑤', ' | ⑤')
                # 移除重複的空格
                line = ' '.join(line.split())
                line = line.replace(' |', ' |')
            
            # 2. 處理二元配對如 "O", "X"
            if q['id'] in [3, 13, 16, 31, 38, 39, 42, 46, 66, 72] and len(q['right']) > 1:
                # 這種情況通常 left 有多行，right 只有兩行代表選項池
                # 合併為一行以 | 區隔
                combined = ' | '.join(q['right'])
                new_right = [combined]
                break
            
            # 3. 處理特定的池化題目 (ID 5, 12, 15, 18, 23, 62, 68等)
            if q['id'] in [5, 12, 15, 18, 23, 62, 68] and len(q['right']) > 1:
                combined = ' | '.join(q['right'])
                new_right = [combined]
                break

            new_right.append(line)
        
        if new_right:
            q['right'] = new_right

for question in data:
    fix_right_field(question)

# 特殊處理：修正之前 replace 沒蓋到的 A : 前綴
for q in data:
    if q['id'] == 4:
        q['right'] = [
            "①private void | ②public static void | ③private static String | ④public String",
            "①int args[] | ②int args | ③String args[] | ④String arg"
        ]
    if q['id'] == 9:
        q['right'] = [
            "①java.io.* | ②java.util.Scanner",
            "①InputStream stream = System.in | ②Scanner sc = new Scanner(System.in)",
            "①sc.wait() | ②sc.next() | ③sc.mark(8) | ④stream.read()",
            "①sc.wait() | ②sc.close() | ③stream.wait() | ④stream.close()"
        ]
    if q['id'] == 11:
        q['right'] = [
            "①substring(0, 5) | ②subSequence(5, 0) | ③substring(5)",
            "①%n | ②%d | ③%s",
            "①%f | ②%d | ③%c",
            "①count() | ②length() | ③chars()"
        ]
    if q['id'] == 14:
        q['right'] = [
            "①double[] array | ②double array | ③double[length] array",
            "①double max = array[1]; | ②double max = array[0];",
            "①array.size()-1 | ②array.size() | ③array.length-1 | ④array.length",
            "①max != array[i] | ②max < array[i]",
            "①max == array[i]; | ②max = array[i];"
        ]
    if q['id'] == 20:
        q['right'] = [
            "①int i = num; | ②int i == num; | ③int i < num; | ④int i <= num;",
            "①i < 0; | ②i <= 0; | ③i > 0; | ④i >= 0;",
            "①i+ | ②++i | ③--i | ④-i"
        ]
    if q['id'] == 24:
        q['right'] = [
            "①while | ②for | ③do",
            "①++ | ②: | ③; | ④instanceof",
            "①break; | ②goto; | ③continue;"
        ]
    if q['id'] == 25:
        q['right'] = [
            "①== | ②>= | ③<= | ④=>",
            "①== | ②= | ③!= | ④=>",
            "①+= | ②-= | ③++ | ④--"
        ]
    if q['id'] == 71:
        q['right'] = [
            "①Candy candy = new candy(); | ②Candy candy = new Candy();",
            "①isPurchased = true; | ②candy.isPurchased = true;",
            "①candy.overdue; | ②candy.overdue();"
        ]
    if q['id'] == 73:
        q['right'] = [
            "①private | ②protected | ③public | ④static",
            "①bool | ②int | ③String | ④void",
            "①() | ②(bool member) | ③(Group member) | ④(String member)"
        ]
    if q['id'] == 76:
        q['right'] = [
            "①new | ②cir1 | ③Circle | ④Circle() | ⑤Circle(radius)"
        ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Successfully fixed all matching 'right' fields with | delimiter.")
