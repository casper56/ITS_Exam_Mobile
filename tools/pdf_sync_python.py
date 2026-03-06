import json
import os

def sync_pdf_to_json():
    json_path = 'www/ITS_Python/questions_ITS_python.json'
    if not os.path.exists(json_path):
        print("Error: JSON file not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 建立 ID 索引方便更新
    q_map = {item['id']: item for item in data}

    # --- 修正 ID 87 (PDF 02) ---
    if 87 in q_map:
        q_map[87]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 需求分析：目標輸出格式為 \"ItemName\", Quantity。",
            "2. 選項 A：\"{0},{1}\" 輸出結果為 ItemName,Quantity（字串沒有雙引號，逗號後沒有空格），不符需求。",
            "3. 選項 B：item + ',' + sales 會引發 TypeError，因為 sales 是整數 (int)，不能直接與字串相加。",
            "4. 選項 C：'\"{0}\", {1}' 手動在 {0} 外加上雙引號。輸出結果為 \"ItemName\", Quantity，符合需求。",
            "5. 選項 D：print 函式使用逗號分隔參數時，預設會加入一個空格。'\"' + item + '\",' 串接後變成 \"ItemName\",，接著印出 sales。結果為 \"ItemName\", Quantity，符合需求。</code></pre>"
        ]

    # --- 修正 ID 3 (PDF 06) ---
    if 3 in q_map:
        q_map[3]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 第 01 行：input() 函式回傳的永遠是 字串 (str)。",
            "2. 第 03 行：eval() 會計算字串運算式的值。整數減整數的結果仍為 整數 (int)。",
            "3. 第 04-05 行：\"...\" + str(born) 是字串串接運算，結果為 字串 (str)。",
            "本題詢問 age 的類型，故答案為 A (str)。</code></pre>"
        ]

    # --- 修正 ID 88 (PDF 07) ---
    if 88 in q_map:
        q_map[88]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 字典內容：1 (Key) 是整數，'Foyer' (Value) 是字串。故第 1 小題選 C (整數和字串)。",
            "2. 輸入類型：input() 取得的是字串。故第 2 小題選 D (String/str)。",
            "3. 錯誤原因：字典的鍵 (Key) 是整數 1，但變數 room 是字串 \"1\"。在 Python 中 \"1\" != 1，因此找不到該鍵。這是資料類型不匹配的問題。故第 3 小題選 B。</code></pre>"
        ]

    # --- 修正 ID 89 (PDF 08) ---
    if 89 in q_map:
        q_map[89]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. %B：完整的月份名稱（如 April，題目顯示為全大寫 APRIL）。",
            "2. %d：兩位數的日期（07）。",
            "3. %y：兩位數的年份（17）。",
            "4. 格式字串：{:%B-%d-%y} 組合為 Month-Day-Year，即 APRIL-07-17。</code></pre>"
        ]

    # --- 修正 ID 9 (PDF 09 - 咖啡問卷) ---
    # PDF 的版本較詳細，我將 ID 9 更新為 PDF 版本
    if 9 in q_map:
        q_map[9]['question'] = [
            "<pre><code class=\"language-python\">某間食品公司需要一套簡易程式，讓他們的客服中心能夠用來輸入新咖啡種類的問卷調查資料。",
            "此程式必須執行下列工作:",
            "- 接受輸入 (rating)。",
            "- 傳回五星評比標準的平均評分 (average)。",
            "- 將輸出四捨五入到兩位小數。",
            "",
            "sum = count = done = 0",
            "average = 0.0",
            "while done != -1:",
            " rating = ____(1)____",
            " if rating == -1:",
            " break",
            " sum += rating",
            " count += 1",
            "average = float(sum / count)",
            "____(2)____ (\"The average star rating for the new coffee is: \" + ____(3)____)</code></pre>"
        ]
        q_map[9]['options'] = [
            "<code>(1) A. float(input(\"...\")) (2) C. print (3) D. format(average, '.2f'))</code>",
            "<code>(1) B. input \"...\" (2) B. output (3) A. {average, '.2f}</code>",
            "<code>(1) C. input(\"...\") (2) D. printline (3) C. format(average,'.2d'))</code>"
        ]
        q_map[9]['answer'] = ["A"]
        q_map[9]['explanation'] = [
            "<pre><code class=\"language-python\">解題分析：",
            "1. 輸入處理 (1)：輸入必須轉換為數值才能進行加法運算，使用 float(input(...)) 是正確的語法。",
            "2. 輸出函式 (2)：Python 3 使用 print 函式輸出資料。",
            "3. 格式化 (3)：題目要求四捨五入到兩位小數。format(average, '.2f') 是正確用法。</code></pre>"
        ]

    # 寫回 JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Successfully synchronized PDF content to JSON (Batch 1).")

if __name__ == "__main__":
    sync_pdf_to_json()
