import os

def absolute_fix():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. 修正 練習區 HTML 結構 (確保不斷行) ---
    old_html = 'let leftItems = item.left.map((l, li) => `<div class="match-item match-item-left" style="display:flex; align-items:center; justify-content:flex-start; min-height:40px; margin-bottom:10px;"><div class="q-text-part" style="font-family:Consolas,monospace; font-size:0.95rem; display:inline-block; text-align:right;">${l}</div>'
    new_html = 'let leftItems = item.left.map((l, li) => `<div class="match-item match-item-left" style="display:flex; align-items:center; justify-content:flex-start; min-height:40px; margin-bottom:10px;"><div class="q-text-part" style="font-family:Consolas,monospace; font-size:0.95rem; display:inline-block; text-align:right; white-space:nowrap !important;">${l}</div>'
    content = content.replace(old_html, new_html)

    # --- 2. 徹底重寫 練習區繪圖區塊 (補齊 y1, 歸零補償) ---
    # 我們鎖定 setTimeout 這一整塊繪圖邏輯
    start_marker = "// 實作左側動態字寬偵測"
    end_marker = "if(window.Prism) Prism.highlightAll();"
    
    # 這是最正確的、完全參照圓圈的邏輯
    replacement_logic = """// 實作左側動態字寬偵測 (要求：先偵測最長字串決定圓圈點)
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
                                                                            // 0 補償版本：完全參照圓圈座標中心，修正 y1 缺失問題
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
                                                                """
    
    # 尋找舊的、損壞的邏輯區塊
    import re
    final_content = re.sub(r'// 實作左側動態字寬偵測.*?if\(window\.Prism\) Prism\.highlightAll\(\);', replacement_logic + "                                                                if(window.Prism) Prism.highlightAll();", content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("SUCCESS: Practice area restored to stable state.")

if __name__ == "__main__":
    absolute_fix()
