import json
import os

def sync_batch3():
    json_path = 'www/ITS_Python/questions_ITS_python.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    q_map = {item['id']: item for item in data}

    # --- CH06 Q1-Q6 (ID 63-68) ---
    if 63 in q_map:
        q_map[63]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\nPython 註解使用 # 開頭，函式定義使用 def 關鍵字，主體必須縮排。</code></pre>"]
    if 64 in q_map:
        q_map[64]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n1. # 開頭為註解，會被直譯器忽略。\n2. 函式內部的字串 (docstring) 雖不執行，但屬於物件屬性，與純註解不同。</code></pre>"]
    if 65 in q_map:
        q_map[65]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n呼叫時傳入兩個引數 (distance, burn_rate)，故定義時參數名稱需對齊內部使用的 kms 與 calories_per_km。</code></pre>"]
    if 66 in q_map:
        q_map[66]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n1. 定義：def calc_score\n2. 參數：(current, value):\n3. 回傳：return current</code></pre>"]
    if 67 in q_map:
        q_map[67]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n1. 預設參數：points = 1 必須放在參數列最後。\n2. 區域變數：函式內修改 points 不會影響外部變數。</code></pre>"]
    if 68 in q_map:
        q_map[68]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n1. getpay(salary=50000)：雖有執行但無 return，回傳 None。\n2. qty > 0 時：直接 return 計算結果，後續程式碼不執行。</code></pre>"]

    # --- CH07 Q1-Q8 (ID 74-81) ---
    if 74 in q_map:
        q_map[74]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n使用 from datetime import datetime as dt 可以直接透過 dt 存取類別。</code></pre>"]
    if 75 in q_map:
        q_map[75]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n使用了 os.path.isfile 但未先 import os，會導致 NameError。</code></pre>"]
    if 76 in q_map:
        q_map[76]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n1. randint(11, 20)：包含 11 與 20。\n2. randrange(11, 21)：包含 11 但不包含 21 (即 11-20)。</code></pre>"]
    if 79 in q_map:
        q_map[79]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\nmath.fabs(x) 取絕對值；math.ceil(x) 無條件進位至整數。</code></pre>"]
    if 80 in q_map:
        q_map[80]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n1. now.strftime(\"%A\")：取得星期幾全稱 (如 Friday)。\n2. now.weekday()：取得 0-6 數字 (週一為 0)。</code></pre>"]
    if 81 in q_map:
        q_map[81]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\nrandom.choice(list) 從清單隨機選一元素；random.randint(1, 50) 產生 1-50 整數。</code></pre>"]

    # --- CH08 Q1-Q7 (ID 82-86, 92-93) ---
    if 82 in q_map:
        q_map[82]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n1. try 可配多個 except。\n2. finally 必在最後且不論有無錯誤皆執行。\n3. try 後不可直接接 finally 而不含 except (雖然語法允許但邏輯不完整)。</code></pre>"]
    if 83 in q_map:
        q_map[83]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n接收輸入 int() 應放在 try 中，若使用者輸入非數字則由 except ValueError 捕捉。</code></pre>"]
    if 93 in q_map:
        q_map[93]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\n1. assertEqual(a, b)：值相等 (==)。\n2. assertIs(a, b)：身分相同 (is)。\n3. assertIn(a, list)：成員關係 (in)。</code></pre>"]
    if 92 in q_map:
        q_map[92]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\nunittest 類別需繼承 unittest.TestCase，測試方法需以 test_ 開頭。</code></pre>"]
    if 85 in q_map:
        q_map[85]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\ninput() 回傳字串，執行 a ** b 會因字串無法進行乘冪運算引發 TypeError。</code></pre>"]
    if 86 in q_map:
        q_map[86]['explanation'] = ["<pre><code class=\"language-python\">解題分析：\nw+ 模式在檔案不存在時會自動建立，故 open 不會報錯；但若變數未定義即使用會引發 NameError。</code></pre>"]

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Successfully synchronized Batch 3 (CH06-CH08) from PDF.")

if __name__ == "__main__":
    sync_batch3()
