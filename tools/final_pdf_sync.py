import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    qid = q.get('id')
    
    # 修正被重複嵌套的標籤 (A-01, A-02, B-01, B-28, B-40)
    if qid in [1, 2, 41, 68, 80]:
        q['question'] = [line.replace('<pre><code><code', '<pre><code').replace('</code></code>', '</code>') for line in q['question']]

    # A-32: 完全復刻 PDF A-14 頁
    if qid == 32:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-32】你要建立名稱為 Car 的 Java 類別用來模擬汽車，此類別必須符合下列需求：",
            "● 任何套件中的所有類別都可將 Car 類別實體化。",
            "● 只有 Car 類別可存取和修改 speed 資料成員。",
            "● 只有和 Car 類別同一套件中的類別才可存取和修改 color 資料成員。",
            "● 每一個已實體化的 Car 物件都可以擁有不同的資料成員。",
            "",
            "    ___A___ class Car {",
            "        ___B___ int speed;",
            "        ___C___ String color;",
            "    }</code></pre>"
        ]
        q['left'] = ["A 選項 (class)", "B 選項 (speed)", "C 選項 (color)"]
        # PDF 選項順序：①private ②protected ③public ④final ⑤abstract
        q['right'] = [
            "①private | ②protected | ③public | ④final | ⑤abstract",
            "①private | ②protected | ③public | ④final | ⑤abstract",
            "①private | ②protected | ③public | ④final | ⑤abstract"
        ]
        q['answer'] = ["C", "A", "B"] # A=public(3), B=private(1), C=protected(2)

    # A-33: 完全復刻 PDF A-14/15 頁
    if qid == 33:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-33】你要建立 Freezer 類別用來模擬冰箱，此類別必須符合下列需求：",
            "● 只允許在同一套件中的類別可存取 Freezer 類別。",
            "● 只允許 Freezer 類別本身存取及修改名稱為 temperature 的資料成員。",
            "● 只允許與 Freezer 類別在同一套件中的類別存取名稱為 minTemperature 的資料成員。",
            "● 確保 minTemperature 資料成員宣告後就無法修改。",
            "",
            "    ___A___ Freezer {",
            "        ___B___ int temperature;",
            "        ___C___ int minTemperature = -15;",
            "    }</code></pre>"
        ]
        q['left'] = ["A 選項 (class)", "B 選項 (temp)", "C 選項 (minTemp)"]
        # PDF 選項順序：①public class ②class ③final ④private ⑤abstract
        q['right'] = [
            "①public class | ②class | ③final | ④private | ⑤abstract",
            "①public class | ②class | ③final | ④private | ⑤abstract",
            "①public class | ②class | ③final | ④private | ⑤abstract"
        ]
        q['answer'] = ["B", "D", "C"] # A=class(2), B=private(4), C=final(3)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("ITS_JAVA JSON A-32/33 已依照官方 PDF 完成終極修正。")
