import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

fixes = {
    27: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-27】你要建立 Test 類別來模擬學校考試，此類別必須符合下列需求：",
            "● 不用將 Test 類別實體化，就可呼叫 setMaxItems 方法。",
            "● 只有和 Test 類別在同一套件中的類別可呼叫 setItems 方法。",
            "● 只有和 Test 類別在同一套件中的類別可呼叫名稱為 setPassScore 的執行個體方法。",
            "請從下列選取正確的選項來完成程式碼。",
            "A ___ void setItems (int num){ }",
            "B ___ void setPassScore (int score){ }</code></pre>"
        ],
        "left": ["A 位置 (setItems)", "B 位置 (setPassScore)"],
        "right": ["①protected | ②private | ③static | ④public"],
        "answer": ["A", "A"], # protected (A), protected (A)
        "explanation": ["1. 同一套件存取應使用 protected。2. 不需實體化應使用 static。"],
        "category": "存取修飾詞"
    },
    28: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-28】你在撰寫名稱為 account 的 Java 類別，此類別具備下列方法：",
            "● 不用將 account 類別實體化，就能從任何程式碼呼叫 showItems 方法。",
            "● 僅有同一套件中的類別，以及任何套件中 account 類別的子類別可以存取名稱為 newAccount 的方法。",
            "請選擇適當的程式碼片段填至對應位置，以完成程式碼。",
            "A ___ B ___ void showItems () { ... }",
            "C ___ void newAccount(String[] items) { ... }"
        ],
        "left": ["A 位置", "B 位置", "C 位置"],
        "right": ["①private | ②final | ③protected | ④public | ⑤static"],
        "answer": ["D", "E", "C"], # public (D), static (E), protected (C)
        "explanation": ["1. 任何程式碼呼叫為 public。2. 不需實體化為 static。3. 同一套件或子類別為 protected。"],
        "category": "存取修飾詞"
    },
    31: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-31】你是銀行的 Java 程式設計師，請審視下列 account 類別。(行號僅供參考)",
            "01 public class account { 02 protected int amount; 03 public account() { 04 amount = 0; 05 }",
            "06 public account(int total) { 07 amount = total; 08 } }",
            "對於下列每一項敘述，請選取 [O] 或 [X]。",
            "A. account 類別只有一個建構函式。",
            "B. 其他類別可以繼承 account 類別。",
            "C. 第 07 行敘述可改寫為 this.amount = total;"
        ],
        "left": ["A 敘述", "B 敘述", "C 敘述"],
        "right": ["O", "X"],
        "answer": ["B", "A", "A"], # X, O, O
        "explanation": ["A: 有兩個建構函式。B: 非 final 類別可繼承。C: 正確，this 可指向實體成員。"],
        "category": "建構函式與繼承"
    },
    33: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-33】你要建立 Freezer 類別用來模擬冰箱，此類別必須符合下列需求：",
            "● 只允許在同一套件中的類別可存取 Freezer 類別。",
            "● 只允許 Freezer 類別本身存取及修改名稱為 temperature 的資料成員。",
            "● 只允許與 Freezer 類別在同一套件中的類別存取名稱為 minTemperature 的資料成員。",
            "● 確保 minTemperature 資料成員宣告後就無法修改。",
            "A ___ Freezer { B int temperature; C int minTemperature = -15; }"
        ],
        "left": ["A 位置 (class)", "B 位置 (temp)", "C 位置 (minTemp)"],
        "right": ["①public class | ②class | ③final | ④private | ⑤abstract | ⑥protected"],
        "answer": ["B", "D", "C"], # class (B, 預設為package-private), private (D), static/final (此處選 C 代表 final)
        "explanation": ["1. 同一套件存取類別不需修飾詞(預設)。2. 僅限類別本身存取為 private。3. 無法修改為 final。"],
        "category": "存取控制與封裝"
    }
}

for q_id, content in fixes.items():
    for q in data:
        if q['id'] == q_id:
            q.update(content)
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
