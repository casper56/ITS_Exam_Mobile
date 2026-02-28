import re

def final_practice_rescue_v2():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. 重構練習區 HTML (prac_bottom_tmpl 內) ---
    # 我們精確抓取 if (item.type === 'matching') 區塊
    # 這是我們要植入的 Flexbox 結構
    new_html = r"""                            if (item.type === 'matching') {
                                let leftItems = item.left.map((l, li) => `<div class="match-item match-item-left" style="display:flex; align-items:center; justify-content:flex-start; min-height:40px; margin-bottom:10px;"><div class="q-text-part" style="font-family:Consolas,monospace; font-size:0.95rem; display:inline-block; text-align:right; white-space:nowrap !important;">${l}</div><div class="match-dot" id="pdl-${idx}-${li}" style="width:16px; height:16px; margin:0 10px; border:2px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div></div>`).join('');
                                let rightItems = item.right.map((r, ri) => `<div class="match-item match-item-right" style="display:flex; align-items:center; justify-content:flex-start; min-height:40px; margin-bottom:10px;"><div class="match-dot" id="pdr-${idx}-${ri}" style="width:16px; height:16px; margin:0 10px; border:2px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div><div class="q-text-part" style="font-family:Consolas,monospace; font-size:0.95rem; display:inline-block; white-space:nowrap !important;">${r}</div></div>`).join('');
                                
                                optHtml = `<div class="matching-wrapper print-matching" id="print-match-${idx}" data-idx="${idx}" style="margin: 20px 0; position:relative; width:100%; display:block; border:1.5px solid #333; padding:15px; border-radius:4px; background:#fff;">
                                    <svg class="print-svg" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:10; overflow:visible; display:block;"></svg>
                                    <div class="matching-columns" style="display:flex !important; justify-content:flex-start !important; gap: 40px !important; position:relative; z-index:5;">
                                        <div class="match-col left-col" style="flex:none; display:flex; flex-direction:column; align-items:flex-end;">
                                            <div style="font-weight:bold; color:#0d6efd; margin-bottom:15px; border-bottom:1.5px solid #333; padding-bottom:5px; font-size:1.1rem; width:100%; text-align:left;">程式碼片段</div>
                                            ${leftItems}
                                        </div>
                                        <div class="match-col right-col" style="flex:none; display:flex; flex-direction:column; align-items:flex-start;">
                                            <div style="font-weight:bold; color:#0d6efd; margin-bottom:15px; border-bottom:1.5px solid #333; padding-bottom:5px; font-size:1.1rem; width:100%; text-align:left;">正確對應回答</div>
                                            ${rightItems}
                                        </div>
                                    </div>
                                </div>`;
                            } else {"""

    # 替換 L1270 附近的舊代碼
    # 使用一段固定的特徵字串作為替換基準
    old_fragment = r"if (item.type === 'matching') {"
    # 我們找到 prepareAndPrint 內部的那個 matching 判斷
    parts = content.split("let optHtml = "";")
    if len(parts) > 2: # 索引 2 通常是練習區的 prepareAndPrint
        sub_parts = parts[2].split("} else {")
        if len(sub_parts) > 1:
            # 替換第一個 if 塊
            sub_parts[0] = new_html
            parts[2] = "} else {".join(sub_parts)
            content = "let optHtml = "";".join(parts)

    # --- 2. 修正練習區繪圖 JS (歸零補償) ---
    content = re.sub(r'const x1 = rL\.left - wRect\.left \+ rL\.width/2 \+ 5; const x2 = rR\.left - wRect\.left \+ rR\.width/2 - 20; console\.log\("Web Drawing triggered"\);\s+const y2 = rR\.top - wRect\.top \+ rR\.height/2;', 
                     'const x1 = rL.left - wRect.left + rL.width/2; const y1 = rL.top - wRect.top + rL.height/2; const x2 = rR.left - wRect.left + rR.width/2; const y2 = rR.top - wRect.top + rR.height/2;', 
                     content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Practice Area fixed: Table layout replaced with Flexbox.")

if __name__ == "__main__":
    final_practice_rescue_v2()
