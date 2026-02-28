def final_rescue():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 錯誤的字串 (被誤改後的)
    broken_str = 'const x2 = rR.left - wRect.left + rR.width/2 + 120;'
    # 正確的字串 (答題模式專用)
    correct_str = 'const x2 = (rR.left + rR.width/2 - rect.left) / zoom;'
    
    # 為了防止全域誤改，我們只針對 drawLines 內部的區塊進行替換
    # 我們搜尋帶有 'y2 = (rR.top' 的那一行，那是答題模式的特徵
    
    # 執行精確替換
    updated = content.replace('const x2 = rR.left - wRect.left + rR.width/2 + 120; y2 = (rR.top + rR.height/2 - rect.top) / zoom;', 'const x2 = (rR.left + rR.width/2 - rect.left) / zoom; const y2 = (rR.top + rR.height/2 - rect.top) / zoom;')
    
    # 也捕捉另一種可能的變體
    updated = updated.replace('const x2 = rR.left - wRect.left + rR.width/2 + 120; const y2 = (rR.top + rR.height/2 - rect.top) / zoom;', 'const x2 = (rR.left + rR.width/2 - rect.left) / zoom; const y2 = (rR.top + rR.height/2 - rect.top) / zoom;')

    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(updated)
    print("Final Rescue: All Zoom formulas recovered.")

if __name__ == "__main__":
    final_rescue()
