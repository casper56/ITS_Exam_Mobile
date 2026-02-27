import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 使用更簡單的替換邏輯，避免正則表達式轉義問題
# 1. 更新 handleDragMove 
new_drag_move = """window.handleDragMove = function(e) {
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
    };"""

content = re.sub(r'window\.handleDragMove = function\(e\) \{.*?\}\s*;', new_drag_move, content, flags=re.DOTALL)

# 2. 更新 handleDragEnd 並移除 handleTargetDrop
new_drag_end = """window.handleDragEnd = function(e) {
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
    };"""

# 尋找並移除舊的 handleTargetDrop 與 handleDragEnd
content = re.sub(r'window\.handleTargetDrop = function\(e, rIdx\) \{.*?\}\s*;', '', content, flags=re.DOTALL)
content = re.sub(r'window\.handleDragEnd = function\(e\) \{.*?\}\s*;', new_drag_end, content, flags=re.DOTALL)

# 3. 更新右側選項渲染
new_right_render = """item.right.forEach((text, rIdx) => {
            const isMatchedByAny = currentAns.includes(rIdx);
            html += `<div class="match-item match-item-right ${isMatchedByAny?'matched':''}" id="right-item-${rIdx}" data-right-idx="${rIdx}">
                        <div class="match-dot" id="dot-right-${rIdx}"></div>
                        <div style="flex:1;">${text}</div>
                     </div>`;
        });"""

content = re.sub(r'item\.right\.forEach\(\(text, rIdx\) => \{.*?html \+= `<div class=\"match-item match-item-right.*?<\/div>`;\s*\}\);', new_right_render, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Patch applied.")
