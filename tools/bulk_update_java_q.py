import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

update_list = {
    22: {
        "type": "single",
        "question": [
            "<pre><code class=\"language-java\">【A-22】請審閱下列程式碼片段：",
            "int[][] array = {{2, 20, 15}, {16, 7, 32}, {50, 4, 27}};",
            "for(int i = 0; i < array.length; i++){",
            "    for(int j = 0; j < array[i].length; j++) {",
            "        if(array[i][j] < 10) break;",
            "        System.out.println(array[i][j]);",
            "    }",
            "}",
            "",
            "請問迴圈執行完成後，主控台視窗輸出為何？</code></pre>"
        ],
        "options": ["16 50", "20 15 16 32 50 27", "50 4 27", "15 32 27"],
        "answer": "A",
        "explanation": ["1. i=0 時，2 < 10 觸發 break，第一列結束。", "2. i=1 時，16 >= 10 (印 16)，接著 7 < 10 (break)。", "3. i=2 時，50 >= 10 (印 50)，接著 4 < 10 (break)。", "最終輸出 16 與 50。"]
    },
    24: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-24】你在撰寫一個 Java 的 checkItems 方法，此方法會執行下列功能：",
            "● 接受名稱為 items 的 String 陣列。",
            "● 逐一查看 items 元素內容。",
            "● 若有元素內容超過 10 個字元，就停止查看並傳回 false。",
            "● 反之則傳回 true。",
            "請選取正確的程式碼片段來完成程式碼。",
            "",
            "public boolean checkItems(String[] items){",
            "    boolean allCheckItems = true;",
            "    for ( ___A___ (String item ___B___ items) {",
            "        if(item.length() > 10) {",
            "            allCheckItems = false;",
            "            ___C___",
            "        }",
            "    };",
            "    return allCheckItems;",
            "}</code></pre>"
        ],
        "left": ["A 選項", "B 選項", "C 選項"],
        "right": [
            "①while | ②for | ③do",
            "①++ | ② : | ③; | ④instanceof",
            "①break; | ②goto; | ③continue;"
        ],
        "answer": ["B", "B", "A"],
        "explanation": ["使用 for-each 語法：for(String item : items)。當條件滿足時，使用 break 立即跳出迴圈。"]
    },
    25: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-25】您是 Java 程式設計師，您的同事建立下列程式碼。(行號僅供參考)",
            "03 while(times => 0) {",
            "04     if(times = 0)",
            "05         break;",
            "06     else{",
            "07         System.out.println(\"倒數計時中...\");",
            "08         times++;",
            "09     }",
            "此程式會從 60 開始倒數，並在主控台顯示訊息，但此程式未能達到預期功能。請選取正確的程式碼片段來修正程式碼。",
            "",
            "while (times ___A___ 0){",
            "    if (times ___B___ 0){",
            "        break;",
            "    }",
            "    else {",
            "        System.out.println(\"倒數計時中...\");",
            "        times ___C___ ;",
            "    }",
            "}</code></pre>"
        ],
        "left": ["A 選項", "B 選項", "C 選項"],
        "right": [
            "①== | ②>= | ③<= | ④=>",
            "①== | ②= | ③!= | ④=>",
            "①+= | ②-= | ③++ | ④--"
        ],
        "answer": ["B", "A", "D"],
        "explanation": ["1. 條件應為大於等於 (>=)。", "2. 判斷相等應使用 (==)。", "3. 倒數計時應使用遞減 (--)。"]
    },
    26: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-26】你正在面試 Java 程式開發人員的工作，你看到下列程式碼：",
            "03     int a = 5;",
            "04     static int b = 5;",
            "05     public void test() {",
            "07         int a = 10;",
            "08         int b = 10;",
            "09         System.out.println(\"a = \" + a);",
            "10         System.out.println(\"this.a = \" + this.a);",
            "11         System.out.println(\"b = \" + b);",
            "12         System.out.println(\"JavaTester.b = \" + JavaTester.b);",
            "請審視該程式碼後，由下列選項中選取正確結果。",
            "",
            "A. 第 09 行輸出為： ___A___",
            "B. 第 10 行輸出為： ___B___",
            "C. 第 11 行輸出為： ___C___",
            "D. 第 12 行輸出為： ___D___</code></pre>"
        ],
        "left": ["A 選項", "B 選項", "C 選項", "D 選項"],
        "right": [
            "①a=5 | ②a=10",
            "①this.a=5 | ②this.a=10 | ③this.x=\"Error\"",
            "①b=5 | ②b=10",
            "①JavaTester.b=5 | ②JavaTester.b=10 | ③JavaTester.b=\"Error\""
        ],
        "answer": ["B", "A", "B", "A"],
        "explanation": ["1. 第09行與11行輸出的是區域變數(10)。", "2. 第10行使用 this.a 存取實體變數(5)。", "3. 第12行使用 JavaTester.b 存取類別變數(5)。"]
    }
}

for q in data:
    if q['id'] in update_list:
        q.update(update_list[q['id']])
        q['category'] = "控制流程與作用域"

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
