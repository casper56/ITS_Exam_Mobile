import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修正 CSS，加入 touch-action: none
css_old = r'\.matching-wrapper \{'
css_new = '.matching-wrapper { touch-action: none; '
content = re.sub(css_old, css_new, content)

# 2. 全面修正 JavaScript 中的座標計算 (除以 globalZoom)
js_patch = """
    window.handleDragStart = function(e, side, idx) {
        if (side !== 'left') return;
        if (userAnswers[currentIndex][idx] !== null) {
            userAnswers[currentIndex][idx] = null;
            renderMatchingQuestion(currentIndex);
        }

        isDragging = true;
        const dot = document.getElementById(`dot-left-${idx}`);
        const rect = dot.getBoundingClientRect();
        const wrapperRect = document.getElementById('matching-wrapper').getBoundingClientRect();
        const zoom = window.globalZoom || 1.0;
        
        dragStartPoint = {
            lIdx: idx,
            x: (rect.left + rect.width/2 - wrapperRect.left) / zoom,
            y: (rect.top + rect.height/2 - wrapperRect.top) / zoom
        };

        const svg = document.getElementById('matching-svg');
        tempLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
        tempLine.setAttribute('x1', dragStartPoint.x);
        tempLine.setAttribute('y1', dragStartPoint.y);
        tempLine.setAttribute('x2', dragStartPoint.x);
        tempLine.setAttribute('y2', dragStartPoint.y);
        tempLine.setAttribute('stroke', '#0d6efd');
        tempLine.setAttribute('stroke-width', '2.5');
        tempLine.setAttribute('opacity', '0.6');
        svg.appendChild(tempLine);
    };

    window.drawLines = function() {
        const svg = document.getElementById('matching-svg');
        const wrapper = document.getElementById('matching-wrapper');
        if (!svg || !wrapper) return;
        svg.innerHTML = '';
        const zoom = window.globalZoom || 1.0;
        const rect = wrapper.getBoundingClientRect();
        
        // 重要：SVG 的畫布屬性也必須除以縮放比例
        svg.setAttribute('width', rect.width / zoom);
        svg.setAttribute('height', rect.height / zoom);

        const currentAns = userAnswers[currentIndex];
        currentAns.forEach((rIdx, lIdx) => {
            if (rIdx === null) return;
            const dotL = document.getElementById(`dot-left-${lIdx}`);
            const dotR = document.getElementById(`dot-right-${rIdx}`);
            if (dotL && dotR) {
                const rectL = dotL.getBoundingClientRect();
                const rectR = dotR.getBoundingClientRect();
                
                const x1 = (rectL.left + rectL.width/2 - rect.left) / zoom;
                const y1 = (rectL.top + rectL.height/2 - rect.top) / zoom;
                const x2 = (rectR.left + rectR.width/2 - rect.left) / zoom;
                const y2 = (rectR.top + rectR.height/2 - rect.top) / zoom;

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

# 替換 handleDragStart 和 drawLines 函式
content = re.sub(r'window\.handleDragStart = function\(e, side, idx\) \{.*?\}\s*;', js_patch, content, flags=re.DOTALL)
content = re.sub(r'window\.drawLines = function\(\) \{.*?\}\s*;', '', content, flags=re.DOTALL) # 移除舊的 drawLines

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Coordinate compensation for zoom applied.")
