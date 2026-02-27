import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修正 renderMatchingQuestion 函式
# 1. 補回導覽按鈕邏輯 (與 renderQuestion 同步)
# 2. 結尾套用目前的 globalZoom
new_matching_render_logic = """
    function renderMatchingQuestion(index) {
        window.scrollTo(0, 0); currentIndex = index; const item = quizData[index];
        const container = document.getElementById('question-container');
        
        // 修正：補回導覽按鈕邏輯
        document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';
        
        if (userAnswers[index] === undefined) userAnswers[index] = new Array(item.left.length).fill(null);
        const currentAns = userAnswers[index];
        const completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);

        let html = `<div class="card question-card">
            <div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizData.length}</span><span class="badge bg-info type-badge">配對題</span></div><div class="category-tag">${item.category || '一般'}</div></div>
            <div class="question-body" style="color:#333;">
                <div class="mb-5" style="font-weight:600; font-size:1.1rem;">${processContent(item.question, item)}</div>`;
        
        if (item.image) html += `<div class="text-center mb-5"><img src="${item.image}" class="q-img"></div>`;
        
        html += `<div class="matching-wrapper" id="matching-wrapper" onmousemove="handleDragMove(event)" onmouseup="handleDragEnd(event)" ontouchmove="handleDragMove(event)" ontouchend="handleDragEnd(event)">
                    <svg id="matching-svg"></svg>
                    <div class="matching-columns">
                        <div class="match-col left-col d-flex flex-column gap-4">`;
        item.left.forEach((text, lIdx) => {
            const isMatched = currentAns[lIdx] !== null;
            html += `<div class="match-item match-item-left ${isMatched?'matched':''}" id="left-item-${lIdx}">
                        <div style="flex:1;">${text}</div>
                        <div class="match-dot" id="dot-left-${lIdx}" 
                             onmousedown="handleDragStart(event, 'left', ${lIdx})" 
                             ontouchstart="handleDragStart(event, 'left', ${lIdx})"></div>
                     </div>`;
        });
        html += `</div>
                        <div class="match-col right-col d-flex flex-column gap-4">`;
        item.right.forEach((text, rIdx) => {
            const isMatchedByAny = currentAns.includes(rIdx);
            html += `<div class="match-item match-item-right ${isMatchedByAny?'matched':''}" id="right-item-${rIdx}" data-right-idx="${rIdx}">
                        <div class="match-dot" id="dot-right-${rIdx}"></div>
                        <div style="flex:1;">${text}</div>
                     </div>`;
        });
        html += `</div></div></div>`;
        
        if (!completed) {
            html += `<div class="text-center mt-5 mb-3 border-top pt-4">
                        <button class="btn btn-primary px-5 btn-lg" onclick="submitMatching()">確認完成配對並提交</button>
                        <p class="text-muted mt-2 small">按住左側圓點拖曳至右側圓點即可連線。點擊左側圓點可清除該行連線。</p>
                     </div>`;
        } else {
            html += `<div class="text-center mt-4 pt-3 border-top"><button class="btn btn-outline-primary px-4" id="toggle-exp-btn" onclick="toggleExplanation()">👁️ 顯示解析</button></div>
                     <div class="answer-section" id="ans-section" style="display:block;"><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div>`;
        }

        html += `</div></div></div>`;
        container.innerHTML = html;
        updateUI(); 
        if(window.Prism) Prism.highlightAll(); 
        saveState();
        
        // 修正：重新套用目前的縮放比例
        if (window.changeZoom) window.changeZoom(0);
        
        setTimeout(drawLines, 150);
    }
"""

content = re.sub(r'function renderMatchingQuestion\(index\) \{.*?setTimeout\(drawLines, 150\);\s*\}', new_matching_render_logic, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Fixed navigation button and zoom persistence in matching question.")
