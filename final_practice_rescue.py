import re

def final_practice_rescue():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. 重構練習區 HTML (prac_bottom_tmpl 內) ---
    # 將表格替換為 Flexbox，並加入 white-space: nowrap
    practice_matching_html = """                            if (item.type === 'matching') {
                                let leftItems = item.left.map((l, li) => `<div class="match-item match-item-left" style="display:flex; align-items:center; justify-content:flex-start; min-height:40px; margin-bottom:10px;"><div class="q-text-part" style="font-family:Consolas,monospace; font-size:0.95rem; display:inline-block; text-align:right; white-space:nowrap !important;">${l}</div><div class="match-dot" id="pdl-${idx}-${li}" style="width:16px; height:16px; margin:0 10px; border:2px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div></div>`).join('');
                                let rightItems = item.right.map((r, ri) => `<div class="match-item match-item-right" style="display:flex; align-items:center; justify-content:flex-start; min-height:40px; margin-bottom:10px;"><div class="match-dot" id="pdr-${idx}-${ri}" style="width:16px; height:16px; margin:0 10px; border:2px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div><div class="q-text-part" style="font-family:Consolas,monospace; font-size:0.95rem; display:inline-block; white-space:nowrap !important;">${r}</div></div>`).join('');
                                
                                optHtml = `<div class="matching-wrapper print-matching" id="print-match-${idx}" data-idx="${idx}" style="margin: 20px 0; position:relative; width:100%; display:block; border:1.5px solid #333; padding:15px; border-radius:4px; background:#fff;">
                                    <svg class="print-svg" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:10; overflow:visible; display:block;"></svg>
                                    <div class="matching-columns" style="display:flex !important; justify-content:flex-start !important; gap: 60px !important; position:relative; z-index:5;">
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
    
    # 替換掉原本的練習區表格生成邏輯
    content = re.sub(r'if \(item\.type === 'matching'\) \{.*?optHtml = `<div class="matching-wrapper print-matching".*?\}\s+else \{', practice_matching_html, content, flags=re.DOTALL)

    # --- 2. 修正練習區繪圖 JS (歸零補償) ---
    # 鎖定練習區座標計算區段，還原為 0 補償
    drawing_logic = """                                                                            const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                                                                            // 練習區最終修正：純粹圓心對位，不加任何偏移
                                                                            const x1 = rL.left - wRect.left + rL.width/2;
                                                                            const y1 = rL.top - wRect.top + rL.height/2;
                                                                            const x2 = rR.left - wRect.left + rR.width/2;
                                                                            const y2 = rR.top - wRect.top + rR.height/2;"""
    
    content = re.sub(r'const x1 = rL\.left - wRect\.left \+ rL\.width/2.*?;.*?const y2 = rR\.top - wRect\.top \+ rR\.height/2;', drawing_logic, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Practice Area fixed: Table removed, Flexbox added, Offsets cleared.")

if __name__ == "__main__":
    final_practice_rescue()
