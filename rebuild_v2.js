const fs = require('fs');
const path = 'www/ITS_Python/ITS_Python.html';
if (!fs.existsSync(path)) process.exit(1);

let content = fs.readFileSync(path, 'utf-8');

// 準備新的腳本內容
const newScript = `
<script>
    let currentIndex = 0;
    let correctSet = new Set(), incorrectSet = new Set(), correctedSet = new Set(), userAnswers = {}; 
    window.itspyZoom = 1.0;
    
    window.changeZoom = function(delta) {
        window.itspyZoom = Math.round((window.itspyZoom + delta) * 10) / 10;
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

    function parseAnswerToIndex(val) {
        if (typeof val === 'number') return val - 1;
        if (typeof val === 'string') {
            const v = val.toUpperCase();
            if (v === 'Y') return 0; if (v === 'N') return 1;
            const code = v.charCodeAt(0);
            if (code >= 65 && code <= 90) return code - 65;
            return parseInt(val) - 1;
        }
        return -1;
    }

    function renderMatchingQuestion(index) {
        currentIndex = index; const item = quizData[index];
        const container = document.getElementById('question-container');
        if(document.getElementById('side-btn-prev')) document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';
        
        if (userAnswers[index] === undefined) userAnswers[index] = new Array(item.left.length).fill(null);
        const currentAns = userAnswers[index];
        const completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);

        let html = `<div class="card question-card">
            <div class="question-header"><div><span class="badge bg-primary me-2">題目 \${index + 1} / \${quizData.length}</span><span class="badge bg-info type-badge">配對題</span></div><div class="category-tag">\${item.category || '一般'}</div></div>
            <div class="question-body" style="color:#333;">
                <div class="mb-4" style="font-weight:600; font-size:1.1rem;">\${processContent(item.question, item)}</div>`;
        
        html += `<div class="matching-wrapper" id="matching-wrapper" onmousemove="handleDragMove(event)" onmouseup="handleDragEnd(event)" ontouchmove="handleDragMove(event)" ontouchend="handleDragEnd(event)">
                    <div class="match-header-row" style="display:flex; justify-content:space-between; margin-bottom:20px; border-bottom:1px solid #eee; padding-bottom:10px;">
                        <div style="font-weight:bold; color:#666;">程式碼片段</div>
                        <div style="font-weight:bold; color:#666; padding-right:150px;">回答區</div>
                    </div>
                    <svg id="matching-svg" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:1;"></svg>
                    <div class="matching-columns" style="display:flex; justify-content:flex-start; gap:120px; position:relative; z-index:2; padding-left:10px;">
                        <div class="match-col left-col" style="display:flex; flex-direction:column; gap:25px; min-width:200px;">`;
        item.left.forEach((text, lIdx) => {
            const isMatched = currentAns[lIdx] !== null;
            html += `<div class="match-item match-item-left \${isMatched?'matched':''}" id="left-item-\${lIdx}" style="display:flex; align-items:center; min-height:45px; justify-content:flex-end;">
                        <div style="font-family:Consolas,monospace; font-size:1.1rem;">\${text}</div>
                        <div class="match-dot" id="dot-left-\${lIdx}" onmousedown="handleDragStart(event, 'left', \${lIdx})" ontouchstart="handleDragStart(event, 'left', \${lIdx})" 
                             style="width:22px; height:22px; border:1.5px solid #333; border-radius:50%; margin:0 15px; display:flex; align-items:center; justify-content:center; background:#fff; position:relative; flex-shrink:0; cursor:pointer;">
                             <div style="width:10px; height:10px; border-radius:50%; background:\${isMatched?'#333':'transparent'};"></div>
                        </div>
                     </div>`;
        });
        html += `</div><div class="match-col right-col" style="display:flex; flex-direction:column; gap:25px; min-width:200px;">`;
        item.right.forEach((text, rIdx) => {
            const isMatchedByAny = currentAns.includes(rIdx);
            html += `<div class="match-item match-item-right \${isMatchedByAny?'matched':''}" id="right-item-\${rIdx}" data-right-idx="\${rIdx}" style="display:flex; align-items:center; min-height:45px;">
                        <div class="match-dot" id="dot-right-\${rIdx}" style="width:22px; height:22px; border:1.5px solid #333; border-radius:50%; margin:0 15px; display:flex; align-items:center; justify-content:center; background:#fff; position:relative; flex-shrink:0;">
                             <div style="width:10px; height:10px; border-radius:50%; background:\${isMatchedByAny?'#333':'transparent'};"></div>
                        </div>
                        <div style="font-size:1.1rem;">\${text}</div>
                     </div>`;
        });
        html += `</div></div></div>`;
        
        if (!completed) {
            html += `<div class="text-center mt-5 mb-3 border-top pt-4">
                        <button class="btn btn-primary px-5 btn-lg" onclick="submitMatching()">確認完成配對並提交</button>
                     </div>`;
        } else {
            html += `<div class="answer-section" style="display:block;"><div class="explanation">\${processContent(item.explanation || '暫無解析。', item)}</div></div>`;
        }
        html += `</div></div></div>`;
        container.innerHTML = html;
        updateUI(); saveState();
        if (window.changeZoom) window.changeZoom(0);
        setTimeout(drawLines, 100);
    }

    let isDragging = false, dragStartPoint = null, tempLine = null;
    window.handleDragStart = function(e, side, idx) {
        if (side !== 'left') return;
        if (userAnswers[currentIndex] && userAnswers[currentIndex][idx] !== null) { userAnswers[currentIndex][idx] = null; renderMatchingQuestion(currentIndex); }
        isDragging = true; if(e.cancelable) e.preventDefault();
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
        isDragging = false; dragStartPoint = null;
        if (tempLine && tempLine.parentNode) tempLine.parentNode.removeChild(tempLine);
        tempLine = null; renderMatchingQuestion(currentIndex);
    };

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
                line.setAttribute('stroke', "#0d6efd"); line.setAttribute('stroke-width', "2.5");
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
        let typeLabel = opts.some(o => String(o).includes('|')) ? "題組" : (item.type === 'multiple' ? "複選" : "單選");
        container.innerHTML = `<div class="card question-card"><div class="question-header"><div><span class="badge bg-primary me-2">題目 \${index + 1} / \${quizData.length}</span><span class="badge bg-info type-badge">\${typeLabel}</span></div><div class="category-tag">\${item.category || '一般'}</div></div><div class="question-body"><div>\${processContent(item.question, item)}</div>\${item.image ? `<img src="\${item.image}" class="q-img">` : ''}<div class="options-area"></div><div class="text-center mt-4 pt-3 border-top"><button class="btn btn-outline-primary px-4" id="toggle-exp-btn" onclick="toggleExplanation()">👁️ 顯示答案 / 解析</button></div><div class="answer-section" id="ans-section"><div class="explanation">\${processContent(item.explanation || '暫無解析。', item)}</div></div></div></div>`;
        const optionsArea = container.querySelector('.options-area');
        const saved = userAnswers[index];
        const completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);
        const cIdxs = Array.isArray(item.answer) ? item.answer.map(parseAnswerToIndex) : [parseAnswerToIndex(item.answer)];
        opts.forEach((optStr, optIdx) => {
            if (String(optStr).includes('|')) {
                const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                const displayLabel = item["question" + alphabet[optIdx]] || `選項 \${optIdx + 1}`;
                let sHtml = `<div class="mt-2 mb-1"><code>\${displayLabel}</code></div><div class="d-flex flex-wrap gap-2">`;
                optStr.split('|').forEach((s, subIdx) => { 
                    sHtml += `<div class="sub-opt-container p-2 border rounded bg-light" onclick="checkSubAnswer(this, \${index}, \${optIdx}, \${subIdx}, event)" style="cursor:pointer; font-size:0.9rem"><input class="form-check-input" type="radio" name="q\${index}_opt\${optIdx}" id="o\${optIdx}_s\${subIdx}"> \${s}</div>`; 
                });
                optionsArea.innerHTML += sHtml + '</div></div>';
            } else {
                const div = document.createElement('div'); div.className = 'option-item p-3 mb-2 border rounded'; div.onclick = (e) => checkAnswer(div, index, optIdx, e);
                const input = document.createElement('input'); input.type = item.type === 'multiple' ? 'checkbox' : 'radio'; input.name = 'q' + index; input.id = 'o' + optIdx; input.className = 'form-check-input me-2';
                if (saved !== undefined && (Array.isArray(saved) ? saved.includes(optIdx) : saved === optIdx)) input.checked = true;
                if (completed) { input.disabled = true; if (cIdxs.includes(optIdx)) div.classList.add('correct'); else if (input.checked) div.classList.add('incorrect'); }
                const label = document.createElement('label'); label.innerHTML = String.fromCharCode(65 + optIdx) + '. ' + optStr;
                div.appendChild(input); div.appendChild(label); optionsArea.appendChild(div);
            }
        });
        if (completed) document.getElementById('ans-section').style.display = 'block';
        if (window.changeZoom) window.changeZoom(0);
        Prism.highlightAll();
    }

    function checkAnswer(element, qIdx, optIdx, event) {
        const item = quizData[qIdx]; if (correctSet.has(qIdx) || correctedSet.has(qIdx)) return;
        const isMultiple = item.type === 'multiple';
        const input = element.querySelector('input');
        if (event.target !== input) input.checked = !input.checked;
        if (isMultiple) {
            const checked = Array.from(document.querySelectorAll('input[name="q'+qIdx+'"]:checked')).map(i => parseInt(i.id.replace('o','')));
            userAnswers[qIdx] = checked;
        } else {
            userAnswers[qIdx] = optIdx;
            evaluateCurrentQuestion();
        }
        saveState(); updateUI();
    }

    function checkSubAnswer(element, qIdx, optIdx, subIdx, event) {
        if (!userAnswers[qIdx]) userAnswers[qIdx] = {};
        userAnswers[qIdx][optIdx] = subIdx;
        const input = element.querySelector('input'); input.checked = true;
        evaluateCurrentQuestion(); saveState(); updateUI();
    }

    function evaluateCurrentQuestion() {
        const item = quizData[currentIndex]; const qIdx = currentIndex;
        const saved = userAnswers[qIdx]; if (!saved) return;
        let isCorrect = false;
        if (item.type === 'matching') return; // matching has its own submit
        if (item.type === 'multiple') {
            const ans = Array.isArray(item.answer) ? item.answer.map(parseAnswerToIndex) : [parseAnswerToIndex(item.answer)];
            isCorrect = saved.length === ans.length && saved.every(v => ans.includes(v));
        } else if (typeof saved === 'object') {
            isCorrect = Object.keys(saved).length === (item.quiz || item.options).length && Object.keys(saved).every(k => parseAnswerToIndex(item.answer[k]) === saved[k]);
        } else {
            isCorrect = parseAnswerToIndex(item.answer) === saved;
        }
        if (isCorrect) correctSet.add(qIdx); else incorrectSet.add(qIdx);
    }

    function toggleExplanation(forceShow = null) { const el = document.getElementById('ans-section'); if (!el) return; const isShow = (forceShow !== null) ? forceShow : (el.style.display !== 'block'); el.style.display = isShow ? 'block' : 'none'; }
    function jumpTo(idx) { renderQuestion(idx); const modal = bootstrap.Modal.getInstance(document.getElementById('gridModal')); if (modal) modal.hide(); }
    const SUBJECT_ID = 'itspy', CORR_KEY = SUBJECT_ID + '_correct_v1', INCORR_KEY = SUBJECT_ID + '_incorrect_v1', CORR_EDIT_KEY = SUBJECT_ID + '_corrected_v1', INDEX_KEY = SUBJECT_ID + '_index_v1', ANSWERS_KEY = SUBJECT_ID + '_answers_v1';
    function loadState() { try { const sCorr = localStorage.getItem(CORR_KEY), sIncorr = localStorage.getItem(INCORR_KEY), sEdit = localStorage.getItem(CORR_EDIT_KEY), sIdx = localStorage.getItem(INDEX_KEY), sAns = localStorage.getItem(ANSWERS_KEY); if (sCorr) correctSet = new Set(JSON.parse(sCorr)); if (sIncorr) incorrectSet = new Set(JSON.parse(sIncorr)); if (sEdit) correctedSet = new Set(JSON.parse(sEdit)); if (sIdx) currentIndex = parseInt(sIdx) || 0; if (sAns) userAnswers = JSON.parse(sAns); } catch(e) {} }
    function saveState() { try { localStorage.setItem(CORR_KEY, JSON.stringify([...correctSet])); localStorage.setItem(INCORR_KEY, JSON.stringify([...incorrectSet])); localStorage.setItem(CORR_EDIT_KEY, JSON.stringify([...correctedSet])); localStorage.setItem(INDEX_KEY, currentIndex.toString()); localStorage.setItem(ANSWERS_KEY, JSON.stringify(userAnswers)); } catch(e) {} }
    function updateUI() {
        const stats = document.getElementById('progress-stats'); if (stats) stats.innerHTML = `✅\${correctSet.size} ❌\${incorrectSet.size} 🟠\${correctedSet.size} <span class="ms-1 small" style="opacity:0.7">/ \${quizData.length}</span>`;
        const grid = document.getElementById('progress-grid'); grid.innerHTML = '';
        quizData.forEach((_, i) => {
            const n = document.createElement('div'); n.className = 'q-node'; if (i === currentIndex) n.classList.add('active');
            if (incorrectSet.has(i)) n.classList.add('incorrect'); else if (correctedSet.has(i)) n.classList.add('corrected'); else if (correctSet.has(i)) n.classList.add('correct');
            n.innerText = i + 1; n.onclick = () => jumpTo(i); grid.appendChild(n);
        });
    }
    function processContent(content, item) { if (!content) return ''; const lines = Array.isArray(content) ? content : [String(content)]; return lines.join('
'); }
    loadState(); window.addEventListener('resize', () => { if(window.drawLines) window.drawLines(); }); renderQuestion(currentIndex);
</script>
`;

// 替換
const startMarker = '<script>';
const endMarker = '</script>';
const startIndex = content.lastIndexOf(startMarker); // 抓最後一個 script 標籤 (邏輯區)
const endIndex = content.lastIndexOf(endMarker);

if (startIndex !== -1 && endIndex !== -1) {
    const newContent = content.substring(0, startIndex) + newScript + content.substring(endIndex + endMarker.length);
    fs.writeFileSync(path, newContent, 'utf-8');
    console.log('SUCCESS: JS Rebuilt via Node.js');
} else {
    console.log('ERROR: Script tags not found');
}
