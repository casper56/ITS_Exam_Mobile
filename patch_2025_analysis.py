
import json

json_path = 'www/ITS_Python/questions_ITS_python.json'
with open(json_path, 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Mapping of updates
updates = {
    20: [
        "<pre><code class="language-python"><b>【2025 深度追蹤分析】</b>",
        "這是一個 while 迴圈，x 從 0 開始，每次加 1，直到 x=4 停止：",
        "1. x = 0：0%4==0 成立 -> 印出 'party'。x 變 1。",
        "2. x = 1：1-2 < 0 成立 -> 印出 'cake'。x 變 2。",
        "3. x = 2：前述皆不合，進入 else -> 印出 'birthday'。x 變 3。",
        "4. x = 3：前述皆不合，進入 else -> 印出 'birthday'。x 變 4。",
        "5. x = 4：條件 x < 4 不成立，結束。結案：party, cake, birthday, birthday</code></pre>"
    ],
    44: [
        "<pre><code class="language-python"><b>【2025 邏輯優化建議】</b>",
        "官方邏輯採「漏斗式過濾」，但 PDF 分析指出其順序有瑕疵：",
        "1. 必須先處理 None：if age is None 必須最先檢查，否則與整數比較會噴 TypeError。",
        "2. 判斷順序：正確應由大到小 (18, 13...) 或由小到大 (12, 17...)，避免 10 歲同時符合 <18 與 <13 的混亂。",
        "3. else 區塊：在此題中補足了所有「非特定範圍」的剩餘情況。</code></pre>"
    ],
    61: [
        "<pre><code class="language-python"><b>【2025 複合陷阱分析】</b>",
        "此題包含兩個技術關鍵點：",
        "1. 模式 'w+'：這是一個「讀寫+自動建立」模式。即使 out.txt 不存在，open('out.txt', 'w+') 也會自動建立它，因此**不會**觸發 IOError。",
        "2. 變數錯誤 (NameError)：雖然檔案開啟成功，但如果 except 區塊使用了未定義的變數 (如 file_name)，在發生錯誤時會引發 NameError。但在正常流程下 (w+ 成功)，程式會順利執行 else 區塊。</code></pre>"
    ],
    70: [
        "<pre><code class="language-python"><b>【2025 報錯分析】</b>",
        "1. 第 03, 04 行：input() 回傳 str，這兩行語法本身正確，不會報錯。",
        "2. 第 02, 05 行：這是報錯主因。calc_power(base, exponent) 傳入的是兩個字串。在第 02 行執行 a ** b (即 str ** str) 時，Python 不支援字串的次方運算，會引發 <b>TypeError</b>。",
        "3. 修正：應在傳入前使用 eval()、int() 或 float() 將字串轉為數值。</code></pre>"
    ]
}

# Apply updates
updated_count = 0
for q in questions:
    if q['id'] in updates:
        q['explanation'] = updates[q['id']]
        updated_count += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)

print(f"Successfully patched {updated_count} questions with 2025 depth analysis.")
