import json
import os

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

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
        q['left'] = ["A 選項", "B 選項", "C 選項"]
        q['right'] = [
            "①if (ages != 65) | ②if (ages >= 65) | ③if (ages > 65) | ④if (ages >= 65 || ages != 20)",
            "①if (ages < 20) | ②if (ages > 19) | ③else if (ages >= 19) | ④else if (ages >= 20)",
            "①if (ages <= 20) | ②else | ③default | ④else if (ages != 20)"
        ]
        q['answer'] = ["B", "D", "B"]
        q['explanation'] = [
            "根據題目需求：",
            "1. ages >= 65 為老人。對應 ___A___ 應選 ②if (ages >= 65)。",
            "2. 20 <= ages < 65 為成人。在 if (ages >= 65) 之後，應使用 ___B___ ④else if (ages >= 20)。",
            "3. 其餘 (小於 20) 為青年。對應 ___C___ 應選 ②else。"
        ]
        q['category'] = "控制流程"
        break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Successfully updated question ID 19.")
