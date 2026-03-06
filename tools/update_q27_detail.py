import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 27:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-27】你要建立 Test 類別來模擬學校考試，此類別必須符合下列需求：",
            "● 不用將 Test 類別實體化，就可呼叫 setMaxItems 方法。",
            "● 只有和 Test 類別在同一套件中的類別可呼叫 setItems 方法。",
            "● 只有和 Test 類別在同一套件中的類別可呼叫名稱為 setPassScore 的執行個體方法。",
            "",
            "請從以下選取正確的選項來完成程式碼。",
            "A. ①protected ②private ③static ④public",
            "B. ①protected ②private ③static ④public",
            "",
            "class Test {",
            "    ___A___ void setItems (int num){",
            "    }",
            "    ___B___ void setPassScore (int score){",
            "    }",
            "}</code></pre>"
        ]
        q['left'] = [
            "A 位置",
            "B 位置"
        ]
        q['right'] = [
            "①protected | ②private | ③static | ④public"
        ]
        # A: ③ (C), B: ① (A)
        q['answer'] = ["C", "A"]
        q['explanation'] = [
            "1. 需求一「不用將類別實體化即可呼叫」：這代表該方法必須宣告為 static。因此 A 位置填入 ③static。",
            "2. 需求二/三「只有同一套件中的類別可呼叫」：在 Java 中，protected 修飾詞允許同一個套件內的類別存取，也允許不同套件的子類別存取。在選項中，這是最符合「同一套件存取」需求的關鍵字。因此 B 位置填入 ①protected。"
        ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Question 27 updated with high detail and correct logic.")
