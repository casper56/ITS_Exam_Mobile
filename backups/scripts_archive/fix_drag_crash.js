const fs = require('fs');
const path = 'final_clean_repair.py';
let content = fs.readFileSync(path, 'utf-8');

const newStart = `    window.handleDragStart = function(e, side, idx) {
        if (side !== 'left') return;
        if (userAnswers[currentIndex] && userAnswers[currentIndex][idx] !== null) { userAnswers[currentIndex][idx] = null; renderMatchingQuestion(currentIndex); }
        isDragging = true; if(e.cancelable) e.preventDefault();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        window.lastClientX = clientX; window.lastClientY = clientY;
        const dot = document.getElementById("dot-left-" + idx), rect = dot.getBoundingClientRect();
        const wrapperRect = document.getElementById("matching-wrapper").getBoundingClientRect();
        const zoom = window.itspyZoom || window.globalZoom || 1.0;
        dragStartPoint = { lIdx: idx, x: (rect.left + rect.width/2 - wrapperRect.left) / zoom, y: (rect.top + rect.height/2 - wrapperRect.top) / zoom };
        const svg = document.getElementById("matching-svg");
        tempLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
        tempLine.setAttribute("x1", dragStartPoint.x); tempLine.setAttribute("y1", dragStartPoint.y);
        tempLine.setAttribute("x2", dragStartPoint.x); tempLine.setAttribute("y2", dragStartPoint.y);
        tempLine.setAttribute("stroke", "#0d6efd"); tempLine.setAttribute("stroke-width", "2.5");
        tempLine.setAttribute("opacity", "0.6"); svg.appendChild(tempLine);
    };`;

const newEnd = `    window.handleDragEnd = function(e) {
        if (!isDragging) return;
        const x = window.lastClientX, y = window.lastClientY;
        if (typeof x === 'number' && typeof y === 'number' && !isNaN(x) && !isNaN(y)) {
            const targetEl = document.elementFromPoint(x, y), rightItem = targetEl ? targetEl.closest('.match-item-right') : null;
            if (rightItem) {
                const rIdx = parseInt(rightItem.getAttribute('data-right-idx'));
                if (!userAnswers[currentIndex]) userAnswers[currentIndex] = [];
                userAnswers[currentIndex][dragStartPoint.lIdx] = rIdx;
            }
        }
        isDragging = false; dragStartPoint = null;
        if (tempLine && tempLine.parentNode) tempLine.parentNode.removeChild(tempLine);
        tempLine = null; renderMatchingQuestion(currentIndex);
    };`;

// 執行替換
content = content.replace(/window\.handleDragStart = function\(e, side, idx\) \{[\s\S]*?\};/ , newStart);
content = content.replace(/window\.handleDragEnd = function\(e\) \{[\s\S]*?\};/ , newEnd);

fs.writeFileSync(path, content, 'utf-8');
console.log('SUCCESS: final_clean_repair.py fixed.');
