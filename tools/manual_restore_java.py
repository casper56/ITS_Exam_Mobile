import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    qid = q.get('id')
    
    # 修正 A-01, A-02 的重複嵌套
    if qid in [1, 2, 41, 68, 80]:
        q['question'] = [line.replace('<pre><code><code', '<pre><code').replace('</code></code>', '</code>') for line in q['question']]

    # 修正 A-32
    if qid == 32:
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

    # 修正 A-33
    if qid == 33:
        q['question'] = [
            "<pre><code class=\"language-java\">【A-33】你要建立 Freezer 類別用來模擬冰箱，此類別必須符合下列需求：",
            "● 只允許在同一套件中的類別可存取 Freezer 類別。",
            "● 只允許 Freezer 類別本身存取及修改名稱為 temperature 的資料成員。",
            "● 只允許與 Freezer 類別在同一套件中的類別存取名稱為 minTemperature 的資料成員。",
            "● 確保 minTemperature 資料成員宣告後就無法修改。",
            "A ___ Freezer { B int temperature; C int minTemperature = -15; }</code></pre>"
        ]

    # 修正 A-34
    if qid == 34:
        q['question'] = [
            "<pre><code class=\"language-java\">【A-34】Song 類別包含一個只能從類別內部存取的 isInSinger 方法。isInSinger 方法接受歌手姓名，來和歌手清單進行比較。請選取正確的選項來完成程式碼。",
            "A ___ B ___ isInSinger C {",
            "  for (int i=0; i<numSingers; i++){",
            "    if (singers[i].equals(singer)) D",
            "  } E",
            "}</code></pre>"
        ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("ITS_JAVA JSON A-32/33/34 及重複標籤修復完成。")
