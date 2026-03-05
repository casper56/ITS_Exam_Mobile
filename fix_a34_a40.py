import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

fixes = {
    34: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-34】Song 類別包含一個只能從類別內部存取的 isInSinger 方法。isInSinger 方法接受歌手姓名，來和歌手清單進行比較。請選取正確的選項來完成程式碼。",
            "A ___ B ___ isInSinger C {",
            "  for (int i=0; i<numSingers; i++){",
            "    if (singers[i].equals(singer)) D",
            "  } E",
            "}"
        ],
        "left": ["A 位置", "B 位置", "C 位置", "D 位置", "E 位置"],
        "right": [
            "①private | ②public | ③protected",
            "①bool | ②int | ③void | ④String | ⑤boolean",
            "①(String singer) | ②() | ③(bool singer)",
            "①return singer; | ②return false; | ③return singer; | ④return true;",
            "①return singer; | ②return false; | ③return singer; | ④return true;"
        ],
        "answer": ["A", "E", "A", "D", "B"], # private, boolean, (String singer), return true, return false
        "explanation": ["1. 僅限內部存取為 private。2. 判斷是否存在傳回 boolean。3. 參數為 String。4. 找到傳回 true，沒找到傳回 false。"],
        "category": "方法定義"
    },
    37: {
        "type": "single",
        "question": [
            "<pre><code class=\"language-java\">【A-37】請審視下列程式碼片段：",
            "public class SearchArray {",
            "  public static void main(String[] args) {",
            "    int[][] ary = {{19, 25}, {28, 30, 50}};",
            "    for (int x=2; x>=0; x--) {",
            "      for (int y=2; y>=0; y--) {",
            "        System.out.println(ary[x][y] + \" \");",
            "      }",
            "    }",
            "  }",
            "}",
            "執行此程式時會產生的結果為何？</code></pre>"
        ],
        "options": ["30 28 25 19", "50 30 28 25 19 28", "ArrayIndexOutOfBoundsException", "編譯錯誤"],
        "answer": "C",
        "explanation": ["x=2 起跳，但 ary 只有兩列 (索引 0, 1)，故會丟出 ArrayIndexOutOfBoundsException。"],
        "category": "例外狀況"
    },
    39: {
        "type": "multimatching",
        "question": [
            "<pre><code class=\"language-java\">【A-39】請審核下列程式碼片段，要找出輸出結果。(行號僅供參考)",
            "01 try { 02 int x = 1 / 0; 03 System.out.println(\"執行 try\"); }",
            "05 catch (ArithmeticException ex) { 06 System.out.println(\"捕捉到 ArithmeticException\"); }",
            "08 catch (Exception ex) { 09 System.out.println(\"捕捉到 Exception\"); }",
            "11 finally { 12 System.out.println(\"執行 finally\"); }",
            "對於下列敘述，請選取 [O] 或 [X]。",
            "A. 輸出：執行 try",
            "B. 輸出：捕捉到 ArithmeticException",
            "C. 輸出：捕捉到 Exception",
            "D. 輸出：執行 finally"
        ],
        "left": ["A 敘述", "B 敘述", "C 敘述", "D 敘述"],
        "right": ["O", "X"],
        "answer": ["B", "A", "B", "A"], # X, O, X, O
        "explanation": ["1. 1/0 會引發 ArithmeticException。2. 被專屬 catch 捕捉，不進一般 Exception。3. finally 無論如何都會執行。"],
        "category": "例外處理"
    }
}

for q_id, content in fixes.items():
    for q in data:
        if q['id'] == q_id:
            q.update(content)
            break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
