const fs = require('fs');

const pyCode = `import json
import os
import glob

def clean_repair_all():
    config_path = 'www/config.json'
    if not os.path.exists(config_path):
        print("ERROR: config.json not found")
        return
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    mock_top = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REPLACE_TITLE 模擬考試</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f7f6; font-family: sans-serif; overflow-x: hidden; }
        .side-nav-btn { position: fixed; top: 55%; transform: translateY(-50%); width: 25px; height: 65px; background: rgba(0,0,0,0.5); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 2000; }
        .side-nav-prev { left: 0; border-radius: 0 15px 15px 0; }
        .side-nav-next { right: 0; border-radius: 15px 0 0 15px; }
        .zoom-controls { position: fixed; bottom: 30px; right: 20px; z-index: 1100; display: flex; flex-direction: column; gap: 10px; }
        .zoom-btn { width: 50px; height: 50px; border-radius: 50%; background: #212529; color: white; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer; border: 2px solid #fff; }
    </style>
</head>
<body>
<div class="zoom-controls no-print">
    <div class="zoom-btn" onclick="adjustZoom(0.1)">➕</div>
    <div class="zoom-btn" onclick="adjustZoom(-0.1)">➖</div>
</div>
<div id="exam-ui">
    <header class="bg-dark text-white p-2 d-flex justify-content-between align-items-center">
        <div><h5>REPLACE_TITLE 模擬考試</h5><small id="q-progress">1 / 60</small></div>
        <button class="btn btn-danger btn-sm" onclick="confirmSubmit()">交卷</button>
    </header>
    <main class="container py-5"><div id="question-area"></div></main>
</div>
<div id="result-screen" style="display:none; text-align:center; padding:50px;">
    <h2>考試結束</h2><div id="review-list" class="text-start mt-5"></div>
</div>
<script>
    let currentIndex = 0, userAnswers = {};
    function adjustZoom(d) { document.body.style.zoom = (parseFloat(getComputedStyle(document.body).zoom)||1) + d; }
    function confirmSubmit() { if(confirm("交卷?")) { document.getElementById('exam-ui').style.display='none'; document.getElementById('result-screen').style.display='block'; } }
    const allQuestions = """

    mock_bottom = r""";
    function renderQuestion(idx) { currentIndex = idx; document.getElementById('question-area').innerText = JSON.stringify(allQuestions[idx]); }
    renderQuestion(0);
</script></body></html>"""

    prac_top = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REPLACE_TITLE 認證練習</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
    <style>
        body { background-color: #f8f9fa; font-family: "Microsoft JhengHei", sans-serif; overflow-x: hidden; }
        .main-wrapper { display: flex; min-height: 100vh; }
        .sidebar { width: 280px; background: #fff; border-right: 1px solid #dee2e6; position: fixed; top: 0; bottom: 0; left: 0; z-index: 1000; padding: 15px; overflow-y: auto; height: 100vh; }
        .content-area { flex: 1; margin-left: 280px; padding: 20px; transition: margin-left 0.3s; }
        .question-card { border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; margin-bottom: 25px; }
        .question-header { border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; display: flex; justify-content: space-between; align-items: center; }
        .question-body { padding: 20px; font-size: 1.05rem; line-height: 1.8; }
        .option-item { border: 1px solid #e9ecef; border-radius: 6px; padding: 12px; margin-bottom: 10px; cursor: pointer; transition: 0.2s; display: flex; align-items: flex-start; gap: 10px; }
        .option-item.correct { background-color: #d1e7dd !important; border-color: #badbcc !important; color: #0f5132 !important; }
        .option-item.incorrect { background-color: #f8d7da !important; border-color: #f5c2c7 !important; color: #842029 !important; }
        .q-node { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border: 1px solid #dee2e6; border-radius: 6px; background-color: #fff; cursor: pointer; font-size: 0.85rem; margin: 3px; }
        .q-node.correct { background-color: #d1e7dd; color: #0f5132; }
        .q-node.incorrect { background-color: #f8d7da; color: #842029; }
        .q-node.corrected { background-color: #fd7e14; color: #fff; }
        .q-node.active { border: 2px solid #0d6efd; transform: scale(1.1); font-weight: bold; }
        .progress-grid { display: flex; flex-wrap: wrap; gap: 5px; }
        #zoom-controls { position: fixed; bottom: 85px; right: 20px; z-index: 2147483647; display: flex; flex-direction: column; gap: 12px; }
        .zoom-btn { width: 52px; height: 52px; border-radius: 50%; background: #212529; color: white; border: 2px solid #fff; font-size: 26px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; }
        #question-container { transform-origin: top center; transition: none; }
        .matching-wrapper { position: relative; margin: 30px 0; width: 100%; user-select: none; touch-action: pan-y pinch-zoom; }
        .matching-columns { display: flex; gap: 100px; padding-left: 10px; }
        .match-col { display: flex; flex-direction: column; gap: 25px; }
        .match-item { display: flex; align-items: center; min-height: 45px; cursor: pointer; }
        .match-dot { width: 22px; height: 22px; border: 1.5px solid #333; border-radius: 50%; margin: 0 15px; display: flex; align-items: center; justify-content: center; background: #fff; flex-shrink: 0; }
        .match-dot div { width: 10px; height: 10px; border-radius: 50%; }
        #matching-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
        .side-nav-btn { position: fixed; top: 55%; width: 25px; height: 65px; background: rgba(0,0,0,0.5); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 2000; transform: translateY(-50%); }
        .side-nav-prev { left: 280px; border-radius: 0 15px 15px 0; }
        .side-nav-next { right: 0; border-radius: 15px 0 0 15px; }
        .answer-section { display: none; margin-top: 20px; padding: 20px; background: #fff; border: 2px solid #0d6efd; border-radius: 8px; }
        .review-ans { color: #198754; font-weight: bold; padding: 10px; background: #e9f7ef; border-left: 5px solid #198754; margin: 10px 0; }
        @media (max-width: 992px) { .sidebar { display: none; } .content-area { margin-left: 0; } .side-nav-prev { left: 0; } .matching-columns { gap: 30px; } }
        .q-img { max-width: 100%; border-radius: 4px; margin: 10px 0; border: 1px solid #eee; }
    </style>
</head>
<body>
    <div id="zoom-controls"><button class="zoom-btn" onclick="changeZoom(0.1)">+</button><button class="zoom-btn" onclick="changeZoom(-0.1)">−</button></div>
    <div class="main-wrapper">
        <nav class="sidebar">
            <div class="mb-3"><h5>REPLACE_TITLE 認證練習</h5><div id="progress-stats" class="fw-bold">✅0 ❌0 🟠0 / REPLACE_TOTAL</div></div>
            <div class="progress-grid" id="progress-grid"></div>
        </nav>
        <div class="side-nav-btn side-nav-prev" id="side-btn-prev" onclick="prevQuestion()">&#10094;</div>
        <div class="side-nav-btn side-nav-next" id="side-btn-next" onclick="nextQuestion()">&#10095;</div>
        <main class="content-area"><div id="question-container"></div></main>
    </div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script>
    const quizData = """

    prac_bottom = r""";
    let currentIndex = 0, correctSet = new Set(), incorrectSet = new Set(), correctedSet = new Set(), userAnswers = {};
    window.itspyZoom = 1.0;
    window.changeZoom = function(d) {
        window.itspyZoom = Math.round((window.itspyZoom + d)*10)/10;
        if(window.itspyZoom<0.6) window.itspyZoom=0.6; if(window.itspyZoom>2.5) window.itspyZoom=2.5;
        const c = document.getElementById('question-container');
        if(c) { c.style.transform = "scale("+window.itspyZoom+")"; if(typeof window.drawLines==='function') window.drawLines(); }
    };
    function parseAnswerToIndex(v) {
        if(typeof v==='number') return v-1;
        if(typeof v==='string'){ let s=v.toUpperCase(); if(s==='Y') return 0; if(s==='N') return 1; return s.charCodeAt(0)-65; }
        return -1;
    }
    function processContent(c, item) {
        if(!c) return '';
        let lines = Array.isArray(c) ? c : [String(c)];
        return lines.join(String.fromCharCode(10)).replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
            const src = item['image' + p1] || item.image;
            return src ? '<img src="' + src + '" class="q-img">' : match;
        });
    }
    function renderMatchingQuestion(index) {
        currentIndex = index; const item = quizData[index]; const container = document.getElementById('question-container');
        if (userAnswers[index] === undefined) userAnswers[index] = new Array(item.left.length).fill(null);
        const currentAns = userAnswers[index];
        const isWrong = incorrectSet.has(index), isCorr = correctSet.has(index), isEdit = correctedSet.has(index);
        const completed = isCorr || isEdit;
        let html = '<div class="card question-card"><div class="question-header"><div>題目 ' + (index+1) + ' / ' + quizData.length + ' <span class="badge ' + (isEdit?'bg-warning':(isCorr?'bg-success':'bg-info')) + '">配對題</span></div></div><div class="question-body"><div>' + processContent(item.question, item) + '</div>';
        if(isWrong && !completed) html += '<div class="alert alert-danger py-2 mt-2">❌ 答案不正確，請重試。</div>';
        html += '<div class="matching-wrapper" id="matching-wrapper" onmousemove="handleDragMove(event)" onmouseup="handleDragEnd(event)">' +
                    '<div class="match-header-row" style="display:flex; gap:100px; font-weight:bold; color:#666; margin-bottom:15px; border-bottom:1px solid #eee;"><div>程式碼片段</div><div>回答區</div></div>' +
                    '<svg id="matching-svg" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:1;"></svg>' +
                    '<div class="matching-columns"><div class="match-col">';
        item.left.forEach((text, lIdx) => {
            const matchedR = currentAns[lIdx], dotC = completed?(isEdit?'#fd7e14':'#198754'):(isWrong?'#dc3545':(matchedR!==null?'#333':'transparent'));
            html += '<div class="match-item"><div>' + text + '</div><div class="match-dot" id="dot-left-' + lIdx + '" onmousedown="' + (completed?'':'handleDragStart(event,'left',' + lIdx + ')') + '" ontouchstart="' + (completed?'':'handleDragStart(event,'left',' + lIdx + ')') + '"><div style="background:' + dotC + '"></div></div></div>';
        });
        html += '</div><div class="match-col">';
        item.right.forEach((text, rIdx) => {
            const isMatched = currentAns.includes(rIdx), dotC = completed?(isEdit?'#fd7e14':'#198754'):(isWrong?'#dc3545':(isMatched?'#333':'transparent'));
            html += '<div class="match-item" data-right-idx="' + rIdx + '"><div class="match-dot" id="dot-right-' + rIdx + '"><div style="background:' + dotC + '"></div></div><div>' + text + '</div></div>';
        });
        html += '</div></div></div>';
        if(!completed) html += '<div class="text-center mt-4"><button class="btn btn-primary px-5" onclick="submitMatching()">確認提交</button></div>';
        else html += '<div class="answer-section" style="display:block"><div class="review-ans">正確答案：' + item.answer.join(', ') + '</div><div class="explanation">' + processContent(item.explanation, item) + '</div></div>';
        container.innerHTML = html + '</div></div>'; updateUI(); setTimeout(drawLines, 100); if(window.Prism) Prism.highlightAll();
    }
    let isDragging = false, dragStartPoint = null, tempLine = null;
    window.handleDragStart = function(e, side, idx) {
        if(side!=='left') return; isDragging = true;
        const dot = document.getElementById("dot-left-"+idx), rect = dot.getBoundingClientRect(), wRect = document.getElementById("matching-wrapper").getBoundingClientRect(), z = window.itspyZoom;
        dragStartPoint = { lIdx: idx, x: (rect.left+rect.width/2-wRect.left)/z, y: (rect.top+rect.height/2-wRect.top)/z };
        const svg = document.getElementById("matching-svg");
        tempLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
        tempLine.setAttribute("stroke", "#0d6efd"); tempLine.setAttribute("stroke-width", "2.5"); svg.appendChild(tempLine);
    };
    window.handleDragMove = function(e) {
        if(!isDragging || !tempLine) return;
        const w = document.getElementById('matching-wrapper').getBoundingClientRect(), z = window.itspyZoom;
        const x2 = (e.clientX-w.left)/z, y2 = (e.clientY-w.top)/z;
        tempLine.setAttribute("x1", dragStartPoint.x); tempLine.setAttribute("y1", dragStartPoint.y);
        tempLine.setAttribute("x2", x2); tempLine.setAttribute("y2", y2);
    };
    window.handleDragEnd = function(e) {
        if(!isDragging) return;
        const target = document.elementFromPoint(e.clientX, e.clientY), item = target ? target.closest('.match-item') : null;
        if(item && item.hasAttribute('data-right-idx')) { userAnswers[currentIndex][dragStartPoint.lIdx] = parseInt(item.getAttribute('data-right-idx')); }
        isDragging = false; if(tempLine) tempLine.remove(); renderMatchingQuestion(currentIndex);
    };
    window.drawLines = function() {
        const svg = document.getElementById('matching-svg'), w = document.getElementById('matching-wrapper');
        if(!svg || !w) return; const z = window.itspyZoom, rect = w.getBoundingClientRect();
        svg.setAttribute('viewBox', '0 0 ' + (rect.width/z) + ' ' + (rect.height/z)); svg.innerHTML = '';
        const ans = userAnswers[currentIndex]; if(!ans) return;
        ans.forEach((rIdx, lIdx) => {
            if(rIdx===null) return;
            const dL = document.getElementById("dot-left-"+lIdx), dR = document.getElementById("dot-right-"+rIdx);
            if(dL && dR) {
                const rL = dL.getBoundingClientRect(), rR = dR.getBoundingClientRect();
                const x1 = (rL.left+rL.width/2-rect.left)/z, y1 = (rL.top+rL.height/2-rect.top)/z;
                const x2 = (rR.left+rR.width/2-rect.left)/z, y2 = (rR.top+rR.height/2-rect.top)/z;
                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute("x1", x1); line.setAttribute("y1", y1);
                line.setAttribute("x2", x2); line.setAttribute("y2", y2);
                line.setAttribute("stroke", "#0d6efd"); line.setAttribute("stroke-width", "2.5"); svg.appendChild(line);
            }
        });
    };
    window.submitMatching = function() {
        const item = quizData[currentIndex], ans = userAnswers[currentIndex];
        if(ans.includes(null)) { alert("請完成配對!"); return; }
        const letters = ans.map(idx => String.fromCharCode(65+idx));
        const isCorrect = JSON.stringify(letters) === JSON.stringify(item.answer);
        if(isCorrect) { if(incorrectSet.has(currentIndex)) { incorrectSet.delete(currentIndex); correctedSet.add(currentIndex); } else correctSet.add(currentIndex); }
        else incorrectSet.add(currentIndex);
        saveState(); renderMatchingQuestion(currentIndex);
    };
    function toggleExplanation(forceShow = null) {
        const el = document.getElementById('ans-section'); if (!el) return;
        const isShow = (forceShow !== null) ? forceShow : (el.style.display !== 'block');
        el.style.display = isShow ? 'block' : 'none';
    }
    function checkAnswer(element, qIdx, optIdx, event) {
        const item = quizData[qIdx]; let answers = Array.isArray(item.answer)?item.answer:[item.answer];
        const correctIndices = answers.map(a => parseAnswerToIndex(a)), input = element.querySelector('input');
        if(event && event.target !== input) input.checked = !input.checked;
        userAnswers[qIdx] = optIdx;
        if(correctIndices.includes(optIdx)) { if(incorrectSet.has(qIdx)) { incorrectSet.delete(qIdx); correctedSet.add(qIdx); } else correctSet.add(qIdx); }
        else { incorrectSet.add(qIdx); }
        saveState(); updateUI(); renderQuestion(qIdx);
    }
    function nextQuestion() { if(currentIndex < quizData.length-1) renderQuestion(currentIndex+1); }
    function prevQuestion() { if(currentIndex > 0) renderQuestion(currentIndex-1); }
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
        localStorage.setItem(ANS_KEY, JSON.stringify(userAnswers)); localStorage.setItem(CORR_KEY, JSON.stringify([...correctSet])); localStorage.setItem(INCORR_KEY, JSON.stringify([...incorrectSet])); localStorage.setItem(EDIT_KEY, JSON.stringify([...correctedSet])); localStorage.setItem(IDX_KEY, currentIndex.toString());
    }
    function updateUI() {
        const stats = document.getElementById('progress-stats'); if (stats) stats.innerHTML = '✅' + correctSet.size + ' ❌' + incorrectSet.size + ' 🟠' + correctedSet.size + ' / ' + quizData.length;
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
    function renderQuestion(index) {
        window.scrollTo(0, 0); currentIndex = index; const item = quizData[index];
        if (item.type === 'matching') { renderMatchingQuestion(index); return; }
        const container = document.getElementById('question-container');
        if(document.getElementById('side-btn-prev')) document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';
        const optionsRaw = item.quiz || item.options || []; const opts = Array.isArray(optionsRaw) ? optionsRaw : [optionsRaw];
        const isWrong = incorrectSet.has(index), isCorr = correctSet.has(index), isEdit = correctedSet.has(index);
        const completed = isCorr || isEdit;
        let html = '<div class="card question-card"><div class="question-header"><div>題目 ' + (index + 1) + ' / ' + quizData.length + '</div></div><div class="question-body"><div>' + processContent(item.question, item) + '</div>' + (item.image ? '<img src="' + item.image + '" class="q-img">' : '') + '<div class="options-area">';
        opts.forEach((opt, oIdx) => {
            const saved = userAnswers[index], isSel = (saved === oIdx);
            const statusClass = (completed && isSel) ? 'correct' : (isWrong && isSel ? 'incorrect' : '');
            html += '<div class="option-item ' + statusClass + '" onclick="checkAnswer(this,' + index + ',' + oIdx + ', event)"><input class="form-check-input" type="radio" name="q' + index + '" id="o' + oIdx + '" ' + (isSel?'checked':'') + '><span>(' + String.fromCharCode(65+oIdx) + ')</span> ' + opt + '</div>';
        });
        html += '</div><div class="text-center mt-4 pt-3 border-top"><button class="btn btn-outline-primary px-4" onclick="toggleExplanation()">👁️ 顯示解析</button></div><div class="answer-section" id="ans-section"><b>正確答案：' + item.answer + '</b><div class="explanation">' + processContent(item.explanation, item) + '</div></div></div></div>';
        container.innerHTML = html; if(completed) toggleExplanation(true);
        updateUI(); saveState(); window.changeZoom(0); if(window.Prism) Prism.highlightAll();
    }
    loadState(); window.addEventListener('resize', () => { if(window.drawLines) window.drawLines(); }); renderQuestion(currentIndex);
</script></body></html>"""

    for subj in config['subjects']:
        try:
            json_file = os.path.join(subj['dir'], subj['json'])
            if not os.path.exists(json_file): continue
            with open(json_file, 'r', encoding='utf-8') as f: quiz_obj = json.load(f)
            
            mock_path = os.path.join(subj['dir'], 'mock_v34.html')
            with open(mock_path, 'w', encoding='utf-8') as f:
                f.write(mock_top.replace('REPLACE_TITLE', subj['title']))
                f.write(json.dumps(quiz_obj, ensure_ascii=False))
                f.write(mock_bottom)
            
            prac_path = os.path.join(subj['dir'], subj['html'])
            with open(prac_path, 'w', encoding='utf-8') as f:
                f.write(prac_top.replace('REPLACE_TITLE', subj['title']).replace('REPLACE_TOTAL', str(len(quiz_obj))).replace('REPLACE_SUBJECT_ID', subj['id']))
                f.write(json.dumps(quiz_obj, ensure_ascii=False))
                f.write(prac_bottom.replace('REPLACE_SUBJECT_ID', subj['id']))
            print(f"DONE: {subj['dir']}")
        except Exception as e: print(f"FAIL {subj['dir']}: {e}")

if __name__ == "__main__": clean_repair_all()
`;

fs.writeFileSync('final_clean_repair.py', pyCode, 'utf-8');
console.log('FINAL_CLEAN_REPAIR.PY FULLY REBUILT');
