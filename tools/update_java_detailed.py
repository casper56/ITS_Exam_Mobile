import json
import os

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 更新題號 26 (A-26) 的詳細內容
for q in data:
    if q['id'] == 26:
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
            "你要判斷 test() 方法的輸出。請審視該程式碼後，由下列選項中選取正確結果。</code>"
        ]
        q['explanation'] = [
            "1. 第 09 行輸出區域變數 a=10。",
            "2. 第 10 行輸出實體變數 this.a=5。",
            "3. 第 11 行輸出區域變數 b=10。",
            "4. 第 12 行輸出類別變數 JavaTester.b=5。"
        ]

    # 更新 A-29 (修正拼字 Triange -> Triangle)
    if q['id'] == 29:
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
            "你要撰寫 Triangle 類別的測試程式，請選取正確的程式碼片段來完成測試程式。</code>",
            "int area;",
            "___A___",
            "___B___",
            "System.out.printf(\"寬=%d 高=%d\\n\", ___C___ );",
            "System.out.printf(\"面積=%b \\n\", area == 400);"
        ]

    # A-37 修正
    if q['id'] == 37:
        q['question'] = [
            "<pre><code class=\"language-java\">【A-37】請審視下列程式碼：",
            "public class SearchArray {",
            "  public static void main(String[] args)",
            "  {",
            "    int[][] ary = {{19, 25}, {28, 30, 50}};",
            "    for (int x = 2; x >= 0; x--){",
            "      for (int y = 2; y >= 0; y--){",
            "        System.out.println(ary[row][column] + \" \");",
            "      }",
            "    }",
            "  }",
            "}",
            "",
            "執行此程式時之輸出為何？</code>"
        ]

    # B-04 修正 (順序題)
    if q['id'] == 44:
        q['question'] = [
            "<pre><code class=\"language-java\">【B-04】您正在面試某份工作。主考官要求您建立一個簡易的主控台程式。此程式必須執行下列工作：",
            "● 自命令列接受多個引數。",
            "● 以使用者在命令列上所輸入的相同順序在畫面上輸出引數。",
            "",
            "請問您應該依序使用哪三個程式碼片段來開發解決方案？請將三個程式碼片段移至答案區，然後按照正確的順序排列。",
            "程式碼片段：",
            "① for (int x = 1; x <= Integer.parseInt(args[0]); x++) {",
            "② System.out.println(arguments[x]);",
            "   }",
            "③ public static void main(String[] args) {",
            "④ for (int x = 1; x <= arguments.length; x++) {",
            "⑤ public static void main(String arguments) {",
            "⑥ System.out.println(args[x]);",
            "   }",
            "⑦ for (int x = 0; x < args.length; x++) {</code></pre>"
        ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Update completed successfully.")
