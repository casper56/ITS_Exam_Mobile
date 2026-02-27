import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修正 CSS：強化標題與圓圈視覺
css_update = """
        .matching-wrapper { position: relative; margin: 20px 0; padding: 15px; user-select: none; }
        .match-header-row { display: flex; justify-content: space-between; margin-bottom: 25px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
        .match-header-title { flex: 1; font-weight: bold; color: #666; font-size: 1.1rem; }
        .match-header-left { text-align: left; padding-left: 10px; }
        .match-header-right { text-align: left; padding-left: 55px; } /* 對齊右側圓點 */
        
        .matching-columns { display: flex; justify-content: space-between; gap: 40px; position: relative; z-index: 2; }
        .match-col { flex: 1; display: flex; flex-direction: column; gap: 30px; }
        
        .match-item { display: flex; align-items: center; min-height: 40px; cursor: pointer; transition: all 0.2s; }
        .match-item-left { justify-content: flex-end; }
        .match-item-right { justify-content: flex-start; }
        
        /* 1:1 復刻圓點視覺 (⦿) */
        .match-dot {
            width: 22px; height: 22px;
            border: 1.5px solid #333; border-radius: 50%;
            margin: 0 15px; display: flex; align-items: center; justify-content: center;
            background: #fff; position: relative; flex-shrink: 0;
        }
        .match-dot::after {
            content: ""; width: 10px; height: 10px;
            background: transparent; border-radius: 50%; transition: all 0.1s;
        }
        /* 答對或選取時顯示黑色內芯 */
        .match-item.matched .match-dot::after, .match-item.selected .match-dot::after { background: #333; }
        .match-item.selected .match-dot { border-color: #0d6efd; box-shadow: 0 0 8px rgba(13,110,253,0.3); }
        
        #matching-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
"""
# 替換舊的配對題 CSS
content = re.sub(r'/\* 完全復刻配對題樣式 \*/.*?#matching-svg \{.*?\}', '/* 完全復刻配對題樣式 */' + css_update, content, flags=re.DOTALL)

# 2. 更新 renderMatchingQuestion：加入標題標頭
new_matching_render = """
    function renderMatchingQuestion(index) {
        currentIndex = index; const item = quizData[index];
        const container = document.getElementById('question-container');
        
        if(document.getElementById('side-btn-prev')) document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';
        if (userAnswers[index] === undefined) userAnswers[index] = new Array(item.left.length).fill(null);
        const currentAns = userAnswers[index];
        const completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);

        let html = `<div class="card question-card">
            <div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizData.length}</span><span class="badge bg-info type-badge">配對題</span></div><div class="category-tag">${item.category || '一般'}</div></div>
            <div class="question-body" style="color:#000;">
                <div class="mb-4" style="font-weight:600; font-size:1.1rem;">${processContent(item.question, item)}</div>`;
        
        html += `<div class="matching-wrapper" id="matching-wrapper" onmousemove="handleDragMove(event)" onmouseup="handleDragEnd(event)" ontouchmove="handleDragMove(event)" ontouchend="handleDragEnd(event)">
                    <!-- 標題標頭 -->
                    <div class="match-header-row">
                        <div class="match-header-title match-header-left">程式碼片段</div>
                        <div class="match-header-title match-header-right">回答區</div>
                    </div>
                    <svg id="matching-svg"></svg>
                    <div class="matching-columns">
                        <div class="match-col left-col">`;
        item.left.forEach((text, lIdx) => {
            const isMatched = currentAns[lIdx] !== null;
            html += `<div class="match-item match-item-left ${isMatched?'matched':''}" id="left-item-${lIdx}">
                        <div style="font-family:Consolas,monospace;">${text}</div>
                        <div class="match-dot" id="dot-left-${lIdx}" onmousedown="handleDragStart(event, 'left', ${lIdx})" ontouchstart="handleDragStart(event, 'left', ${lIdx})"></div>
                     </div>`;
        });
        html += `</div><div class="match-col right-col">`;
        item.right.forEach((text, rIdx) => {
            const isMatchedByAny = currentAns.includes(rIdx);
            html += `<div class="match-item match-item-right ${isMatchedByAny?'matched':''}" id="right-item-${rIdx}" data-right-idx="${rIdx}">
                        <div class="match-dot" id="dot-right-${rIdx}"></div>
                        <div style="font-family:sans-serif;">${text}</div>
                     </div>`;
        });
        html += `</div></div></div>`;
        
        if (!completed) {
            html += `<div class="text-center mt-5 mb-3 border-top pt-4">
                        <button class="btn btn-primary px-5 btn-lg" onclick="submitMatching()">確認完成配對並提交</button>
                        <p class="text-muted mt-2 small">操作指引：按住左側圓點拖曳至右側選項即可連線。點擊左側圓點可重選。</p>
                     </div>`;
        } else {
            html += `<div class="text-center mt-4 pt-3 border-top"><button class="btn btn-outline-primary px-4" id="toggle-exp-btn" onclick="toggleExplanation()">👁️ 顯示解析</button></div>
                     <div class="answer-section" id="ans-section" style="display:block;"><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div>`;
        }

        html += `</div></div></div>`;
        container.innerHTML = html;
        updateUI(); saveState();
        if (window.changeZoom) window.changeZoom(0);
        setTimeout(drawLines, 150);
    }
"""

content = re.sub(r'function renderMatchingQuestion\(index\) \{.*?setTimeout\(drawLines, 150\);\s*\}', new_matching_render, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: PC Matching Layout enhanced with headers and improved dots.")
