import re

def fix_practice_matching_print():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修正 HTML 結構：確保「程式碼片段」不換行，且具備偵測用的 class
    # 尋找練習區 (prac_bottom_tmpl) 中的 matching HTML 生成
    old_html_pattern = r'let leftItems = item\.left\.map\(\(l, li\) => `<div class="match-item match-item-left".*?</div></div>`\)\.join\(''\);'
    new_html = 'let leftItems = item.left.map((l, li) => `<div class="match-item match-item-left" style="display:flex; align-items:center; justify-content:flex-start; min-height:40px; margin-bottom:10px;"><div class="q-text-part" style="font-family:Consolas,monospace; font-size:0.95rem; display:inline-block; text-align:right; white-space:nowrap;">${l}</div><div class="match-dot" id="pdl-${idx}-${li}" style="width:16px; height:16px; margin:0 10px; border:2px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div></div>`).join('');'
    content = re.sub(old_html_pattern, new_html, content)

    # 2. 修正 JS 繪圖邏輯：還原動態字寬偵測 + 座標 0 補償
    # 我們精確替換練習區專屬的繪圖區塊
    drawing_pattern = r'// 實作左側動態字寬偵測.*?setTimeout\(\(\) => \{ window\.print\(\);'
    
    new_drawing_logic = """// 實作左側動態字寬偵測 (要求：先偵測最長字串決定圓圈點)
                                                                    const leftParts = wrapper.querySelectorAll('.match-item-left .q-text-part');
                                                                    let maxW = 0;
                                                                    leftParts.forEach(p => {
                                                                        const w = p.getBoundingClientRect().width;
                                                                        if (w > maxW) maxW = w;
                                                                    });
                                                                    if (maxW > 0) {
                                                                        leftParts.forEach(p => p.style.width = (maxW + 2) + 'px');
                                                                    }

                                                                    const wRect = wrapper.getBoundingClientRect();
                                                                    if (wRect.width === 0) return;
                                                                    
                                                                    svg.setAttribute('width', wRect.width);
                                                                    svg.setAttribute('height', wRect.height);
                                                                    svg.style.width = wRect.width + 'px';
                                                                    svg.style.height = wRect.height + 'px';
                                                                    svg.innerHTML = ''; 
                                                                    
                                                                    const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
                                                                    answers.forEach((ansVal, lIdx) => {
                                                                        const rIdx = parseAnswerToIndex(ansVal);
                                                                        const dotL = document.getElementById(`pdl-${qIdx}-${lIdx}`);
                                                                        const dotR = document.getElementById(`pdr-${qIdx}-${rIdx}`);
                                                                        if (dotL && dotR) {
                                                                            const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                                                                            // 0 補償版本：完全參照圓圈座標中心
                                                                            const x1 = rL.left - wRect.left + rL.width/2;
                                                                            const y1 = rL.top - wRect.top + rL.height/2;
                                                                            const x2 = rR.left - wRect.left + rR.width/2;
                                                                            const y2 = rR.top - wRect.top + rR.height/2;
                                                                            
                                                                            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                                                                            line.setAttribute('x1', x1.toFixed(2)); line.setAttribute('y1', y1.toFixed(2)); 
                                                                            line.setAttribute('x2', x2.toFixed(2)); line.setAttribute('y2', y2.toFixed(2));
                                                                            line.setAttribute('stroke', "#198754"); line.setAttribute('stroke-width', "5"); 
                                                                            line.setAttribute('stroke-linecap', "round"); 
                                                                            line.setAttribute('style', "stroke-opacity:1 !important;");
                                                                            svg.appendChild(line);
                                                                        }
                                                                    });
                                                                    const html = svg.innerHTML; svg.innerHTML = ''; svg.innerHTML = html;
                                                                });
                                                                if(window.Prism) Prism.highlightAll(); 
                                                                setTimeout(() => { window.print();"""
    
    # 執行最終替換 (針對練習區)
    # 我們搜尋 L1300 附近的區段並替換
    content = re.sub(r'// 實作左側動態字寬偵測.*?if\(window\.Prism\) Prism\.highlightAll\(\); \s+setTimeout\(\(\) => \{ window\.print\(\);', new_drawing_logic, content, flags=re.DOTALL)

    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Practice Area fixed: No-wrap, Dynamic Width, and Lines restored.")

if __name__ == "__main__":
    fix_practice_matching_print()
