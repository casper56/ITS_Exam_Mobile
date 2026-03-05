import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 32:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-32】你要建立名稱為 Car 的 Java 類別用來模擬汽車，此類別必須符合下列需求：",
            "● 任何套件中的所有類別都可將 Car 類別實體化。",
            "● 只有 Car 類別可存取和修改 speed 資料成員。",
            "● 只有和 Car 類別同一套件中的類別才可存取和修改 color 資料成員。",
            "● 每一個已實體化的 Car 物件都可以擁有不同的資料成員。",
            "",
            "請從下列選項中選取正確的程式碼片段對應 A、B、C 位置。",
            "",
            "    ___A___ class Car {",
            "        ___B___ int speed;",
            "        ___C___ String color;",
            "    }</code></pre>"
        ]
        q['left'] = ["A 選項", "B 選項", "C 選項"]
        q['right'] = [
            "①private | ②protected | ③public | ④final | ⑤abstract",
            "①private | ②protected | ③public | ④final | ⑤abstract",
            "①private | ②protected | ③public | ④final | ⑤abstract"
        ]
        q['answer'] = ["C", "A", "B"] # A=public(C), B=private(A), C=protected(B)
        q['explanation'] = [
            "1. 任何套件皆可存取：使用 public。",
            "2. 僅類別內部存取：使用 private。",
            "3. 同一套件成員存取：使用 protected (或預設，但在本選題中 ② 為正確選項)。"
        ]
        q['category'] = "封裝與存取修飾詞"
        break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
