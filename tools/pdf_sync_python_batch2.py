import json
import os

def sync_batch2():
    json_path = 'www/ITS_Python/questions_ITS_python.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    q_map = {item['id']: item for item in data}

    # --- ID 87 (PDF 202412 Q02) ---
    if 87 in q_map:
        q_map[87]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 需求：\"ItemName\", Quantity (字串加雙引號，數字不加，逗號分隔)。",
            "2. 選項 C：'\"{0}\", {1}' 手動在 {0} 外加雙引號，輸出符合 \"ItemName\", Quantity。",
            "3. 選項 D：print 預設逗號分隔會補一空格。'\"' + item + '\",' 串接後加 sales 變為 \"ItemName\", Quantity。",
            "注意：選項 B 會因 int 與 str 相加引發 TypeError。</code></pre>"
        ]

    # --- ID 12 (PDF 20250804 CH02 Q12) ---
    if 12 in q_map:
        q_map[12]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. n1 == n2：相等比較，語法正確。",
            "2. n1 <= n2：包含「小於」或「等於」，故「只有在小於時才列印」的敘述是錯誤的 (X)。",
            "3. n2 = n1：這是在執行「賦值」而非比較，會導致 Syntax Error。正確應使用 ==。",
            "4. n2 <> n1：這是 Python 2 的舊語法，Python 3 已廢棄，應改用 !=。</code></pre>"
        ]

    # --- ID 46 (PDF 20250804 CH05 Q5) ---
    if 46 in q_map:
        q_map[46]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 5歲以上且是學生 (60元)：if age >= 5 and school == True:。",
            "2. 5歲至17歲非學生 (120元)：elif age <= 17: (此處因前一條件已排除學生，故只需判斷年齡)。",
            "3. 17歲以上非學生 (180元)：最後的 else 區塊。</code></pre>"
        ]

    # --- ID 61 (PDF 20250804 CH05 Q6) ---
    if 61 in q_map:
        q_map[61]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 一位數：num < 10 (在正整數前提下)。",
            "2. 兩位數：num < 100 (已排除一位數，故涵蓋 10-99)。",
            "3. 超過兩位數：最後的 else 或 elif num >= 100:。</code></pre>"
        ]

    # --- ID 44 & 58 (PDF 20250804 CH05 Q1) ---
    for qid in [44, 58]:
        if qid in q_map:
            q_map[qid]['explanation'] = [
                "<pre><code class=\"language-python\">解題分析：",
                "這是一個典型的階梯式 if-elif-else 結構。",
                "1. A 級 (90-100)：if grade >= 90:。",
                "2. B 級 (80-89)：elif grade >= 80: (已隱含 < 90 的前提)。",
                "3. C 級 (70-79)：elif grade >= 70:。",
                "4. D 級 (60-69)：elif grade >= 60:。",
                "5. 不及格：最後由 else 捕捉。</code></pre>"
            ]

    # --- ID 34 (PDF 20250804 CH05 Q9) ---
    if 34 in q_map:
        q_map[34]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 全大寫檢查：if name.upper() == name:。若成立代表原字串即為全大寫。",
            "2. 全小寫檢查：elif name.lower() == name:。",
            "3. 混合大小寫：最後使用 else 處理。</code></pre>"
        ]

    # --- ID 31 (PDF 20250804 CH04 Q10) ---
    if 31 in q_map:
        q_map[31]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. EOF (檔案結尾)：readline() 讀到結尾會回傳「空字串 ''」。",
            "2. 空行：readline() 讀到空行會回傳「換行符號 '\\n'」。",
            "3. 邏輯：必須先判斷是否為結尾 (line != '')，再判斷是否為空行 (line != '\\n') 才能正確過濾。</code></pre>"
        ]

    # --- ID 45 (PDF 202412 Q22) ---
    if 45 in q_map:
        q_map[45]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 正數判斷：if a >= 0:。正數可直接開任意次方根。",
            "2. 負偶數次方根：a < 0 且 b % 2 == 0。這會產生虛數 (Imaginary number)。",
            "3. 負奇數次方根：a < 0 且 b 為奇數。數學上等於 -((-a) ** (1/b))。</code></pre>"
        ]

    # 寫回 JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Successfully updated Batch 2 items from PDF.")

if __name__ == "__main__":
    sync_batch2()
