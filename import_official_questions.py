
import json
import os

# Load current data
json_path = 'www/ITS_Python/questions_ITS_python.json'
with open(json_path, 'r', encoding='utf-8') as f:
    questions = json.load(f)

current_max_id = max(q['id'] for i in [questions] for q in i)

new_questions = [
    {
        "id": current_max_id + 1,
        "type": "multiple",
        "category": "D0_官方鑑定考點",
        "question": [
            "<pre><code class="language-python">您正在建立一個電子商務指令碼來接受使用者輸入並以逗點分隔格式輸出資料。",
            "您撰寫了下列程式碼以接受輸入:",
            "item = input("Enter the item name: ")",
            "sales = int(input("Enter the quantity: "))",
            "",
            "輸出必須符合下列需求:",
            "⚫ 以雙引號括住字串。",
            "⚫ 不以引號或其他字元括住數字。",
            "⚫ 以逗點分隔項目。",
            "",
            "請問您應該使用哪兩個程式碼片段? (選擇兩項)</code></pre>"
        ],
        "options": [
            "<code>print("{0},{1}".format(item, sales))</code>",
            "<code>print(item + ',' + sales)</code>",
            "<code>print('"{0}", {1}'.format(item, sales))</code>",
            "<code>print('"' + item + '",', sales)</code>"
        ],
        "answer": ["C", "D"],
        "weight": 1,
        "explanation": [
            "<pre><code class="language-python">1. 需求：目標格式為 "ItemName", Quantity。",
            "2. 選項 C：'"{0}", {1}' 手動在 {0} 外加上雙引號，符合需求。",
            "3. 選項 D：print 使用逗號分隔參數時預設會加空格，'"' + item + '",' 串接後變成 "ItemName",，接著印出 sales，結果正確。</code></pre>"
        ]
    },
    {
        "id": current_max_id + 2,
        "type": "multioption",
        "category": "D0_官方鑑定考點",
        "question": [
            "<pre><code class="language-python">您建立了下列程式來找出會議室並顯示房間名稱。",
            "當輸入值 1 或 2 時，程式輸出為 Room does not exist.。",
            "01 rooms = {1: 'Foyer', 2: 'Conference Room'}",
            "02 room = input('Enter the room number: ')",
            "03 if not room in rooms:",
            "04    print('Room does not exist.')",
            "05 else:",
            "06    print("The room name is " + rooms[room])",
            "",
            "1. 請問第 01 行的 rooms 字典中儲存哪兩種資料類型？",
            "2. 請問第 02 行的 room 是哪種資料類型？",
            "3. 為什麼第 03 行無法尋找房間？</code></pre>"
        ],
        "options": [
            "<code>A.布林值和字串|B.浮點數和布林值|C.整數和字串|D.浮點數和整數</code>",
            "<code>A.bool|B.float|C.int|D.String</code>",
            "<code>A.無效的語法|B.不符合的資料型態|C.命名錯誤的變數</code>"
        ],
        "answer": ["C", "D", "B"],
        "weight": 1,
        "explanation": [
            "<pre><code class="language-python">1. 字典鍵 (Key) 1 是整數，值 (Value) 'Foyer' 是字串。",
            "2. input() 函式回傳的永遠是字串 (str)。",
            "3. 字典的鍵是整數 1，但 room 是字串 "1"，型態不匹配導致尋找失敗。</code></pre>"
        ]
    },
    {
        "id": current_max_id + 3,
        "type": "single",
        "category": "D0_官方鑑定考點",
        "question": [
            "<pre><code class="language-python">您撰寫了以下這段程式碼:",
            "import datetime",
            "d = datetime.datetime(2017, 4, 7)",
            "print('{:%B-%d-%y}'.format(d))",
            "請問輸出為何?</code></pre>"
        ],
        "options": [
            "<code>04-07-17</code>",
            "<code>2017-APRIL-07</code>",
            "<code>APRIL-07-17</code>",
            "<code>04-07-2017</code>"
        ],
        "answer": ["C"],
        "weight": 1,
        "explanation": [
            "<pre><code class="language-python">%B：完整的月份名稱（APRIL）。",
            "%d：兩位數日期（07）。",
            "%y：兩位數年份（17）。</code></pre>"
        ]
    },
    {
        "id": current_max_id + 4,
        "type": "multioption",
        "category": "D0_官方鑑定考點",
        "question": [
            "<pre><code class="language-python">請回答有關記錄 Python 程式碼的問題。",
            "1. 請問哪些字元代表單行文件字串 (Docstring) 的開頭和結尾?",
            "2. 在記錄函式時，文件字串的標準位置在哪裡?",
            "3. 假設有函式 cube(n)，哪個命令可列印其文件字串?</code></pre>"
        ],
        "options": [
            "<code>A. '|B. "|C. ""|D. """</code>",
            "<code>A.在檔案開頭|B.在函式定義後的第一行|C.在檔案結尾</code>",
            "<code>A.print(_doc_)|B.print(cube(doc))|C.print(cube.__doc__)|D.print(cube(docstring))</code>"
        ],
        "answer": ["D", "B", "C"],
        "weight": 1,
        "explanation": [
            "<pre><code class="language-python">1. Docstring 使用三個雙引號 """..."""。",
            "2. 根據 PEP 257，Docstring 位於函式定義後的第一行。",
            "3. 物件的內建屬性 __doc__ 儲存了文件字串。</code></pre>"
        ]
    },
    {
        "id": current_max_id + 5,
        "type": "single",
        "category": "D0_官方鑑定考點",
        "question": [
            "<pre><code class="language-python">您撰寫了以下這段程式碼:",
            "import sys",
            "print(sys.argv[2])",
            "",
            "執行下列命令: python Script.py Cheese Bacon Bread",
            "請問此命令的輸出為何?</code></pre>"
        ],
        "options": [
            "<code>Bread</code>",
            "<code>Cheese</code>",
            "<code>Script.py</code>",
            "<code>Bacon</code>"
        ],
        "answer": ["D"],
        "weight": 1,
        "explanation": [
            "<pre><code class="language-python">sys.argv 是清單：",
            "sys.argv[0] = 'Script.py'",
            "sys.argv[1] = 'Cheese'",
            "sys.argv[2] = 'Bacon'",
            "sys.argv[3] = 'Bread'</code></pre>"
        ]
    },
    {
        "id": current_max_id + 6,
        "type": "multioption",
        "category": "D0_官方鑑定考點",
        "question": [
            "<pre><code class="language-python">您需要測試某個物件是否為特定類別的執行個體。",
            "請完成下列單元測試程式碼：",
            "import _(1)_",
            "class TestIsInstance(_(2)_):",
            "    def _(3)_:",
            "        _(4)_",
            "if __name__ == '__main__':",
            "    unittest.main()</code></pre>"
        ],
        "options": [
            "<code>A.test|B.unittest</code>",
            "<code>A.unittest.TestCase|B.test.Test</code>",
            "<code>A.isInstance(self)|B.test_isInstance(self)</code>",
            "<code>A.self.assertIsInstance(obj, cls)|B.check(obj, cls)</code>"
        ],
        "answer": ["B", "A", "B", "A"],
        "weight": 1,
        "explanation": [
            "<pre><code class="language-python">1. 模組名為 unittest。",
            "2. 必須繼承自 unittest.TestCase。",
            "3. 測試方法必須以 test_ 開頭。",
            "4. 斷言方法為 assertIsInstance。</code></pre>"
        ]
    },
    {
        "id": current_max_id + 7,
        "type": "multioption",
        "category": "D0_官方鑑定考點",
        "question": [
            "<pre><code class="language-python">請選擇正確的 assert 方法以完成敘述：",
            "1. 若要測試變數 a 與 b 的「值」是否相同，請使用？",
            "2. 若要測試物件 a 與 b 是否為「同一個物件」，請使用？",
            "3. 若要測試「清單中是否存在某個值」，請使用？</code></pre>"
        ],
        "options": [
            "<code>assertEqual|assertTrue|assertIs|assertIn</code>",
            "<code>assertEqual|assertTrue|assertIs|assertIn</code>",
            "<code>assertEqual|assertTrue|assertIs|assertIn</code>"
        ],
        "answer": ["A", "C", "D"],
        "weight": 1,
        "explanation": [
            "<pre><code class="language-python">1. assertEqual 測試值 (==)。",
            "2. assertIs 測試物件身分 (is)。",
            "3. assertIn 測試成員關係 (in)。</code></pre>"
        ]
    },
    {
        "id": current_max_id + 8,
        "type": "multiple",
        "category": "D0_官方鑑定考點",
        "question": [
            "<pre><code class="language-python">您正在建立一個函式，將傳入函式的數字當作浮點數 (float) 值操作。",
            "此函式必須執行下列工作:",
            "⚫ 提取浮點數 (float) 的絕對值。",
            "⚫ 移除整數後面的任何小數點 (無條件捨去)。",
            "請問您應該使用哪兩個數學函式? (選擇兩項)</code></pre>"
        ],
        "options": [
            "<code>math.floor(x)</code>",
            "<code>math.fabs(x)</code>",
            "<code>math.frexp(x)</code>",
            "<code>math.fmod(x)</code>"
        ],
        "answer": ["A", "B"],
        "weight": 1,
        "explanation": [
            "<pre><code class="language-python">math.fabs(x) 回傳絕對值 (浮點數)。",
            "math.floor(x) 回傳小於或等於 x 的最大整數，達成移除小數點的效果。</code></pre>"
        ]
    }
]

questions.extend(new_questions)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)

print(f"Successfully inserted {len(new_questions)} official questions.")
