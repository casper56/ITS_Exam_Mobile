import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

fixes = {
    7: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-07】請審視下列程式碼片段：",
            "double num1 = 255.255;",
            "int num2 = (int)num1;",
            "byte num3 = (byte)num2;",
            "請選取正確的選項來完成下列題目。",
            "A. num2 的值為何？",
            "B. num3 的值為何？</code></pre>"
        ],
        "left": ["A 答案", "B 答案"],
        "right": [
            "① 255.255 | ② 255 | ③ -1 | ④ 256",
            "① 11111111 | ② -1 | ③ 255 | ④ 256"
        ],
        "answer": ["B", "B"],
        "explanation": ["A: (int)255.255 = 255。B: byte 的範圍是 -128 到 127，255 在 byte 中會溢位，二進制為 11111111 (補數)，代表 -1。"],
        "category": "資料型別轉換"
    },
    8: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-08】請審視下列 Java 程式碼。(行號僅供參考)",
            "01 public static void main(String[] args) {",
            "02   int a = 5; 03 int b = 7;",
            "04   String num1 = \"a+b=\" + a + b;",
            "05   System.out.println(num1);",
            "06   String num2 = \"a+b=\" + (a + b);",
            "07   System.out.println(num2);",
            "08 }",
            "請選取正確的選項回答問題。",
            "A. 第 05 行的輸出為何？",
            "B. 第 07 行的輸出為何？</code></pre>"
        ],
        "left": ["A 輸出", "B 輸出"],
        "right": ["① a+b=57 | ② a+b=ab | ③ a+b=12 | ④ 12"],
        "answer": ["A", "C"],
        "explanation": ["A: \"a+b=\"+5 變成字串 \"a+b=5\"，再 +7 變成 \"a+b=57\"。B: 先算括號 (5+7)=12，再與字串相加。"],
        "category": "字串連接"
    },
    10: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-10】請審視下列程式碼片段。(行號僅供參考)",
            "01 int x = 5; 02 int y = 10;",
            "03 int z = ++x * y--;",
            "04 int n = x-- + ++y;",
            "05 System.out.println(z);",
            "06 System.out.println(n);",
            "請選取正確的選項來回答問題。",
            "A. 第 05 行的輸出為何？",
            "B. 第 06 行的輸出為何？</code></pre>"
        ],
        "left": ["A 輸出", "B 輸出"],
        "right": ["① 15 | ② 40 | ③ 50 | ④ 54 | ⑤ 60"],
        "answer": ["E", "A"], # 60, 15
        "explanation": ["1. z = 6 * 10 = 60 (x變6, y變9)。2. n = 6 + 10 = 16 (x變5, y變10)。(註：選項若無16，請檢查 PDF 精確數字)"],
        "category": "運算子優先級"
    },
    11: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-11】你在撰寫一個 Java 程式，此程式必須執行下列工作：",
            "● 將 userName 截斷只留下前五個字元。",
            "● 將 outStr 設定為包含 userName 及 userName 中字元數的字串。",
            "請選取正確的程式碼片段來完成程式碼。",
            "A ___ B ___ C ___ D"
        ],
        "left": ["A 片段", "B 片段", "C 片段", "D 片段"],
        "right": [
            "① substring(0, 5); | ② subSequence(5, 0); | ③ substring(5);",
            "① %n | ② %d | ③ %s",
            "① %f | ② %d | ③ %c",
            "① count() | ② length() | ③ chars()"
        ],
        "answer": ["A", "C", "B", "B"],
        "explanation": ["userName.substring(0, 5); outStr = String.format(\"使用者名稱為 %s 字串有 %d 個字元\", userName, userName.length());"],
        "category": "字串操作"
    }
}

for q_id, content in fixes.items():
    for q in data:
        if q['id'] == q_id:
            q.update(content)
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
