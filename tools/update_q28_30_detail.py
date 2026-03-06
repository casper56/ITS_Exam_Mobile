import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    # 題號 28 (A-28)
    if q['id'] == 28:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-28】你在撰寫名稱為 account 的 Java 類別，此類別具備下列方法：",
            "● 不用將 account 類別實體化，就能從任何程式碼呼叫 showItems 方法。",
            "● 僅有同一套件中的類別，以及任何套件中 account 類別的子類別可以存取名稱為 newAccount 的方法。",
            "",
            "請選擇適當的程式碼片段填至對應位置，以完成程式碼。每個程式碼片段可能使用一次或多次，甚至完全不用。",
            "程式碼片段：",
            "① private ② final ③ protected ④ public ⑤ static",
            "",
            "public class account {",
            "    ___A___  ___B___ void showItems () { /*...*/ }",
            "    ___C___ void newAccount(String[] items) { /*...*/ }",
            "}</code></pre>"
        ]
        q['left'] = ["A 位置", "B 位置", "C 位置"]
        q['right'] = ["① private | ② final | ③ protected | ④ public | ⑤ static"]
        q['answer'] = ["D", "E", "C"] # A: 4, B: 5, C: 3
        q['explanation'] = [
            "1. 「從任何程式碼呼叫」代表權限為 public (④)。",
            "2. 「不用實體化就能呼叫」代表必須為 static (⑤)。",
            "3. 「同一套件或子類別存取」代表權限為 protected (③)。"
        ]

    # 題號 29 (A-29)
    if q['id'] == 29:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-29】你是 Java 程式設計師，同事建立了 Triangle 類別。(行號僅供參考)",
            "01 public class Triangle {",
            "02   private int width;",
            "03   private int length;",
            "04",
            "05   Triangle(int width, int length){",
            "06     this.width = width;",
            "07     this.length = length;",
            "08   }",
            "09",
            "10   public int calArea(){",
            "11     return this.width * this.length / 2;",
            "12   }",
            "13",
            "14   public int getWidth(){",
            "15     return this.width;",
            "16   }",
            "17",
            "18   public int getLength(){",
            "19     return this.length;",
            "20   }",
            "21 }",
            "",
            "你要撰寫 Triangle 類別的測試程式，請選取正確的程式碼片段來完成測試程式。</code></pre>",
            "<pre><code class=\"language-java\">int area;",
            "___A___",
            "___B___",
            "System.out.printf(\"寬 = %d 高 = %d\\n\", ___C___ );",
            "System.out.printf(\"面積是否正確: %b \\n\", area == 400);</code></pre>"
        ]
        q['left'] = [
            "A. 建立實例 (Triangle tri = ...)",
            "B. 計算面積 (area = ...)",
            "C. 獲取寬高參數"
        ]
        q['right'] = [
            "① Triangle tri = new Triangle(20, 40); | ② Triangle tri = Triangle(20, 40);",
            "① area = tri.calArea() | ② area = Triangle.calArea()",
            "① tri.getWidth(), tri.getLength() | ② tri.width, tri.length"
        ]
        q['answer'] = ["A", "A", "A"] # A: 1, B: 1, C: 1 (根據新的 right 列表排列)
        q['explanation'] = [
            "A: 必須使用 new Triangle(20, 40) 來呼叫建構子。",
            "B: calArea 是實體方法，必須透過物件實體 tri 呼叫。",
            "C: width 與 length 是 private，外部必須透過 public 的 Getter 方法 (getWidth/getLength) 存取。"
        ]

    # 題號 30 (A-30)
    if q['id'] == 30:
        q['type'] = "single"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-30】你為學校撰寫下列程式碼。(行號僅供參考)",
            "01 public class Teacher {",
            "02   public String tchName = \"Jack\";",
            "03",
            "04",
            "05   public String toString(){",
            "06     return tchName;",
            "07   }",
            "08 }",
            "",
            "Teacher 類別要使用自定義的 toString 方法，而非標準方法。請問應該在第 04 行使用哪個註釋？</code></pre>"
        ]
        q['options'] = [
            "@Override",
            "@Rewrite",
            "@Repeatable",
            "@Inherited"
        ]
        q['answer'] = "A"
        q['explanation'] = [
            "在 Java 中，toString() 是繼承自 Object 類別的方法。若要定義自己的版本，應標註 @Override，這能讓編譯器協助檢查是否正確覆寫了父類別的方法。"
        ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Questions 28, 29, 30 updated successfully.")
