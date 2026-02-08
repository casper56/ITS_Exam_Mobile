import json

def fix_id27_v2():
    path = 'www/ITS_Python/mock_exam.html'
    with open(path, 'rb') as f:
        data = f.read()
    
    start_tag = b'"id": 27,'
    start_idx = data.find(start_tag)
    if start_idx == -1:
        print("ID 27 not found")
        return
    
    cat_idx = data.find(b'"category"', start_idx)
    end_idx = data.find(b'}', cat_idx) + 1
    
    # 使用 Unicode 轉義表示所有中文
    # 27. 【CH03-6】你為學校設計了一個 Python 應用程式，在 classroom 的清單中包含了 60 位同學的姓名，最後 3 名是班上的幹部。<br>
    # 你需要分割清單內容顯示除了幹部以外的所有同學，你可以利用以下哪二個程式碼達成？<br>
    # 可以答成回答 Yes ， 不能回答回答 No
    q_text = "27. \u3010CH03-6\u3011\u4f60\u70ba\u5b78\u6821\u8a2d\u8a08\u4e86\u4e00\u500b Python \u61c9\u7528\u7a0b\u5f0f\uff0c\u5728 classroom \u7684\u6e05\u55ae\u4e2d\u5305\u542b\u4e86 60 \u4f4d\u540c\u5b78\u7684\u59d3\u540d\uff0c\u6700\u5f8c 3 \u540d\u662f\u73ed\u4e0a\u7684\u5e79\u90e8\u3002<br>\n\u4f60\u9700\u8981\u5206\u5272\u6e05\u55ae\u5167\u5bb9\u986f\u793a\u9664\u4e86\u5e79\u90e8\u4ee5\u5916\u7684\u6240\u6709\u540c\u5b78\uff0c\u4f60\u53ef\u4ee5\u5229\u7528\u4ee5\u4e0b\u54ea\u4e8c\u500b\u7a0b\u5f0f\u78bc\u9054\u6210\uff1f<br>\n\u53ef\u4ee5\u7b54\u6210\u56de\u7b54 Yes \uff0c \u4e0d\u80fd\u56de\u7b54\u56de\u7b54 No<pre><code class=\"language-python\">1. classroom[0: -2] = _(\u9078\u9805 1)_\n2. classroom[0: -3] = _(\u9078\u9805 2)_\n3. classroom[1: -3] = _(\u9078\u9805 3)_\n4. classroom[: -3] = _(\u9078\u9805 4)_\n5. classroom[1: -3] = _(\u9078\u9805 5)_</code></pre>"
    
    explanation = "\u25cf \u5728\u9019\u500b\u60c5\u6cc1\u4e0b\uff0c`classroom[0: -3]` \u548c `classroom[: -3]` \u90fd\u53ef\u4ee5\u6b63\u78ba\u5730\u53d6\u5f97\u9664\u4e86\u6700\u5f8c 3 \u540d\u540c\u5b78\u4ee5\u5916\u7684\u6240\u6709\u540c\u5b78\u3002<br>\n\u25cf \u56e0\u6b64\uff0c\u9078\u9805 2 \u548c\u9078\u9805 4 \u662f\u6b63\u78ba\u7684\u3002"
    
    category = "D1_\u8cc7\u6599\u578b\u5225\u8207\u904b\u7b97\u5b50"

    fixed_obj = {
        "id": 27,
        "type": "multioption",
        "question": q_text,
        "options": ["Yes|No", "Yes|No", "Yes|No", "Yes|No", "Yes|No"],
        "answer": [2, 1, 2, 1, 2],
        "weight": 1,
        "image": None,
        "explanation": explanation,
        "category": category
    }
    
    # 轉為 JSON 字串，並確保使用 \n 轉義而非實際換行
    fixed_json_str = json.dumps(fixed_obj, ensure_ascii=False)
    
    # 取代原始資料
    new_data = data[:start_idx-1] + b'{' + fixed_json_str.encode('utf-8') + b'}' + data[end_idx:]
    
    with open(path, 'wb') as f:
        f.write(new_data)
    print("Successfully fixed ID 27 JSON format.")

if __name__ == "__main__":
    fix_id27_v2()