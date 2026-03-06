import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 26:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-26】你正在面試 Java 程式開發人員的工作，你看到下列程式碼：(行號僅供參考)",
            "01 public class JavaTester",
            "02 {",
            "03   int a = 5;",
            "04   static int b = 5;",
            "05   public void test()",
            "06   {",
            "07     int a = 10;",
            "08     int b = 10;",
            "09     System.out.println(\"a = \" + a);",
            "10     System.out.println(\"this.a = \" + this.a);",
            "11     System.out.println(\"b = \" + b);",
            "12     System.out.println(\"JavaTester.b = \" + JavaTester.b);",
            "13   }",
            "14 }",
            "",
            "你要判斷 test() 方法的輸出。請審視該程式碼後，由下列選項中選取正確結果。</code></pre>"
        ]
        q['left'] = [
            "A. 第 09 行輸出為",
            "B. 第 10 行輸出為",
            "C. 第 11 行輸出為",
            "D. 第 12 行輸出為"
        ]
        q['right'] = [
            "① a = 5 | ② a = 10",
            "① this.a = 5 | ② this.a = 10 | ③ this.x = \"Error\"",
            "① b = 5 | ② b = 10",
            "① JavaTester.b = 5 | ② JavaTester.b = 10 | ③ JavaTester.b = \"Error\""
        ]
        q['answer'] = ["B", "A", "B", "A"]
        q['explanation'] = [
            "1. 第 09 行輸出區域變數 a = 10 (遮蔽實體變數)。",
            "2. 第 10 行使用 this.a 存取實體變數 5。",
            "3. 第 11 行輸出區域變數 b = 10 (遮蔽靜態變數)。",
            "4. 第 12 行使用類別名 JavaTester.b 存取靜態變數 5。"
        ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Question 26 updated with full details.")
