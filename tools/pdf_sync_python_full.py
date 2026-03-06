import json
import os

def sync_full():
    json_path = 'www/ITS_Python/questions_ITS_python.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    q_map = {item['id']: item for item in data}

    # --- CH01 Q1 (ID 1 - 步速計算) ---
    if 1 in q_map:
        q_map[1]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 距離：距離測量通常需要精確，可能是小數，應使用 float 轉換輸入為浮點數以保留精度。",
            "2. 分鐘：題目要求「分秒輸入值都要轉換為整數」，故使用 int。",
            "3. 秒數：同理，使用 int 轉換為整數。",
            "綜合以上分析，正確順序為 float, int, int。</code></pre>"
        ]

    # --- CH01 Q2 (ID 2 - 變數類型) ---
    if 2 in q_map:
        q_map[2]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. age = 12: 沒有小數點的整數，屬於 int。",
            "2. minor = False: 布林值，屬於 bool。",
            "3. name = 'David': 雙引號包圍的文字，屬於 str。",
            "4. weight = 64.5: 帶有小數點的數字，屬於 float。",
            "5. zip = '545': 被雙引號包圍，視為文字，屬於 str。</code></pre>"
        ]

    # --- CH01 Q3 (ID 3 - 出生年份類型) ---
    if 3 in q_map:
        q_map[3]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "A. 正確。input() 無論輸入什麼，一律以字串 (str) 回傳。",
            "B. 錯誤。eval() 處理整數減法通常回傳 int (如 2024-30=1994)，除非輸入含小數點。",
            "C. 錯誤。message 由字串串接而成，結果永遠是字串 (str)。</code></pre>"
        ]

    # --- CH02 Q2 (ID 13 - 運算優先級) ---
    if 13 in q_map:
        q_map[13]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 取餘數: 24 % 7 = 3。",
            "2. 乘法: 3 * 100 = 300。",
            "3. 指數: 2.0 ** 3.0 = 8.0。",
            "4. 整數除法: 300 // 8.0 = 37.0 (浮點數參與運算，結果為浮點數但取整)。",
            "5. 減法: 37.0 - 7 = 30.0。</code></pre>"
        ]

    # --- CH02 Q3 (ID 7 - 數學公式 (-a)**2) ---
    if 7 in q_map:
        q_map[7]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "題目要求「a 乘以 -1 之後再平方」。這意指 (a * -1) 整體進行平方運算。",
            "由於指數運算 (**) 優先級高於負號 (Unary negation)，",
            "若寫 -a**2 會被解讀為 -(a**2)。因此必須加上括號寫成 (-a)**2。</code></pre>"
        ]

    # --- CH03 Q3 (ID 6 - is vs ==) ---
    if 6 in q_map:
        q_map[6]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 初次 is：alist 與 blist 是不同物件，記憶體位置不同，故為 False。",
            "2. 初次 ==：內容分別是字串與數字，內容不同，故為 False。",
            "3. 賦值：aList = bList 使兩者指向同一物件。",
            "4. 賦值後 is 與 ==：指向同物件且內容相同，兩者皆為 True。</code></pre>"
        ]

    # --- CH03 Q4 (ID 69 - 反轉名稱) ---
    if 69 in q_map:
        q_map[69]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 初始化索引：Python 索引從 0 開始，最後一個字元索引為 len(s) - 1。",
            "2. 取得字元：使用 backward_name[index] 取得當前指向的字元並串接。</code></pre>"
        ]

    # --- CH03 Q5 (ID 26 - Slicing) ---
    if 26 in q_map:
        q_map[26]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. alph[3:15]: 取索引 3 到 14，即 'defghijklmno'。",
            "2. alph[3:15:3]: 每隔 3 個取一個，取 3,6,9,12，即 'dgjm'。",
            "3. alph[15:3:-3]: 反向，從 15 開始每隔 3 個，取 15,12,9,6，即 'pmjg'。",
            "4. alph[::-3]: 從最後一個開始反向每隔 3 個，取 'zwtqnkheb'。</code></pre>"
        ]

    # 寫回 JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Successfully updated JSON with full PDF content (Batch 1).")

if __name__ == "__main__":
    sync_full()
