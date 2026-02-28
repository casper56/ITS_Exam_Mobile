import re

def apply_clean_patch():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修正 練習區 HTML 不斷行
    content = content.replace('display:inline-block; text-align:right;">${l}</div>', 'display:inline-block; text-align:right; white-space:nowrap !important;">${l}</div>')

    # 2. 修正 練習區繪圖邏輯 (確保連線恢復，補齊 y1，移除補償)
    # 我們鎖定 L1300 附近的座標區段
    broken_pattern = r'const x1 = rL\.left - wRect\.left \+ rL\.width/2 \+ 5; const x2 = rR\.left - wRect\.left \+ rR\.width/2 - 20; console\.log\("Web Drawing triggered"\);\s+const y2 = rR\.top - wRect\.top \+ rR\.height/2;'
    correct_logic = 'const x1 = rL.left - wRect.left + rL.width/2; const y1 = rL.top - wRect.top + rL.height/2; const x2 = rR.left - wRect.left + rR.width/2; const y2 = rR.top - wRect.top + rR.height/2;'
    
    # 如果 L1300 的內容已經被 git checkout 還原成舊的
    if 'const x1 = rL.left - wRect.left + rL.width/2;' in content:
        print("Standard practice formula already present.")
    else:
        content = re.sub(broken_pattern, correct_logic, content)

    # 3. 確保 模擬考分離補償邏輯 正確植入
    # 網頁版 +120
    content = content.replace('// 網頁顯示: 純粹圓心對位，不加補償
                        const x2 = rR.left - wRect.left + rR.width/2;', '// 網頁顯示: 補償 +120px
                        const x2 = rR.left - wRect.left + rR.width/2 + 120;')
    # PDF 版 -20
    content = content.replace('// 基準點對齊修正: 還原為精確圓心對位 (模擬考無側邊欄干擾)
                        const x1 = rL.left - wRect.left + rL.width/2;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2;', '// 基準點對齊修正: PDF 版 -20px
                        const x1 = rL.left - wRect.left + rL.width/2 + 5;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2 - 20;')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Clean Patch Applied Successfully.")

if __name__ == "__main__":
    apply_clean_patch()
