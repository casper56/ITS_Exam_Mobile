import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修正 CSS：確保縮放按鈕 z-index 極高，且 matching-wrapper 不會剪裁連線
content = re.sub(r'#zoom-controls\s*\{.*?\}', '#zoom-controls { position: fixed; bottom: 85px; right: 20px; z-index: 2147483647; display: flex; flex-direction: column; gap: 12px; pointer-events: auto; }', content, flags=re.DOTALL)
content = content.replace('.matching-wrapper { touch-action: pan-y pinch-zoom; position: relative; margin: 30px 0; padding: 10px; }', 
                         '.matching-wrapper { touch-action: pan-y pinch-zoom; position: relative; margin: 30px 0; padding: 10px; z-index: 10; overflow: visible !important; }')

# 2. 移除 renderMatchingQuestion 中的跳轉 scrollTo，並優化呼叫順序
content = content.replace('window.scrollTo(0, 0); currentIndex = index;', 'currentIndex = index;')

# 3. 升級 drawLines 邏輯：解決縮放後線條偏移的核心 math
new_draw_lines = """
    window.drawLines = function() {
        const svg = document.getElementById('matching-svg');
        const wrapper = document.getElementById('matching-wrapper');
        if (!svg || !wrapper) return;
        
        const zoom = window.globalZoom || 1.0;
        const wrapperRect = wrapper.getBoundingClientRect();
        
        // 強制 SVG 內部座標系與 wrapper 同步 (不除以 zoom 以維持 1:1)
        svg.setAttribute('width', wrapperRect.width / zoom);
        svg.setAttribute('height', wrapperRect.height / zoom);
        svg.innerHTML = '';

        const currentAns = userAnswers[currentIndex];
        if (!currentAns) return;
        
        currentAns.forEach((rIdx, lIdx) => {
            if (rIdx === null) return;
            const dotL = document.getElementById("dot-left-" + lIdx);
            const dotR = document.getElementById("dot-right-" + rIdx);
            if (dotL && dotR) {
                const rectL = dotL.getBoundingClientRect();
                const rectR = dotR.getBoundingClientRect();
                
                // 計算相對於 wrapper 的原始座標 (排除縮放帶來的視覺位移)
                const x1 = (rectL.left + rectL.width/2 - wrapperRect.left) / zoom;
                const y1 = (rectL.top + rectL.height/2 - wrapperRect.top) / zoom;
                const x2 = (rectR.left + rectR.width/2 - wrapperRect.left) / zoom;
                const y2 = (rectR.top + rectR.height/2 - wrapperRect.top) / zoom;

                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute('x1', x1); line.setAttribute('y1', y1);
                line.setAttribute('x2', x2); line.setAttribute('y2', y2);
                line.setAttribute('stroke', '#0d6efd');
                line.setAttribute('stroke-width', '2.5');
                svg.appendChild(line);
            }
        });
    };
"""

# 替換 drawLines 函式
content = re.sub(r'window\.drawLines = function\(\) \{.*?\}\s*;', new_draw_lines, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Fixed line misalignment and removed jumpy scroll.")
