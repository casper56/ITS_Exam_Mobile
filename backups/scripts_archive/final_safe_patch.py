def final_safe_patch():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Practice Area HTML: Add white-space:nowrap
    content = content.replace('display:inline-block; text-align:right;">${l}</div>', 'display:inline-block; text-align:right; white-space:nowrap !important;">${l}</div>')

    # 2. Fix Mock Web Results: Add +120
    # Search for the specific coordinate line in submitExam
    content = content.replace('const x2 = rR.left - wRect.left + rR.width/2;', 'const x2 = rR.left - wRect.left + rR.width/2 + 120;')

    # 3. Fix Mock PDF: Add -20
    content = content.replace('// 基準點對齊修正: 還原為精確圓心對位 (模擬考無側邊欄干擾)
                        const x1 = rL.left - wRect.left + rL.width/2;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2;', 'const x1 = rL.left - wRect.left + rL.width/2 + 5; const y1 = rL.top - wRect.top + rL.height/2; const x2 = rR.left - wRect.left + rR.width/2 - 20;')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Safe Patch Applied.")

if __name__ == "__main__":
    final_safe_patch()
