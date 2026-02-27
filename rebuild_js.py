import os

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 尋找 script 標籤之後的穩定起點 (我們保留 quizData 之後的部分)
# 這裡我們用一個保守的點進行切割
marker = 'let currentSelection = { side: null, index: null };'
parts = content.split(marker)

if len(parts) > 1:
    # 我們保留前半部 (包含 CSS 與 quizData)，重寫後半部 JS 邏輯
    head_part = parts[0]
    
    new_js_logic = """let currentSelection = { side: null, index: null };
    window.itspyZoom = 1.0;
    window.changeZoom = function(delta) {
        window.itspyZoom = (Math.round((window.itspyZoom + delta) * 10) / 10);
        if (window.itspyZoom < 0.6) window.itspyZoom = 0.6;
        if (window.itspyZoom > 2.5) window.itspyZoom = 2.5;
        const container = document.getElementById('question-container');
        if (container) {
            container.style.transform = "scale(" + window.itspyZoom + ")";
            container.style.transformOrigin = "top center";
            if (window.itspyZoom > 1.0) container.style.marginBottom = ((window.itspyZoom - 1.0) * 100) + "%";
            else container.style.marginBottom = "0";
            if (typeof window.drawLines === 'function') window.drawLines();
        }
    };

    function renderMatchingQuestion(index) {
        currentIndex = index; const item = quizData[index];
        const container = document.getElementById('question-container');
        if(document.getElementById('side-btn-prev')) document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';
        if (userAnswers[index] === undefined) userAnswers[index] = new Array(item.left.length).fill(null);
        const currentAns = userAnswers[index];
        const completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);

        let html = `<div class="card question-card">
            <div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizData.length}</span><span class="badge bg-info type-badge">配對題</span></div><div class="category-tag">${item.category || '一般'}</div></div>
            <div class="question-body" style="color:#333;">
                <div class="mb-4" style="font-weight:600; font-size:1.1rem;">${processContent(item.question, item)}</div>`;
        
        html += `<div class="matching-wrapper" id="matching-wrapper" onmousemove="handleDragMove(event)" onmouseup="handleDragEnd(event)" ontouchmove="handleDragMove(event)" ontouchend="handleDragEnd(event)">
                    <div class="match-header-row">
                        <div class="match-header-title match-header-left">程式碼片段</div>
                        <div class="match-header-title match-header-right">回答區</div>
                    </div>
                    <svg id="matching-svg" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:1;"></svg>
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
                        <div>${text}</div>
                     </div>`;
        });
        html += `</div></div></div>`;
        
        if (!completed) {
            html += `<div class="text-center mt-5 mb-3 border-top pt-4">
                        <button class="btn btn-primary px-5 btn-lg" onclick="submitMatching()">確認提交</button>
                     </div>`;
        } else {
            html += `<div class="answer-section" style="display:block;"><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div>`;
        }
        html += `</div></div></div>`;
        container.innerHTML = html;
        updateUI(); saveState();
        if (window.changeZoom) window.changeZoom(0);
        setTimeout(drawLines, 100);
    }

    window.handleDragStart = function(e, side, idx) {
        if (side !== 'left') return;
        if (userAnswers[currentIndex] && userAnswers[currentIndex][idx] !== null) {
            userAnswers[currentIndex][idx] = null;
            renderMatchingQuestion(currentIndex);
        }
        isDragging = true;
        const dot = document.getElementById("dot-left-" + idx);
        const rect = dot.getBoundingClientRect();
        const wrapperRect = document.getElementById("matching-wrapper").getBoundingClientRect();
        const zoom = window.itspyZoom || 1.0;
        dragStartPoint = { lIdx: idx, x: (rect.left + rect.width/2 - wrapperRect.left) / zoom, y: (rect.top + rect.height/2 - wrapperRect.top) / zoom };
        const svg = document.getElementById("matching-svg");
        tempLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
        tempLine.setAttribute("x1", dragStartPoint.x); tempLine.setAttribute("y1", dragStartPoint.y);
        tempLine.setAttribute("x2", dragStartPoint.x); tempLine.setAttribute("y2", dragStartPoint.y);
        tempLine.setAttribute("stroke", "#0d6efd"); tempLine.setAttribute("stroke-width", "2.5");
        tempLine.setAttribute("opacity", "0.6"); svg.appendChild(tempLine);
    };

    window.handleDragMove = function(e) {
        if (!isDragging || !tempLine) return;
        const wrapper = document.getElementById('matching-wrapper');
        const rect = wrapper.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        window.lastClientX = clientX; window.lastClientY = clientY;
        const zoom = window.itspyZoom || 1.0;
        const x2 = (clientX - rect.left) / zoom;
        const y2 = (clientY - rect.top) / zoom;
        tempLine.setAttribute('x2', x2); tempLine.setAttribute('y2', y2);
    };

    window.handleDragEnd = function(e) {
        if (!isDragging) return;
        const x = window.lastClientX; const y = window.lastClientY;
        const targetEl = document.elementFromPoint(x, y);
        const rightItem = targetEl ? targetEl.closest('.match-item-right') : null;
        if (rightItem) {
            const rIdx = parseInt(rightItem.getAttribute('data-right-idx'));
            if (!userAnswers[currentIndex]) userAnswers[currentIndex] = [];
            userAnswers[currentIndex][dragStartPoint.lIdx] = rIdx;
        }
        finishDrag();
    };

    function finishDrag() {
        isDragging = false; dragStartPoint = null;
        if (tempLine && tempLine.parentNode) tempLine.parentNode.removeChild(tempLine);
        tempLine = null; renderMatchingQuestion(currentIndex);
    }

    window.drawLines = function() {
        const svg = document.getElementById('matching-svg');
        const wrapper = document.getElementById('matching-wrapper');
        if (!svg || !wrapper) return;
        const zoom = window.itspyZoom || 1.0;
        const rect = wrapper.getBoundingClientRect();
        svg.setAttribute('width', rect.width / zoom);
        svg.setAttribute('height', rect.height / zoom);
        svg.innerHTML = '';
        const currentAns = userAnswers[currentIndex];
        if (!currentAns) return;
        currentAns.forEach((rIdx, lIdx) => {
            if (rIdx === null) return;
            const dotL = document.getElementById("dot-left-" + lIdx);
            const dotR = document.getElementById("dot-right-" + rIdx);
            if (dotL && dotR) {
                const rL = dotL.getBoundingClientRect(); const rR = dotR.getBoundingClientRect();
                const x1 = (rL.left + rL.width/2 - rect.left) / zoom;
                const y1 = (rL.top + rL.height/2 - rect.top) / zoom;
                const x2 = (rR.left + rR.width/2 - rect.left) / zoom;
                const y2 = (rR.top + rR.height/2 - rect.top) / zoom;
                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute('x1', x1); line.setAttribute('y1', y1);
                line.setAttribute('x2', x2); line.setAttribute('y2', y2);
                line.setAttribute('stroke', '#0d6efd'); line.setAttribute('stroke-width', '2.5');
                svg.appendChild(line);
            }
        });
    };

    window.submitMatching = function() {
        const item = quizData[currentIndex];
        const ans = userAnswers[currentIndex];
        if (!ans || ans.includes(null)) { alert("請完成所有配對！"); return; }
        const isCorrect = JSON.stringify(ans) === JSON.stringify(item.answer);
        if (isCorrect) correctSet.add(currentIndex); else incorrectSet.add(currentIndex);
        renderMatchingQuestion(currentIndex);
    };

    function renderQuestion(index) {
        currentIndex = index; const item = quizData[index];
        if (item.type === 'matching') { renderMatchingQuestion(index); return; }
        const container = document.getElementById('question-container');
        if(document.getElementById('side-btn-prev')) document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';
        let opts = Array.isArray(item.quiz || item.options) ? (item.quiz || item.options) : [item.quiz || item.options];
        let typeLabel = opts.some(o => String(o).includes('|')) ? "下拉選單" : (item.type === 'multiple' ? "複選題" : "單選題");
        container.innerHTML = `<div class="card question-card"><div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizData.length}</span><span class="badge bg-info type-badge">${typeLabel}</span></div><div class="category-tag">${item.category || '一般'}</div></div><div class="question-body"><div>${processContent(item.question, item)}</div>${item.image ? `<img src="${item.image}" class="q-img">` : ''}<div class="options-area"></div><div class="text-center mt-4 pt-3 border-top"><button class="btn btn-outline-primary px-4" id="toggle-exp-btn" onclick="toggleExplanation()">👁️ 顯示解析</button></div><div class="answer-section" id="ans-section"><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div></div></div>`;
        const optionsArea = container.querySelector('.options-area');
        const saved = userAnswers[index];
        const completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);
        const cIdxs = Array.isArray(item.answer) ? item.answer.map(parseAnswerToIndex) : [parseAnswerToIndex(item.answer)];
        opts.forEach((optStr, optIdx) => {
            if (String(optStr).includes('|')) {
                const subOpts = optStr.split('|');
                const select = document.createElement('select'); select.className = 'form-select mb-3'; select.onchange = (e) => { userAnswers[index] = userAnswers[index] || []; userAnswers[index][optIdx] = e.target.value; saveState(); };
                const defaultOpt = document.createElement('option'); defaultOpt.text = '請選擇回答'; defaultOpt.value = ''; select.add(defaultOpt);
                subOpts.forEach(so => { const o = document.createElement('option'); o.text = so; o.value = so; if (saved && saved[optIdx] === so) o.selected = true; select.add(o); });
                if (completed) { select.disabled = true; select.classList.add(saved && saved[optIdx] === item.answer[optIdx] ? 'is-valid' : 'is-invalid'); }
                optionsArea.appendChild(select);
            } else {
                const div = document.createElement('div'); div.className = 'option-item p-3 mb-2 border rounded';
                const input = document.createElement('input'); input.type = item.type === 'multiple' ? 'checkbox' : 'radio'; input.name = 'q' + index; input.id = 'o' + optIdx; input.className = 'form-check-input me-2'; input.onchange = () => { if (item.type === 'multiple') { const checked = Array.from(container.querySelectorAll('input:checked')).map(i => parseInt(i.id.replace('o',''))); userAnswers[index] = checked; } else { userAnswers[index] = optIdx; } saveState(); };
                if (saved !== undefined && (Array.isArray(saved) ? saved.includes(optIdx) : saved === optIdx)) input.checked = true;
                if (completed) { input.disabled = true; if (cIdxs.includes(optIdx)) div.classList.add('correct'); else if (input.checked) div.classList.add('incorrect'); }
                const label = document.createElement('label'); label.htmlFor = 'o' + optIdx; label.innerHTML = String.fromCharCode(65 + optIdx) + '. ' + optStr;
                div.appendChild(input); div.appendChild(label); optionsArea.appendChild(div);
            }
        });
        if (completed) document.getElementById('ans-section').style.display = 'block';
        if (window.changeZoom) window.changeZoom(0);
        Prism.highlightAll();
    }

    function toggleExplanation() { const s = document.getElementById('ans-section'); s.style.display = s.style.display === 'none' ? 'block' : 'none'; }
    function jumpTo(i) { renderQuestion(i); const modal = bootstrap.Modal.getInstance(document.getElementById('gridModal')); if (modal) modal.hide(); }
    function loadState() { const s = localStorage.getItem('its_py_state'); if (s) { const data = JSON.parse(s); userAnswers = data.userAnswers || []; correctSet = new Set(data.correctSet || []); incorrectSet = new Set(data.incorrectSet || []); correctedSet = new Set(data.correctedSet || []); currentIndex = data.currentIndex || 0; } }
    function saveState() { localStorage.setItem('its_py_state', JSON.stringify({ userAnswers, correctSet: Array.from(correctSet), incorrectSet: Array.from(incorrectSet), correctedSet: Array.from(correctedSet), currentIndex })); }
    function updateUI() {
        const grid = document.getElementById('q-grid'); grid.innerHTML = '';
        quizData.forEach((_, i) => {
            const n = document.createElement('div'); n.className = 'grid-item';
            if (incorrectSet.has(i)) n.classList.add('incorrect'); else if (correctedSet.has(i)) n.classList.add('corrected'); else if (correctSet.has(i)) n.classList.add('correct');
            n.innerText = i + 1; n.onclick = () => jumpTo(i); grid.appendChild(n);
        });
    }
    loadState(); renderQuestion(currentIndex);
</script>
</body>
</html>"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(head_part + new_js_logic)
    print("SUCCESS: Full JS logic rewrite completed.")
else:
    print("ERROR: Marker not found.")
