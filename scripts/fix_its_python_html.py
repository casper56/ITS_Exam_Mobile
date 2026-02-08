import json
import os

def fix_its_python_html():
    path = 'www/ITS_Python/ITS_Python.html'
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    with open(path, 'rb') as f:
        data = f.read()
    
    # 定位 ID 27
    start_tag = b'"id": 27,'
    start_idx = data.find(start_tag)
    if start_idx == -1:
        print("ID 27 not found in ITS_Python.html")
        return
    
    # 定位物件結束
    end_marker = b'}, {"id": 28'
    end_idx = data.find(end_marker, start_idx)
    if end_idx == -1:
        end_idx = data.find(b'}]', start_idx) + 1
    
    # 構造正確的 ID 27 資料
    q_text = (
        "27. 【CH03-6】你為學校設計了一個 Python 應用程式，在 classroom 的清單中包含了 60 位同學的姓名，最後 3 名是班上的幹部。<br>\n"
        "你需要分割清單內容顯示除了幹部以外的所有同學，你可以利用以下哪二個程式碼達成？<br>\n"
        "可以答成回答 Yes ， 不能回答回答 No<pre><code class=\"language-python\">1. classroom[0: -2] = _(選項 1)_\n"
        "2. classroom[0: -3] = _(選項 2)_\n"
        "3. classroom[1: -3] = _(選項 3)_\n"
        "4. classroom[: -3] = _(選項 4)_\n"
        "5. classroom[1: -3] = _(選項 5)_</code></pre>"
    )
    explanation = (
        "● 在這個情況下，`classroom[0: -3]` 和 `classroom[: -3]` 都可以正確地取得除了最後 3 名同學以外的所有同學。<br>\n"
        "● 因此，選項 2 和 選項 4 是正確的。"
    )
    
    fixed_obj = {
        "id": 27,
        "type": "multioption",
        "question": q_text,
        "options": ["Yes|No", "Yes|No", "Yes|No", "Yes|No", "Yes|No"],
        "answer": [2, 1, 2, 1, 2],
        "weight": 1,
        "image": None,
        "explanation": explanation,
        "category": "D1_資料型別與運算子"
    }
    
    fixed_json = json.dumps(fixed_obj, ensure_ascii=False)
    
    # 執行取代
    new_data = data[:start_idx-1] + b'{' + fixed_json.encode('utf-8') + data[end_idx:]
    
    with open(path, 'wb') as f:
        f.write(new_data)
    print("Successfully fixed ID 27 in ITS_Python.html")

if __name__ == "__main__":
    fix_its_python_html()