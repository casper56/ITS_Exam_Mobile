import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

fixes = {
    1: {
        "question": ["<pre><code class=\"language-java\">【A-01】Java 程式碼中的註解，下列何者為正確語法？</code></pre>"],
        "options": ["// 這是註解文字", "# 這是註解文字", "\\\\ 這是註解文字", "*/ 這是註解文字"],
        "answer": "A",
        "explanation": ["Java 使用 // 進行單行註解，/* */ 進行多行註解。"],
        "category": "基礎語法"
    },
    2: {
        "question": ["<pre><code class=\"language-java\">【A-02】你需要使用最少的記憶體來儲存 3,200,000,000 (32 億) 數值，應該使用下列哪種資料類別？</code></pre>"],
        "options": ["byte", "int", "short", "long"],
        "answer": "D",
        "explanation": ["int 的最大值約為 21 億，32 億超過了 int 的範圍，因此必須使用 long。"],
        "category": "資料型別"
    },
    3: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-03】你正在參加 Java 程式開發人員的面試，必須證明您熟識 main 方法。對於下列關於 main 方法的敘述，請選取 [O] 或 [X]。",
            "A. main 方法的 args 參數是 String 資料類別的陣列。",
            "B. Java 應用程式只能接受一個命令列引數。",
            "C. main 方法必須為靜態，因為執行時不會將類別中的物件實體化。</code></pre>"
        ],
        "left": ["A 敘述", "B 敘述", "C 敘述"],
        "right": ["O", "X"],
        "answer": ["A", "B", "A"],
        "explanation": ["A: 正確，String[] args。B: 錯誤，可接受多個引數。C: 正確，static 方法不需實體化即可執行。"],
        "category": "main 方法規範"
    },
    4: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-04】你在建立一個 Java 主控台應用程式，必須定義應用程式啟動時所執行的第一個方法的簽章，請選取正確的程式碼片段來完成程式碼。",
            "A ___ main ( B ) { ... }</code></pre>"
        ],
        "left": ["A 片段", "B 片段"],
        "right": [
            "①private void | ②public static void | ③private static String | ④public String",
            "①int args[] | ②int args | ③String args[] | ④String arg"
        ],
        "answer": ["B", "C"],
        "explanation": ["標準進入點簽章為 public static void main(String[] args)。"],
        "category": "main 方法規範"
    },
    5: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-05】請選擇適當值作為下列程式碼片段的值。每個值可能使用一次或多次，甚至完全不用。",
            "A. (3 + 2) * 4 - 1",
            "B. 4 * 4 + 2 * 5",
            "C. 8 * 2 % 3",
            "D. 5 / 2 - 6 % 2</code></pre>"
        ],
        "left": ["A 運算", "B 運算", "C 運算", "D 運算"],
        "right": ["① 0 | ② 1 | ③ 2 | ④ 3 | ⑤ 16 | ⑥ 19 | ⑦ 26 | ⑧ 80 | ⑨ 90"],
        "answer": ["F", "G", "B", "C"], # 19, 26, 1, 2
        "explanation": ["A: 5*4-1=19。B: 16+10=26。C: 16%3=1。D: 2-0=2。"],
        "category": "算術運算"
    },
    6: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-06】請審視下列程式碼片段。(行號僅供參考)",
            "01 byte num=127; 02 num++;",
            "03 System.out.println(num);",
            "04 System.out.println(1.0 / 3.0);",
            "05 System.out.println(1.0f / 3.0f);",
            "06 System.out.println(1 / 3);",
            "請選取正確的選項回答問題。",
            "A. 第 03 行的輸出為何？",
            "B. 第 04 行的輸出為何？",
            "C. 第 05 行的輸出為何？",
            "D. 第 06 行的輸出為何？</code></pre>"
        ],
        "left": ["A 輸出", "B 輸出", "C 輸出", "D 輸出"],
        "right": [
            "① -128 | ② 128",
            "① 0.33333334 | ② 0.3333333333333333",
            "① 0.33333334 | ② 0.3333333333333333",
            "① 0.33333334 | ② 0"
        ],
        "answer": ["A", "B", "A", "B"],
        "explanation": ["A: byte 溢位 127+1=-128。B: double 精度。C: float 精度。D: 整數除法 1/3=0。"],
        "category": "資料型別與運算"
    }
}

for q_id, content in fixes.items():
    for q in data:
        if q['id'] == q_id:
            q.update(content)
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
