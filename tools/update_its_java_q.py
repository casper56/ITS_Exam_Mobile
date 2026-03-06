import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 更新 A-19
for q in data:
    if q['id'] == 19:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-19】你在撰寫一個 Java 方法，此方法要能執行下列工作：",
            "● 接受名稱為 ages 的 int 參數。",
            "● 若 ages 為 65 或以上，則指定為 &quot;老人&quot; 分類 (kind)。",
            "● 若 ages 為 20 或以上，但低於 65，則指定為 &quot;成人&quot; 分類。",
            "● 否則，指定為 &quot;青年&quot; 分類。",
            "請選取正確的程式碼片段來完成程式碼。",
            "",
            "public static String ageClassification(int ages){",
            "    String kind;",
            "    ___A___",
            "        kind = &quot;老人&quot;;",
            "    ___B___",
            "        kind = &quot;成人&quot;;",
            "    ___C___",
            "        kind = &quot;青年&quot;;",
            "    return kind;",
            "}</code></pre>"
        ]
        q['right'] = [
            "①if (ages != 65) | ②if (ages >= 65) | ③if (ages > 65) | ④if (ages >= 65 || ages != 20)",
            "①if (ages < 20) | ②if (ages > 19) | ③else if (ages >= 19) | ④else if (ages >= 20)",
            "①if (ages <= 20) | ②else | ③default | ④else if (ages != 20)"
        ]
        q['answer'] = ["B", "D", "B"]
        q['explanation'] = ["1. A選② (ages>=65)", "2. B選④ (else if ages>=20)", "3. C選② (else)"]
        q['category'] = "控制流程"

# 更新 A-20
for q in data:
    if q['id'] == 20:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-20】您在撰寫一個 Java 的 countdown 方法，此方法必須執行下列工作：",
            "● 接受名稱為 num 的 int 參數。",
            "● 顯示從 num 遞減到零的所有數字。",
            "請選取正確的程式碼片段來完成程式碼。",
            "",
            "public static void countdown(int num){",
            "    for ( ___A___  ___B___  ___C___ ){",
            "        System.out.println(i);",
            "    }",
            "}</code></pre>"
        ]
        q['left'] = ["A 選項", "B 選項", "C 選項"]
        q['right'] = [
            "①int i = num; | ②int i == num; | ③int i < num; | ④int i <= num;",
            "①i < 0; | ②i <= 0; | ③i > 0; | ④i >= 0;",
            "①+i | ②++i | ③--i | ④-i"
        ]
        q['answer'] = ["A", "D", "C"]
        q['explanation'] = ["for迴圈初始化 i=num，條件 i>=0，每次執行後 i--。"]
        q['category'] = "控制流程"

# 更新 A-21
for q in data:
    if q['id'] == 21:
        q['type'] = "single"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-21】請檢閱下列程式碼片段：",
            "char[][] array = {{'a', 'b', 'c'}, {'d', 'e', 'f'}, {'g', 'h', 'i'}};",
            "for(int i = 0; i < array.length; i++) {",
            "    for(int j = array[i].length - 1; j >= 0; j--)",
            "        System.out.print(array[i][j]);",
            "}",
            "",
            "請問迴圈執行完成後，主控台視窗會輸出下列何者？</code></pre>"
        ]
        q['options'] = ["cbafedihg", "abcdefghi", "ghidefabc", "ihgfedcba"]
        q['answer'] = "A"
        q['explanation'] = ["外層迴圈遍歷列(Row)，內層迴圈從最後一個索引反向輸出該列字元。'abc'->'cba', 'def'->'fed', 'ghi'->'ihg'。"]
        q['category'] = "二維陣列"

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
