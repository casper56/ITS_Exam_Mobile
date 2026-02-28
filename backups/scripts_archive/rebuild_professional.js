const fs = require('fs');
const path = 'final_clean_repair.py';
let content = fs.readFileSync(path, 'utf-8');

const goldenJS = `prac_bottom = r""";
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

    function processContent(content, item) {
        if (!content) return '';
        let html = Array.isArray(content) ? content.join('
') : String(content);
        return html.replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
            const src = item['image' + p1] || item['image' + parseInt(p1, 10)] || item.image;
            return src ? `<img src="\${src}" class="q-img">` : match;
        });
    }

    function renderMatchingQuestion(index) {
        currentIndex = index; const item = quizData[index];
        const container = document.getElementById('question-container');
        if(document.getElementById('side-btn-prev')) document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';
        
        if (userAnswers[index] === undefined) userAnswers[index] = new Array(item.left.length).fill(null);
        const currentAns = userAnswers[index];
        const isCorrect = correctSet.has(index);
        const isCorrected = correctedSet.has(index);
        const isWrong = incorrectSet.has(index);
        const completed = isCorrect || isCorrected;

        let html = `<div class="card question-card">
            <div class="question-header"><div><span class="badge bg-primary me-2">題目 \${index + 1} / \${quizData.length}</span><span class="badge \${completed ? (isCorrected ? 'bg-warning' : 'bg-success') : (isWrong ? 'bg-danger' : 'bg-info')} type-badge">\${isCorrected ? '更正題' : (isWrong ? '答錯題' : (isCorrect ? '答對題' : '配對題'))}</span></div><div class="category-tag">\${item.category || '一般'}</div></div>
            <div class="question-body" style="color:#333;">
                <div class="mb-4" style="font-weight:600; font-size:1.1rem;">\${processContent(item.question, item)}</div>`;
        
        if (isWrong && !completed) html += `<div class="alert alert-danger py-2 small mb-3">❌ 答案不正確，請檢查連線後再次提交。</div>`;

        html += `<div class="matching-wrapper" id="matching-wrapper" onmousemove="handleDragMove(event)" onmouseup="handleDragEnd(event)" ontouchmove="handleDragMove(event)" ontouchend="handleDragEnd(event)">
                    <div class="match-header-row">
                        <div class="match-header-title">程式碼片段</div>
                        <div class="match-header-title">回答區</div>
                    </div>
                    <svg id="matching-svg"></svg>
                    <div class="matching-columns">
                        <div class="match-col left-col">`;
        item.left.forEach((text, lIdx) => {
            const isMatched = currentAns[lIdx] !== null;
            const dotColor = completed ? (isCorrected ? '#fd7e14' : '#198754') : (isWrong ? '#dc3545' : (isMatched ? '#333' : 'transparent'));
            html += `<div class="match-item match-item-left \${isMatched?'matched':''}" id="left-item-\${lIdx}"><div style="font-family:Consolas,monospace;">\${text}</div><div class="match-dot" id="dot-left-\${lIdx}" onmousedown="\${completed?'':`handleDragStart(event, 'left', \${lIdx})`}" ontouchstart="\${completed?'':`handleDragStart(event, 'left', \${lIdx})`}"><div style="width:10px; height:10px; border-radius:50%; background:\${dotColor};"></div></div></div>`;
        });
        html += `</div><div class="match-col right-col">`;
        item.right.forEach((text, rIdx) => {
            const isMatchedByAny = currentAns.includes(rIdx);
            const dotColor = completed ? (isCorrected ? '#fd7e14' : '#198754') : (isWrong ? '#dc3545' : (isMatchedByAny ? '#333' : 'transparent'));
            html += `<div class="match-item match-item-right \${isMatchedByAny?'matched':''}" id="right-item-\${rIdx}" data-right-idx="\${rIdx}"><div class="match-dot" id="dot-right-\${rIdx}"><div style="width:10px; height:10px; border-radius:50%; background:\${dotColor};"></div></div><div>\${text}</div></div>`;
        });
        html += `</div></div></div>`;
        
        if (!completed) html += `<div class="text-center mt-5 mb-3 border-top pt-4"><button class="btn btn-primary px-5 btn-lg" onclick="submitMatching()">確認提交</button></div>`;
        else {
            const ansText = item.answer.join(', ');
            html += `<div class="answer-section" style="display:block;">
                        <div class="fw-bold mb-2 \${isCorrected?'text-warning':'text-success'}">\${isCorrected?'🟠 已更正成功！':'✅ 答對了！'}</div>
                        <div class="review-ans" style="margin: 10px 0;">正確答案：\${ansText}</div>
                        <div class="explanation">\${processContent(item.explanation || '暫無解析。', item)}</div>
                     </div>`;
        }
        html += `</div></div></div>`;
        container.innerHTML = html; updateUI(); saveState();
        window.changeZoom(0); setTimeout(drawLines, 100);
        if(window.Prism) Prism.highlightAll();
    }

    let isDragging = false, dragStartPoint = null, tempLine = null;
    window.handleDragStart = function(e, side, idx) {
        if (side !== 'left') return;
        if (userAnswers[currentIndex] && userAnswers[currentIndex][idx] !== null) { userAnswers[currentIndex][idx] = null; renderMatchingQuestion(currentIndex); }
        isDragging = true; if(e.cancelable) e.preventDefault();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        window.lastClientX = clientX; window.lastClientY = clientY;
        const dot = document.getElementById("dot-left-" + idx), rect = dot.getBoundingClientRect();
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
        const wrapper = document.getElementById('matching-wrapper'), rect = wrapper.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX, clientY = e.touches ? e.touches[0].clientY : e.clientY;
        window.lastClientX = clientX; window.lastClientY = clientY;
        const zoom = window.itspyZoom || 1.0;
        tempLine.setAttribute('x2', (clientX - rect.left) / zoom); tempLine.setAttribute('y2', (clientY - rect.top) / zoom);
    };

    window.handleDragEnd = function(e) {
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
    };

    window.drawLines = function() {
        const svg = document.getElementById('matching-svg'), wrapper = document.getElementById('matching-wrapper');
        if (!svg || !wrapper) return;
        const zoom = window.itspyZoom || 1.0, rect = wrapper.getBoundingClientRect();
        const baseW = rect.width / zoom, baseH = rect.height / zoom;
        svg.setAttribute('viewBox', `0 0 \${baseW} \${baseH}`);
        svg.innerHTML = ''; const currentAns = userAnswers[currentIndex]; if (!currentAns) return;
        currentAns.forEach((rIdx, lIdx) => {
            if (rIdx === null) return;
            const dotL = document.getElementById("dot-left-" + lIdx), dotR = document.getElementById("dot-right-" + rIdx);
            if (dotL && dotR) {
                const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                const x1 = (rL.left + rL.width/2 - rect.left) / zoom, y1 = (rL.top + rL.height/2 - rect.top) / zoom;
                const x2 = (rR.left + rR.width/2 - rect.left) / zoom, y2 = (rR.top + rR.height/2 - rect.top) / zoom;
                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute('x1', x1); line.setAttribute('y1', y1);
                line.setAttribute('x2', x2); line.setAttribute('y2', y2);
                line.setAttribute('stroke', "#0d6efd"); line.setAttribute('stroke-width', "2.5"); svg.appendChild(line);
            }
        });
    };

    window.submitMatching = function() {
        const item = quizData[currentIndex], ans = userAnswers[currentIndex];
        if (!ans || ans.includes(null)) { alert("請完成配對!"); return; }
        const letters = ans.map(idx => String.fromCharCode(65 + idx));
        const isCorrect = JSON.stringify(letters) === JSON.stringify(item.answer);
        if (isCorrect) {
            if (incorrectSet.has(currentIndex)) { incorrectSet.delete(currentIndex); correctedSet.add(currentIndex); }
            else { correctSet.add(currentIndex); }
        } else {
            incorrectSet.add(currentIndex); correctSet.delete(currentIndex); correctedSet.delete(currentIndex);
        }
        saveState(); updateUI(); renderMatchingQuestion(currentIndex);
    };

    function toggleExplanation(forceShow = null) {
        const el = document.getElementById('ans-section'), btn = document.getElementById('toggle-exp-btn');
        if (!el || !btn) return;
        const isShow = (forceShow !== null) ? forceShow : (el.style.display !== 'block');
        el.style.display = isShow ? 'block' : 'none';
        if (isShow) setTimeout(() => { if(window.Prism) Prism.highlightAll(); }, 50);
    }

    function checkAnswer(element, qIdx, optIdx, event) {
        const item = quizData[qIdx], isMultiple = item.type === 'multiple';
        let answers = item.answer; if (!Array.isArray(answers)) answers = [answers];
        const correctIndices = answers.map(a => parseAnswerToIndex(a));
        const input = element.querySelector('input');
        if (event && event.target !== input) { if (isMultiple) input.checked = !input.checked; else input.checked = true; }
        if (isMultiple) {
            const inputs = document.querySelectorAll(`input[name="q\${qIdx}"]`);
            let selected = []; inputs.forEach((inp, idx) => { if (inp.checked) selected.push(idx); });
            userAnswers[qIdx] = selected;
            element.classList.toggle('correct', input.checked && correctIndices.includes(optIdx));
            element.classList.toggle('incorrect', input.checked && !correctIndices.includes(optIdx));
            const isPerfect = selected.length === correctIndices.length && selected.every(v => correctIndices.includes(v));
            if (isPerfect) {
                if (incorrectSet.has(qIdx)) { incorrectSet.delete(qIdx); correctedSet.add(qIdx); }
                else if (!correctedSet.has(qIdx)) { correctSet.add(qIdx); }
                inputs.forEach(i => i.disabled = true); toggleExplanation(true);
            } else if (selected.some(v => !correctIndices.includes(v)) || selected.length > correctIndices.length) {
                incorrectSet.add(qIdx); correctSet.delete(qIdx); correctedSet.delete(qIdx);
            }
        } else {
            if (correctSet.has(qIdx) || correctedSet.has(qIdx)) return;
            userAnswers[qIdx] = optIdx;
            if (correctIndices.includes(optIdx)) {
                element.classList.add('correct');
                if (incorrectSet.has(qIdx)) { incorrectSet.delete(qIdx); correctedSet.add(qIdx); }
                else { correctSet.add(qIdx); }
                document.querySelectorAll(`input[name="q\${qIdx}"]`).forEach(i => i.disabled = true);
            } else {
                element.classList.add('incorrect'); incorrectSet.add(qIdx);
                const ci = document.getElementById(`o\${correctIndices[0]}`); if (ci) ci.closest('.option-item').classList.add('correct');
            }
            toggleExplanation(true);
        }
        saveState(); updateUI();
    }

    function checkSubAnswer(element, qIdx, optIdx, subIdx, event) {
        const item = quizData[qIdx];
        let answers = item.answer; if (!Array.isArray(answers)) answers = [answers];
        const correctSubIdx = parseAnswerToIndex(answers[optIdx]), input = element.querySelector('input');
        if (event && event.target !== input) input.checked = true;
        if (!userAnswers[qIdx]) userAnswers[qIdx] = {}; userAnswers[qIdx][optIdx] = subIdx;
        element.parentElement.querySelectorAll('.sub-opt-container').forEach(el => el.classList.remove('selected'));
        element.classList.add('selected');
        if (subIdx === correctSubIdx) {
            element.classList.add('correct');
            const totalSub = (item.quiz || item.options || []).length;
            const curCorrect = document.querySelectorAll('.sub-opt-container.correct').length;
            if (curCorrect === totalSub) {
                if (incorrectSet.has(qIdx)) { incorrectSet.delete(qIdx); correctedSet.add(qIdx); }
                else if (!correctedSet.has(qIdx)) { correctSet.add(qIdx); }
                toggleExplanation(true);
            }
            document.querySelectorAll(`input[name="q\${qIdx}_opt\${optIdx}"]`).forEach(i => i.disabled = true);
        } else {
            element.classList.add('incorrect'); incorrectSet.add(qIdx);
            const ci = document.getElementById(`o\${optIdx}_s\${correctSubIdx}`); if (ci) ci.parentElement.classList.add('correct');
            toggleExplanation(true);
        }
        saveState(); updateUI();
    }

    function jumpTo(idx) { renderQuestion(idx); }
    const SUBJECT_ID = 'REPLACE_SUBJECT_ID';
    const ANS_KEY = SUBJECT_ID+'_ans_v1', CORR_KEY = SUBJECT_ID+'_corr_v1', INCORR_KEY = SUBJECT_ID+'_inc_v1', EDIT_KEY = SUBJECT_ID+'_edit_v1', IDX_KEY = SUBJECT_ID+'_idx_v1';
    
    function loadState() {
        try {
            const a = localStorage.getItem(ANS_KEY), c = localStorage.getItem(CORR_KEY), i = localStorage.getItem(INC_KEY), e = localStorage.getItem(EDIT_KEY), idx = localStorage.getItem(IDX_KEY);
            if(a) userAnswers = JSON.parse(a); if(c) correctSet = new Set(JSON.parse(c)); if(i) incorrectSet = new Set(JSON.parse(i)); if(e) correctedSet = new Set(JSON.parse(e)); if(idx) currentIndex = parseInt(idx)||0;
        } catch(e) {}
    }
    function saveState() {
        localStorage.setItem(ANS_KEY, JSON.stringify(userAnswers)); localStorage.setItem(CORR_KEY, JSON.stringify([...correctSet])); localStorage.setItem(INC_KEY, JSON.stringify([...incorrectSet])); localStorage.setItem(EDIT_KEY, JSON.stringify([...correctedSet])); localStorage.setItem(IDX_KEY, currentIndex.toString());
    }

    function updateUI() {
        const stats = document.getElementById('progress-stats'); if (stats) stats.innerHTML = `✅\${correctSet.size} ❌\${incorrectSet.size} 🟠\${correctedSet.size} / \${quizData.length}`;
        const grid = document.getElementById('progress-grid'); if(!grid) return;
        grid.innerHTML = '';
        quizData.forEach((_, i) => {
            const n = document.createElement('div'); n.className = 'q-node';
            if(i === currentIndex) n.classList.add('active');
            if(correctSet.has(i)) n.classList.add('correct');
            else if(correctedSet.has(i)) n.classList.add('corrected');
            else if(incorrectSet.has(i)) n.classList.add('incorrect');
            n.innerText = i + 1; n.onclick = () => jumpTo(i);
            grid.appendChild(n);
        });
    }

    function nextQuestion() { if (currentIndex < quizData.length-1) renderQuestion(currentIndex+1); }
    function prevQuestion() { if (currentIndex > 0) renderQuestion(currentIndex-1); }

    function renderQuestion(index) {
        window.scrollTo(0, 0); currentIndex = index; const item = quizData[index];
        if (item.type === 'matching') { renderMatchingQuestion(index); return; }
        const container = document.getElementById('question-container');
        if(document.getElementById('side-btn-prev')) document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';
        const optionsRaw = item.quiz || item.options || [];
        const opts = Array.isArray(optionsRaw) ? optionsRaw : [optionsRaw];
        let typeLabel = opts.some(o => String(o).includes('|')) ? "題組" : (item.type === 'multiple' ? "複選" : "單選");
        container.innerHTML = `<div class="card question-card"><div class="question-header"><div><span class="badge bg-primary me-2">題目 \${index + 1} / \${quizData.length}</span><span class="badge bg-info type-badge">\${typeLabel}</span></div><div class="category-tag">\${item.category || '一般'}</div></div><div class="question-body"><div>\${processContent(item.question, item)}</div>\${item.image ? `<img src="\${item.image}" class="q-img">` : ''}<div class="options-area"></div><div class="text-center mt-4 pt-3 border-top"><button class="btn btn-outline-primary px-4" id="toggle-exp-btn" onclick="toggleExplanation()">👁️ 顯示答案 / 解析</button></div><div class="answer-section" id="ans-section"><h6 class="fw-bold mb-3">正確答案: <span class="text-blue">\${Array.isArray(item.answer) ? item.answer.join(', ') : item.answer}</span></h6><div class="explanation">\${processContent(item.explanation || '暫無解析。', item)}</div></div></div></div>`;
        const optionsArea = container.querySelector('.options-area');
        opts.forEach((opt, oIdx) => {
            let labelText = `(\${String.fromCharCode(65+oIdx)}) `;
            if (String(opt).includes('|')) {
                const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                const displayLabel = item["question" + alphabet[oIdx]] || `選項 \${oIdx + 1}`;
                let sHtml = `<div class="mt-2 mb-1"><code>\${displayLabel}</code></div><div class="d-flex flex-wrap gap-2">`;
                opt.split('|').forEach((s, subIdx) => { 
                    sHtml += `<div class="sub-opt-container p-2 border rounded bg-light" onclick="checkSubAnswer(this, \${index}, \${oIdx}, \${subIdx}, event)" style="cursor:pointer; font-size:0.9rem"><input class="form-check-input" type="radio" name="q\${index}_opt\${oIdx}" id="o\${oIdx}_s\${subIdx}"> \${s}</div>`; 
                });
                optionsArea.innerHTML += sHtml + '</div></div>';
            } else { optionsArea.innerHTML += `<div class="option-item" onclick="checkAnswer(this, \${index}, \${oIdx}, event)"><input class="form-check-input" type="\${item.type==='multiple'?'checkbox':'radio'}" name="q\${index}" id="o\${oIdx}"><span>\${labelText}</span>\${opt}</div>`; }
        });
        const saved = userAnswers[index], completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);
        let answers = Array.isArray(item.answer) ? item.answer : [item.answer];
        let cIdxs = answers.map(a => parseAnswerToIndex(a));
        if (opts.some(o => String(o).includes('|'))) {
            opts.forEach((opt, r) => {
                const correctSubIdx = parseAnswerToIndex(answers[r]); const savedSubIdx = (saved && typeof saved === 'object') ? saved[r] : undefined;
                opt.split('|').forEach((_, subIdx) => {
                    const inp = document.getElementById(`o\${r}_s\${subIdx}`); if (!inp) return;
                    if (savedSubIdx !== undefined && parseInt(savedSubIdx) === subIdx) { inp.checked = true; inp.parentElement.classList.add('selected'); }
                    if (completed) { if (subIdx === correctSubIdx) inp.parentElement.classList.add('correct'); else if (savedSubIdx !== undefined && parseInt(savedSubIdx) === subIdx) inp.parentElement.classList.add('incorrect'); }
                });
            });
        } else if (saved !== undefined) {
            (Array.isArray(saved)?saved:[saved]).forEach(idx => { const inp = document.getElementById(`o\${idx}`); if (inp) { inp.checked = true; if(completed) inp.closest('.option-item').classList.add(cIdxs.includes(idx) ? 'correct' : 'incorrect'); } });
            if(completed) cIdxs.forEach(ci => { const inp = document.getElementById(`o\${ci}`); if (inp) inp.closest('.option-item').classList.add('correct'); });
        }
        if (completed) { toggleExplanation(true); document.querySelectorAll(`input[name^="q\${index}"]`).forEach(i => i.disabled = true); }
        updateUI(); setTimeout(() => { if(window.Prism) Prism.highlightAll(); }, 50); saveState(); window.changeZoom(0);
    }
    loadState(); window.addEventListener('resize', () => { if(window.drawLines) window.drawLines(); }); renderQuestion(currentIndex);
""";`;

const startMarker = 'prac_bottom = r"""';
const endMarker = '""";';
const sIdx = content.indexOf(startMarker);
const eIdx = content.indexOf(endMarker, sIdx + startMarker.length);

if (sIdx !== -1 && eIdx !== -1) {
    const finalContent = content.substring(0, sIdx) + goldenJS + content.substring(eIdx + endMarker.length);
    fs.writeFileSync(path, finalContent, 'utf-8');
    console.log('SUCCESS: Professional Rendering Engine restored.');
} else {
    console.log('ERROR: Marker not found.');
}
