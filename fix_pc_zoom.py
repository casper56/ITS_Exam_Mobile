import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 更新 drawLines：使用 viewBox 技術，這是解決縮放位移最穩定的方法
new_draw_lines = """
    window.drawLines = function() {
        const svg = document.getElementById('matching-svg');
        const wrapper = document.getElementById('matching-wrapper');
        if (!svg || !wrapper) return;
        
        const zoom = window.globalZoom || 1.0;
        const wrapperRect = wrapper.getBoundingClientRect();
        
        // 取得設計階段的原始寬高 (視覺寬高 / 縮放比例)
        const baseW = wrapperRect.width / zoom;
        const baseH = wrapperRect.height / zoom;
        
        // 設定 viewBox，讓 SVG 內部的單位自動與設計座標對齊
        svg.setAttribute('viewBox', `0 0 ${baseW} ${baseH}`);
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
                
                // 計算相對於 wrapper 左上角的視覺距離，並除以 zoom 還原為原始單位
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

# 2. 修正 CSS：確保 SVG 寬高撐滿容器，不再手動指定屬性
content = content.replace('#matching-svg {', '#matching-svg { width: 100%; height: 100%; ')

# 替換 drawLines 函式
content = re.sub(r'window\.drawLines = function\(\) \{.*?\}\s*;', new_draw_lines, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: PC-stable SVG alignment applied with viewBox.")
