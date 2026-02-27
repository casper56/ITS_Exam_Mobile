import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定義一套完整且正確的配套函式
new_js_logic = """
    window.handleDragStart = function(e, side, idx) {
        if (side !== 'left') return;
        if (userAnswers[currentIndex] && userAnswers[currentIndex][idx] !== null) {
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

    window.handleDragMove = function(e) {
        if (!isDragging || !tempLine) return;
        const wrapper = document.getElementById('matching-wrapper');
        const rect = wrapper.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        
        window.lastClientX = clientX;
        window.lastClientY = clientY;

        const zoom = window.globalZoom || 1.0;
        const x2 = (clientX - rect.left) / zoom;
        const y2 = (clientY - rect.top) / zoom;
        
        tempLine.setAttribute('x2', x2);
        tempLine.setAttribute('y2', y2);
    };

    window.handleDragEnd = function(e) {
        if (!isDragging) return;
        const x = window.lastClientX;
        const y = window.lastClientY;
        const targetEl = document.elementFromPoint(x, y);
        const rightItem = targetEl ? targetEl.closest('.match-item-right') : null;

        if (rightItem) {
            const rIdx = parseInt(rightItem.getAttribute('data-right-idx'));
            userAnswers[currentIndex][dragStartPoint.lIdx] = rIdx;
        }
        finishDrag();
    };

    function finishDrag() {
        isDragging = false;
        dragStartPoint = null;
        if (tempLine && tempLine.parentNode) tempLine.parentNode.removeChild(tempLine);
        tempLine = null;
        renderMatchingQuestion(currentIndex);
    }

    window.drawLines = function() {
        const svg = document.getElementById('matching-svg');
        const wrapper = document.getElementById('matching-wrapper');
        if (!svg || !wrapper) return;
        svg.innerHTML = '';
        const zoom = window.globalZoom || 1.0;
        const rect = wrapper.getBoundingClientRect();
        
        svg.setAttribute('width', rect.width / zoom);
        svg.setAttribute('height', rect.height / zoom);

        const currentAns = userAnswers[currentIndex];
        if (!currentAns) return;
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

    window.submitMatching = function() {
        const item = quizData[currentIndex];
        const ans = userAnswers[currentIndex];
        if (!ans || ans.includes(null)) { alert("請完成所有配對後再提交！"); return; }
        
        const isCorrect = JSON.stringify(ans) === JSON.stringify(item.answer);
        if (isCorrect) correctSet.add(currentIndex); else incorrectSet.add(currentIndex);
        renderMatchingQuestion(currentIndex);
    };
"""

# 清除所有舊的、重複的配對題函式定義
# 我們從 renderMatchingQuestion 結束後開始清理，直到 parseAnswerToIndex 之前
pattern = re.compile(r'setTimeout\(drawLines, 150\);.*?function parseAnswerToIndex\(val\)', re.DOTALL)

def replacement(match):
    return "setTimeout(drawLines, 150);
    }
" + new_js_logic + "
    function parseAnswerToIndex(val)"

if pattern.search(content):
    new_content = pattern.sub(replacement, content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Cleaned up duplicate functions and restored correct logic.")
else:
    print("ERROR: Could not find target cleanup area.")
