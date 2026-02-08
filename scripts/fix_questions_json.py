import json
import os

def fix_questions_json():
    path = 'www/ITS_Python/questions_ITS_python.json'
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get("id") == 27:
            item["type"] = "multioption"
            item["question"] = (
                "27. 【CH03-6】你為學校設計了一個 Python 應用程式，在 classroom 的清單中包含了 60 位同學的姓名，最後 3 名是班上的幹部。<br>
"
                "你需要分割清單內容顯示除了幹部以外的所有同學，你可以利用以下哪二個程式碼達成？<br>
"
                "可以答成回答 Yes ， 不能回答回答 No<pre><code class="language-python">1. classroom[0: -2] = _(選項 1)_
"
                "2. classroom[0: -3] = _(選項 2)_
"
                "3. classroom[1: -3] = _(選項 3)_
"
                "4. classroom[: -3] = _(選項 4)_
"
                "5. classroom[1: -3] = _(選項 5)_</code></pre>"
            )
            item["options"] = ["Yes|No", "Yes|No", "Yes|No", "Yes|No", "Yes|No"]
            item["answer"] = [2, 1, 2, 1, 2]
            item["weight"] = 1
            item["image"] = None
            item["explanation"] = "● 在這個情況下，`classroom[0: -3]` 和 `classroom[: -3]` 都可以正確地取得除了最後 3 名同學以外的所有同學。<br>
● 因此，選項 2 和 選項 4 是正確的。"
            item["category"] = "D1_資料型別與運算子"
            found = True
            break
    
    if found:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Successfully fixed ID 27 in questions_ITS_python.json")
    else:
        print("ID 27 not found in questions_ITS_python.json")

if __name__ == "__main__":
    fix_questions_json()
