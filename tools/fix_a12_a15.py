import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

fixes = {
    12: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-12】你要使用初始值來宣告 2X3 的 int 資料型別陣列。請選擇適當的程式碼片段來完成程式碼。每個程式碼片段可能只使用一次，也可能使用多次，甚至完全不用。",
            "",
            "int[][] array = __A__ 72, 34, 56 __B__ 28, 145, 26 __C__</code></pre>"
        ],
        "left": ["A 括號", "B 分隔", "C 結束"],
        "right": ["①[[ ②]] ③][ ④{{ ⑤ }} ⑥}{ ⑦ { ⑧ }, { ⑨ ],["],
        "answer": ["G", "H", "E"], # { (G), }, { (H), } (E)
        "explanation": ["2x3 二維陣列宣告語法：int[][] array = { {72, 34, 56}, {28, 145, 26} };"],
        "category": "陣列宣告"
    },
    13: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-13】你在撰寫一個方法來變更遊戲中玩家的點數，請評估下列程式碼。(行號僅供參考)",
            "01 public class GamePoint { 02 static int extra = 300;",
            "03 public static int changePoint(int point, Boolean bonus, int extra){",
            "04   if(bonus == true){ 05 point += extra; 06 } 07 return point; 08 }",
            "09 ... 10 public static void main(String[] args){ 11 Boolean bonus = true;",
            "12 int point = 10; 13 int newPoint = changePoint(point, bonus, 100);",
            "14 System.out.println(point); 15 System.out.println(newPoint); 16 } }",
            "下列敘述是否正確，請填入 [O] 或 [X]。",
            "A. 第 04 行 bonus 的值為 true。",
            "B. 第 05 行 extra 的值為 300。",
            "C. 第 07 行 point 的值為 110。",
            "D. 第 14 行 point 的值為 110。"
        ],
        "left": ["A 敘述", "B 敘述", "C 敘述", "D 敘述"],
        "right": ["O", "X"],
        "answer": ["A", "B", "A", "B"],
        "explanation": ["A: main 傳入 true。B: 參數遮蔽了類別變數，extra 為 100。C: 10+100=110。D: Java 為 call by value，原始 point 仍為 10。"],
        "category": "方法參數與作用域"
    },
    14: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-14】你在撰寫一個 Java 方法，此方法要能執行下列工作：",
            "● 可接受一個 double 陣列。 ● 會傳回陣列中的最大值。",
            "請選取正確的程式碼片段來完成程式碼。",
            "public double getMax( __A__ ){",
            "  __B__",
            "  for (int i=1; i< __C__ ; i++)",
            "    if( __D__ ) __E__",
            "  return max;",
            "}"
        ],
        "left": ["A 參數", "B 初始化", "C 條件", "D 判斷", "E 指派"],
        "right": [
            "①double[] array | ②double array | ③double[length] array",
            "①double max = array[1]; | ②double max = array[0];",
            "①array.size()-1; | ②array.size(); | ③array.length-1; | ④array.length;",
            "①max != array[i] | ②max < array[i]",
            "①max == array[i]; | ②max = array[i];"
        ],
        "answer": ["A", "B", "D", "B", "B"],
        "explanation": ["A: 陣列型別。B: 設最大值為首項。C: 陣列長度屬性。D: 若目前值較大。E: 更新最大值。"],
        "category": "陣列處理"
    },
    15: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-15】你要建立 if 陳述式，在同時滿足下列兩項條件時，該陳述式會判定為 true：",
            "● total 大於或等於 num。 ● nt 小於 num。",
            "請選擇適當的運算子填入對應位置。運算子：① && ② || ③ < ④ > ⑤ <= ⑥ >= ⑦ == ⑧ !=",
            "if (num __A__ total __B__ nt __C__ num)"
        ],
        "left": ["A 位置", "B 位置", "C 位置"],
        "right": ["① && | ② || | ③ < | ④ > | ⑤ <= | ⑥ >= | ⑦ == | ⑧ !="],
        "answer": ["E", "A", "C"], # <=, &&, <
        "explanation": ["total >= num 等同於 num <= total。且為 &&。nt < num。"],
        "category": "邏輯運算"
    }
}

for q_id, content in fixes.items():
    for q in data:
        if q['id'] == q_id:
            q.update(content)
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
