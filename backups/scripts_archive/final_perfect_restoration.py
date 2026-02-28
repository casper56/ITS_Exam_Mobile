import re

def final_perfect_restoration():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修正 HTML 結構：加入 white-space:nowrap 防止程式碼片段換行
    pattern_html = r'let leftItems = item\.left\.map\(\(l, li\) => `<div class="match-item match-item-left".*?</div></div>`\)\.join\(''\);'
    fixed_html = 'let leftItems = item.left.map((l, li) => `<div class="match-item match-item-left" style="display:flex; align-items:center; justify-content:flex-start; min-height:40px; margin-bottom:10px;"><div class="q-text-part" style="font-family:Consolas,monospace; font-size:0.95rem; display:inline-block; text-align:right; white-space:nowrap !important;">${l}</div><div class="match-dot" id="pdl-${idx}-${li}" style="width:16px; height:16px; margin:0 10px; border:2px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div></div>`).join('');'
    content = re.sub(pattern_html, fixed_html, content)

    # 2. 修正 JS 繪圖邏輯：還原 0 補償公式，並補齊遺失的 y1 變數
    # 我們搜尋 L1345 到 L1365 之間的損壞區域並替換
    damaged_area_pattern = r'const x1 = rL\.left - wRect\.left \+ rL\.width/2 \+ 5; const x2 = rR\.left - wRect\.left \+ rR\.width/2 - 20; console\.log\("Web Drawing triggered"\);\s+const y2 = rR\.top - wRect\.top \+ rR\.height/2;'
    
    # 正確且完整的座標計算 (0 補償)
    perfect_logic = """const x1 = rL.left - wRect.left + rL.width/2;
                                                                            const y1 = rL.top - wRect.top + rL.height/2;
                                                                            const x2 = rR.left - wRect.left + rR.width/2;
                                                                            const y2 = rR.top - wRect.top + rR.height/2;"""
    
    content = re.sub(damaged_area_pattern, perfect_logic, content)

    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Final Perfect Restoration Applied: No-wrap, Full Coordinates, Zero Offset.")

if __name__ == "__main__":
    final_perfect_restoration()
