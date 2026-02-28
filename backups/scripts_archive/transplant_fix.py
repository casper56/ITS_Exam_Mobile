import re

def transplant_practice_drawing_to_mock():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 這是練習區那套成功的繪圖邏輯 (改編為模擬考版)
    # 確保補償為 0 (網頁版需求)
    mock_web_drawing = """        // 繪製模擬考試報告中的正確連線 (參考練習區成功方案)
        setTimeout(() => {
            document.querySelectorAll('.print-matching').forEach(wrapper => {
                const idx = parseInt(wrapper.getAttribute('data-idx'));
                const item = examQuestions[idx];
                const svg = wrapper.querySelector('.print-svg');
                if (!svg) return;

                // 實作動態字寬偵測 (移植練習區成功經驗)
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
                    const dotL = document.getElementById(`mdl-${idx}-${lIdx}`);
                    const dotR = document.getElementById(`mdr-${idx}-${rIdx}`);
                    if (dotL && dotR) {
                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        // 0 補償精確圓心公式
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
        }, 2500);"""

    # 執行強力替換：將 submitExam 結尾處那段不穩定的繪圖邏輯替換掉
    pattern = r'// 繪製模擬考試報告中的正確連線.*?if\(window\.Prism\) Prism\.highlightAll\(\);\s+\}, 2000\);'
    content = re.sub(pattern, mock_web_drawing, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("MOCK Web Results restored using Practice Area logic.")

if __name__ == "__main__":
    transplant_practice_drawing_to_mock()
