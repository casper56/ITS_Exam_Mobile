import re

def fix_only_print_report():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. 還原「練習區答題介面」(renderMatchingQuestion) ---
    # 確保答題介面的「回答區」標題與結構不被干擾
    content = content.replace('style="width: 80px !important; white-space: nowrap !important; display: inline-block !important; text-align: left;"', '')

    # --- 2. 修正「預覽列印報告」(prepareAndPrint 內部) ---
    
    # A. 確保 HTML 不斷行
    # 針對 prepareAndPrint 生成的 leftItems
    content = content.replace('text-align:right; white-space:nowrap !important;">${l}</div>', 'text-align:right; white-space:nowrap !important; overflow:visible;">${l}</div>')
    
    # B. 徹底修正座標計算 (移除 +120, +5 等所有人工偏移，還原 y1)
    # 鎖定練習區預覽專用的 pdl- / pdr- 區塊
    content = re.sub(
        r'const x1 = rL\.left - wRect\.left \+ rL\.width/2 \+ 5; const x2 = rR\.left - wRect\.left \+ rR\.width/2 - 20; console\.log\("Web Drawing triggered"\);\s+const y2 = rR\.top - wRect\.top \+ rR\.height/2;',
        'const x1 = rL.left - wRect.left + rL.width/2; const y1 = rL.top - wRect.top + rL.height/2; const x2 = rR.left - wRect.left + rR.width/2; const y2 = rR.top - wRect.top + rR.height/2;',
        content
    )
    
    # 也要捕捉可能已經被改過的 +120 或 -20 版本
    content = re.sub(
        r'const x2 = rR\.left - wRect\.left \+ rR\.width/2 \+ 120;',
        'const x2 = rR.left - wRect.left + rR.width/2;',
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("FIXED: Interactive screen restored. Print report logic corrected.")

if __name__ == "__main__":
    fix_only_print_report()
