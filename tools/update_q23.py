import json

file_path = 'www/ITS_JAVA/questions_ITS_JAVA.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 23:
        q['type'] = "multimatching"
        q['question'] = [
            "<pre><code class=\"language-java\">【A-23】您要在不變更功能下，重寫下列程式碼。(行號僅供參考)",
            "01 showMenu();",
            "02 for( ; ; ){",
            "03     boolean n = newDeal();",
            "04     if (!n)",
            "05         break;",
            "06     showMenu();",
            "07 }",
            "",
            "請選擇下列適當的程式碼片段填入正確位置，來完成程式碼。",
            "",
            "    ___A___",
            " {",
            "    showMenu();",
            " }",
            "    ___B___",
            "</code></pre>"
        ]
        q['left'] = ["A 選項", "B 選項"]
        # 根據使用者要求，將選項填入 right 並以 | 分隔
        q['right'] = [
            "① } do; | ② do | ③ } break; | ④ while (newDeal())",
            "⑤ while (newDeal()); | ⑥ } | ⑦ } continue; | ⑧ continue"
        ]
        q['answer'] = ["B", "A"] # A對應②(B), B對應⑤(A)
        q['explanation'] = [
            "原始程式碼邏輯：先顯示一次選單，然後進入無限迴圈，每次判斷是否有新交易 (newDeal)，若無則跳出，若有則再顯示選單。這等同於「先執行一次，再判斷條件」的 do-while 結構。",
            "1. ___A___ 位於大括號前，應填入 ② do。",
            "2. ___B___ 位於結束大括號後，應填入 ⑤ while (newDeal());。"
        ]
        q['category'] = "控制流程"
        break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Successfully updated question ID 23.")
