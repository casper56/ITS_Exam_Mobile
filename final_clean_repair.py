import json
import os
import glob

def clean_repair_all():
    config_path = 'www/config.json'
    if not os.path.exists(config_path):
        print("錯誤：找不到 www/config.json 設定檔！")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # --- 模板 A: 模擬考試 (mock_v34.html) ---
    mock_top_tmpl = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REPLACE_TITLE 模擬考試</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
    <style>
        html { scrollbar-gutter: stable; }
        body { background-color: #f4f7f6; font-family: 'Segoe UI', "Microsoft JhengHei", sans-serif; overflow-x: hidden !important; }
        .exam-header { position: fixed; top: 0; left: 0; right: 0; z-index: 1050; background: #212529; color: white; padding: 10px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .timer-box { font-size: 1.5rem; font-weight: bold; color: #ffc107; }
        .main-content { margin-top: 80px; padding-bottom: 100px; width: calc(100% - 60px) !important; margin-left: auto !important; margin-right: auto !important; padding-left: 0 !important; padding-right: 0 !important; max-width: none !important; }
        .question-card { border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; margin-bottom: 25px; }
                .question-header { background-color: #fff; border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; }
                .question-body, .explanation, .review-q-text, .review-exp { 
                    padding: 5px 20px; 
                    font-size: 1.05rem; 
                    background-color: #fff; 
                    color: #000; 
                    word-wrap: break-word; 
                    word-break: normal; 
                    overflow-x: hidden;
                }
                
                .q-content { white-space: pre-wrap; }
                
                code:not([class*="language-"]) { 
                    display: inline-block; 
                    margin: 5px 0; 
                    line-height: 1.4; 
                    font-size: 1.0rem; 
                    color: #222222; 
                }
                
                code {
                    background-color: transparent !important; 
                    font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
                }
        code[class*="language-"], pre[class*="language-"] { color: #333 !important; text-shadow: none !important; background: #fdfdfd !important; white-space: pre-wrap !important; word-break: break-all !important; }
        .token.operator, .token.entity, .token.url, .language-css .token.string, .style .token.string { background: none !important; }

        .option-item { list-style: none; margin-bottom: 8px; padding: 8px 12px; border: 1px solid #e9ecef; border-radius: 8px; cursor: pointer; transition: all 0.2s; background-color: #fff; font-size: 1rem; display: flex; align-items: flex-start; gap: 5px; }
        .option-item:hover { background-color: #f8f9fa; border-color: #adb5bd; }
        .option-item.selected { background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }
        .sub-opt-container { padding: 6px 10px; border: 1px solid #dee2e6; border-radius: 6px; cursor: pointer; background: #fff; transition: all 0.2s; font-size: 0.85rem; }
        .sub-opt-container.selected { background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }
        .sub-question-label { font-weight: bold; margin-top: 15px; margin-bottom: 8px; color: #212529; border-left: 4px solid #198754; padding-left: 10px; font-size: 0.9rem; }
        #result-screen { display: none; text-align: center; padding: 50px 20px; }
        .score-circle { width: 150px; height: 150px; border-radius: 50%; border: 8px solid #0d6efd; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: bold; margin: 20px auto; color: #0d6efd; }
        .q-img { max-width: 48%; height: auto; border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); margin: 5px 5px 5px 0; display: inline-block; vertical-align: top; }
        pre { background-color: transparent !important; border: none !important; line-height: 1.6; white-space: pre-wrap !important; word-wrap: break-word !important; word-break: break-all !important; overflow-x: hidden !important; margin: 0 !important; padding: 0 !important; }
        .question-body pre { margin: 0 !important; padding: 0 !important; }

        table, .q-table { max-width: 98% !important; border-collapse: collapse !important; margin: 15px 0; border: 1px solid #000 !important; font-size: 0.9rem; line-height: 1.2; box-sizing: border-box !important; }
        th, td, .q-table th, .q-table td { border: 1px solid #000 !important; padding: 10px 8px; vertical-align: top; word-break: break-all !important; color: #000; overflow-wrap: break-word !important; }
        
        .side-nav-btn { position: fixed; top: 55%; transform: translateY(-50%); width: 25px; height: 65px; background: rgba(108, 117, 125, 0.7); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 2000; transition: all 0.3s ease, width 0.2s; text-decoration: none; font-size: 1.1rem; border: none; font-family: serif; font-weight: bold; }
        .side-nav-btn:hover { background: #0d6efd; color: white; width: 30px; }
        .side-nav-prev { left: 0; border-radius: 0 15px 15px 0; }
        .side-nav-next { right: 0; border-radius: 15px 0 0 15px; }
        #review-area { display: none; text-align: left; margin-top: 30px; border-top: 2px solid #dee2e6; padding: 20px; background: #fff; position: relative; z-index: 2000; }
        .review-item { margin-bottom: 20px; padding: 10px; border: 2px solid #000; border-radius: 4px; background: #fff; }
        .review-id { font-weight: bold; color: #000; padding: 5px 0; border-bottom: 1px solid #000; margin-bottom: 10px; }
        .review-ans { color: #198754; font-weight: bold; padding: 10px; border: 1px solid #000; margin: 10px 0; border-left-width: 5px; }
        .review-exp { font-size: 0.95rem; color: #212529; background: #f8f9fa; padding: 10px; border: 1px solid #000; }
        @media print { 
            @page { size: auto; margin: 10mm; }
            * { overflow: visible !important; max-height: none !important; height: auto !important; }
            body { background: white; width: 100%; margin: 0; padding: 0; font-size: 1.0rem !important; }
            #exam-ui, #result-screen h2, .score-circle, .lead, #result-msg, .no-print { display: none !important; }
            #result-screen { display: block !important; padding: 0 !important; width: 100% !important; margin: 0 !important; }
            #review-area { display: block !important; border: none !important; width: 100% !important; padding: 0 !important; margin: 0 !important; }
            .review-item { border: 2px solid #000 !important; width: 100% !important; page-break-inside: auto !important; margin-bottom: 5px !important; padding: 10px !important; border-radius: 0 !important; }
            .review-id { margin: 0 0 5px 0 !important; padding: 0 0 2px 0 !important; border-bottom: 1px solid #000 !important; color: #000 !important; background: #fff !important; }
            .review-q-text { display: block !important; padding: 2px 0 !important; font-size: 1.0rem !important; width: 100% !important; }
            .review-ans { color: #198754 !important; font-weight: bold !important; padding: 4px 10px !important; border: 1px solid #000 !important; border-left: 5px solid #198754 !important; margin: 5px 0 !important; }
            .review-exp { font-size: 0.95rem !important; padding: 5px 10px !important; border: 1px solid #000 !important; line-height: 1.4 !important; }
            
            /* 強效鎖定列印配對圖佈局 */
            .print-matching { 
                display: block !important; 
                width: 100% !important; 
                position: relative !important; 
                margin: 15px 0 !important; 
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .match-header-row, .matching-columns { display: block !important; width: 100% !important; clear: both !important; }
            .match-header-title, .match-col { display: inline-block !important; width: 48% !important; vertical-align: top !important; }
            .match-item { display: flex !important; width: 100% !important; margin-bottom: 5px !important; }
            .print-svg { 
                position: absolute !important; 
                top: 0 !important; 
                left: 0 !important; 
                width: 100% !important; 
                height: 100% !important; 
                z-index: 99 !important; 
                visibility: visible !important;
                display: block !important;
                overflow: visible !important;
            }
            line { stroke-opacity: 1 !important; }
            pre, code { white-space: pre-wrap !important; word-break: break-all !important; border: none !important; font-size: 1.0rem !important; margin: 0 !important; padding: 0 !important; }
            .q-table { font-size: 0.7rem !important; margin: 10px 0 !important; page-break-inside: avoid; -webkit-print-color-adjust: exact; }
            .q-table td, .q-table th { border: 1px solid #000 !important; padding: 6px !important; }
        }
        .zoom-controls { position: fixed; bottom: 30px; right: 20px; z-index: 1100; display: flex; flex-direction: column; gap: 10px; }
        .zoom-btn { width: 50px; height: 50px; border-radius: 50%; background: rgba(255, 255, 255, 0.9); color: #0d6efd; border: 2px solid #0d6efd; box-shadow: 0 4px 10px rgba(0,0,0,0.2); font-size: 1.5rem; font-weight: bold; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; padding: 0; user-select: none; -webkit-tap-highlight-color: transparent; }
        
        /* 配對題樣式 */
        .matching-wrapper { position: relative; margin: 10px 0 15px 0 !important; padding: 0 10px 10px 10px !important; width: 100%; user-select: none; touch-action: pan-y pinch-zoom; overflow: visible !important; }
        .match-header-title { font-weight: bold; color: #666; font-size: 1.1rem; border-bottom: 1px solid #eee; margin-bottom: 10px; padding-bottom: 5px; }
        .right-col .match-header-title { margin-left: 10px; }
        .matching-columns { display: flex !important; justify-content: flex-start !important; align-items: flex-start !important; gap: 60px !important; position: relative; z-index: 2; padding-left: 10px !important; width: max-content !important; }
        .match-col { display: flex !important; flex-direction: column !important; gap: 25px !important; width: max-content !important; flex: none !important; }
        .match-item { display: flex !important; align-items: center !important; min-height: 45px !important; cursor: pointer !important; width: max-content !important; }
        .match-item-left { justify-content: flex-start !important; text-align: left !important; }
        .match-item-right { justify-content: flex-start !important; text-align: left !important; }
        .match-item-left .q-text-part { display: inline-block !important; }
        .match-dot { width: 22px !important; height: 22px !important; border: 1.5px solid #333 !important; border-radius: 50% !important; display: flex !important; align-items: center !important; justify-content: center !important; background: #fff !important; position: relative !important; flex-shrink: 0 !important; margin: 0 10px !important; }
        .match-item.matched .match-dot::after, .match-item.selected .match-dot::after { background: #333; }
        #matching-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
        @media (max-width: 768px) {
            .matching-columns, .match-header-row { gap: 30px !important; }
            .match-col { min-width: 140px !important; }
        }
    </style>
</head>
<body>
<div class="zoom-controls no-print">
    <div class="zoom-btn" onclick="adjustZoom(0.1)">➕</div>
    <div class="zoom-btn" onclick="adjustZoom(-0.1)">➖</div>
</div>
<div id="exam-ui">
    <header class="exam-header d-flex justify-content-between align-items-center">
        <div><h5 class="m-0">REPLACE_TITLE 模擬考試</h5><small id="q-progress">1 / 60</small></div>
        <div class="timer-box" id="timer">50:00</div>
        <button class="btn btn-danger btn-sm" onclick="confirmSubmit()">交卷</button>
    </header>
    <div class="side-nav-btn side-nav-prev" id="side-btn-prev" onclick="changeQuestion(-1)">&#10094;</div>
    <div class="side-nav-btn side-nav-next" id="side-btn-next" onclick="changeQuestion(1)">&#10095;</div>
    <main class="container-fluid main-content" style="width: calc(100% - 60px); margin-top: 80px; max-width: none !important;"><div id="question-area"></div></main>
</div>
<div id="result-screen" class="container-fluid">
    <h2 class="mb-4">考試結束</h2><div class="score-circle" id="final-score">0</div>
    <p class="lead">答對題數：<span id="correct-count">0</span> / 60</p>
    <div id="category-stats" class="mb-4 no-print"></div><div id="result-msg" class="mb-4"></div>
    <div class="mt-5 no-print">
        <a href="../../index.html" class="btn btn-primary btn-lg me-2">回首頁</a>
        <button class="btn btn-outline-secondary btn-lg me-2" onclick="location.reload()">重新挑戰</button>
        <button id="btn-export-pdf" class="btn btn-success btn-lg" onclick="window.print()">🖨️ 列印錯題</button>
    </div>
    <div id="review-area">
        <div class="d-flex justify-content-between align-items-center mb-4 no-print"><h3 class="m-0">錯誤題目回顧報告</h3></div>
        <div id="review-list"></div>
    </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-csharp.min.js"></script>
<script>
    const EXAM_LIMIT = 60, WRONG_KEY = 'REPLACE_SUBJECT_ID_exam_wrong_ids', HISTORY_KEY = 'REPLACE_SUBJECT_ID_mock_history';
    let currentIndex = 0, userAnswers = {}, timeLeft = 50 * 60, timerInterval;
    let examQuestions = [];

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

    const allQuestions = """

    mock_bottom_tmpl = r"""
    function renderMatchingQuestion(index) {
        currentIndex = index; const item = examQuestions[index];
        const container = document.getElementById('question-area');
        if (!container) return;
        const progressEl = document.getElementById('q-progress');
        if (progressEl) progressEl.innerText = `${index + 1} / ${examQuestions.length}`;
        const sidePrev = document.getElementById('side-btn-prev'), sideNext = document.getElementById('side-btn-next');
        if (sidePrev) sidePrev.style.display = index === 0 ? 'none' : 'flex';
        if (sideNext) sideNext.style.display = 'flex';
        
        if (userAnswers[index] === undefined) userAnswers[index] = new Array(item.left.length).fill(null);
        const currentAns = userAnswers[index];
        
        let qText = processContent(item.question, item);
        let html = `<div class="card question-card"><div class="question-header">題目 ${index + 1} / ${examQuestions.length} <span class="badge bg-secondary ms-2">${item.category || ''}</span> <span class="badge bg-info ms-2">配對題</span></div><div class="question-body"><div class="q-content mb-0" style="margin: 0 !important; padding: 0 !important; display: block;">${qText}</div><div class="matching-wrapper" id="matching-wrapper" onmousemove="handleDragMove(event)" onmouseup="handleDragEnd(event)" ontouchmove="handleDragMove(event)" ontouchend="handleDragEnd(event)">
        <svg id="matching-svg"></svg>
        <div class="matching-columns">
            <div class="match-col left-col">
                <div class="match-header-title">程式碼片段</div>`;
        item.left.forEach((text, lIdx) => {
            const isMatched = currentAns[lIdx] !== null;
            const dotColor = isMatched ? '#333' : 'transparent';
            html += `<div class="match-item match-item-left ${isMatched?'matched':''}" id="left-item-${lIdx}"><div class="q-text-part" style="font-family:Consolas,monospace; white-space:nowrap;">${text}</div><div class="match-dot" id="dot-left-${lIdx}" onmousedown="handleDragStart(event, 'left', ${lIdx})" ontouchstart="handleDragStart(event, 'left', ${lIdx})"><div style="width:10px; height:10px; border-radius:50%; background:${dotColor};"></div></div></div>`;
        });
        html += `</div><div class="match-col right-col">
            <div class="match-header-title">回答區</div>`;
        item.right.forEach((text, rIdx) => {
            const isMatchedByAny = currentAns.includes(rIdx);
            const dotColor = isMatchedByAny ? '#333' : 'transparent';
            html += `<div class="match-item match-item-right ${isMatchedByAny?'matched':''}" id="right-item-${rIdx}" data-right-idx="${rIdx}"><div class="match-dot" id="dot-right-${rIdx}"><div style="width:10px; height:10px; border-radius:50%; background:${dotColor};"></div></div><div style="font-family:Consolas,monospace;">${text}</div></div>`;
        });
        html += `</div></div></div></div></div>`;
        container.innerHTML = html; 
        setTimeout(() => {
            const parts = container.querySelectorAll('.match-item-left .q-text-part');
            let maxW = 0; parts.forEach(p => maxW = Math.max(maxW, p.offsetWidth));
            parts.forEach(p => p.style.width = (maxW + 2) + 'px');
            drawLines();
        }, 15);
        if(window.Prism) Prism.highlightAll();
    }

    let isDragging = false, dragStartPoint = null, tempLine = null;
    window.handleDragStart = function(e, side, idx) {
        if (side !== 'left') return;
        if (userAnswers[currentIndex] && userAnswers[currentIndex][idx] !== null) { userAnswers[currentIndex][idx] = null; renderMatchingQuestion(currentIndex); }
        isDragging = true; if(e.cancelable) e.preventDefault();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX, clientY = e.touches ? e.touches[0].clientY : e.clientY;
        window.lastClientX = clientX; window.lastClientY = clientY;
        const dot = document.getElementById("dot-left-" + idx), rect = dot.getBoundingClientRect();
        const wrapperRect = document.getElementById("matching-wrapper").getBoundingClientRect();
        const zoom = parseFloat(document.body.style.zoom) || 1.0;
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
        const zoom = parseFloat(document.body.style.zoom) || 1.0;
        tempLine.setAttribute('x2', (clientX - rect.left) / zoom); tempLine.setAttribute('y2', (clientY - rect.top) / zoom);
    };
    window.handleDragEnd = function(e) {
        if (!isDragging) return;
        let x = window.lastClientX, y = window.lastClientY;
        if (e && e.changedTouches && e.changedTouches[0]) { x = e.changedTouches[0].clientX; y = e.changedTouches[0].clientY; }
        else if (e && e.clientX !== undefined) { x = e.clientX; y = e.clientY; }
        if (Number.isFinite(x) && Number.isFinite(y)) {
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
        const zoom = parseFloat(document.body.style.zoom) || 1.0, rect = wrapper.getBoundingClientRect();
        const baseW = rect.width / zoom, baseH = rect.height / zoom;
        svg.setAttribute('viewBox', `0 0 ${baseW} ${baseH}`);
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

    function startTimer() {
        timerInterval = setInterval(() => {
            timeLeft--;
            const m = Math.floor(timeLeft / 60), s = timeLeft % 60;
            const el = document.getElementById('timer');
            if (el) el.innerText = `${m}:${s < 10 ? '0' : ''}${s}`;
            if (timeLeft <= 0) { clearInterval(timerInterval); submitExam(); }
        }, 1000);
    }

    function adjustZoom(delta) {
        const body = document.body;
        let currentZoom = parseFloat(getComputedStyle(body).zoom) || 1;
        body.style.zoom = currentZoom + delta;
    }

    function processContent(content, item) {
        if (!content) return '';
        const lines = Array.isArray(content) ? content : [String(content)];
        return lines.join(String.fromCharCode(10)).replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
            const num = parseInt(p1, 10);
            const src = item['image' + num] || item['image' + p1] || item['image'];
            return src ? `<img src="${src}" class="q-img">` : match;
        });
    }

    function initExam() {
        if (typeof allQuestions === 'undefined' || allQuestions.length === 0) {
            console.error("題庫資料載入失敗！"); return;
        }
        const CUTOFF = REPLACE_CUTOFF;
        const TARGET_OFF_COUNT = Math.floor(EXAM_LIMIT * 0.95); // 57
        const TARGET_SUPP_COUNT = EXAM_LIMIT - TARGET_OFF_COUNT; // 3
        
        let historySet = new Set();
        try {
            const savedHistory = localStorage.getItem(HISTORY_KEY);
            if (savedHistory) historySet = new Set(JSON.parse(savedHistory));
        } catch(e) {}

        // 1. 池子拆分：官方與補充
        const offPoolTotal = allQuestions.filter(q => q.id <= CUTOFF);
        const suppPoolTotal = allQuestions.filter(q => q.id > CUTOFF);

        // 2. 池內優先級排序 (未看優先)
        const offUnseen = offPoolTotal.filter(q => !historySet.has(q.id)).sort(() => 0.5 - Math.random());
        const offSeen = offPoolTotal.filter(q => historySet.has(q.id)).sort(() => 0.5 - Math.random());
        const suppUnseen = suppPoolTotal.filter(q => !historySet.has(q.id)).sort(() => 0.5 - Math.random());
        const suppSeen = suppPoolTotal.filter(q => historySet.has(q.id)).sort(() => 0.5 - Math.random());

        let finalOffOrder = [...offUnseen, ...offSeen];
        let finalSuppOrder = [...suppUnseen, ...suppSeen];

        let selected = [], usedIds = new Set();
        
        // --- 階段 A：分類平衡 (優先從官方池抽) ---
        const categories = {};
        allQuestions.forEach(q => {
            const cat = q.category || '一般';
            if (!categories[cat]) categories[cat] = [];
            categories[cat].push(q);
        });
        const catNames = Object.keys(categories).sort();
        
        catNames.forEach(cat => {
            let pool = finalOffOrder.filter(q => q.category === cat && !usedIds.has(q.id));
            if (pool.length === 0) pool = finalSuppOrder.filter(q => q.category === cat && !usedIds.has(q.id));
            const limit = (cat.includes('D0')) ? 2 : 3;
            for (let i = 0; i < limit; i++) {
                if (pool.length > 0) {
                    const q = pool.shift();
                    selected.push(q);
                    usedIds.add(q.id);
                }
            }
        });

        // --- 階段 B：死守官方 95% 配額 ---
        for (let q of finalOffOrder) {
            if (selected.filter(s => s.id <= CUTOFF).length >= TARGET_OFF_COUNT) break;
            if (!usedIds.has(q.id)) {
                // 如果是 D0 類別，且已經有 2 題，則跳過
                if (q.category && q.category.includes('D0')) {
                    const curD0 = selected.filter(s => s.category && s.category.includes('D0')).length;
                    if (curD0 >= 2) continue;
                }
                selected.push(q);
                usedIds.add(q.id);
            }
        }

        // --- 階段 C：填滿補充 5% 配額 ---
        for (let q of finalSuppOrder) {
            if (selected.length >= EXAM_LIMIT) break;
            if (!usedIds.has(q.id)) {
                selected.push(q);
                usedIds.add(q.id);
            }
        }

        // --- 階段 D：兜底 ---
        if (selected.length < EXAM_LIMIT) {
            const fallback = allQuestions.filter(q => !usedIds.has(q.id)).sort(() => 0.5 - Math.random());
            while (selected.length < EXAM_LIMIT && fallback.length > 0) {
                const q = fallback.shift();
                selected.push(q);
                usedIds.add(q.id);
            }
        }

        // 3. 更新歷史
        selected.forEach(q => historySet.add(q.id));
        if (historySet.size > (allQuestions.length * 0.9)) historySet.clear();
        localStorage.setItem(HISTORY_KEY, JSON.stringify([...historySet]));

        examQuestions = selected.sort((a, b) => {
            const catA = a.category || "";
            const catB = b.category || "";
            return catA.localeCompare(catB) || (a.id - b.id);
        }).slice(0, EXAM_LIMIT);
        renderQuestion(0); startTimer();
    }

    function renderQuestion(index, scrollTop = true) {
        currentIndex = index; const item = examQuestions[index]; 
        if (item.type === 'matching') { renderMatchingQuestion(index); return; }
        const container = document.getElementById('question-area'); 
        if (!container) return;
        container.innerHTML = '';
        const progressEl = document.getElementById('q-progress');
        if (progressEl) progressEl.innerText = `${index + 1} / ${examQuestions.length}`;
        const sidePrev = document.getElementById('side-btn-prev'), sideNext = document.getElementById('side-btn-next');
        if (sidePrev) sidePrev.style.display = index === 0 ? 'none' : 'flex';
        if (sideNext) { sideNext.style.display = 'flex'; sideNext.title = index === (examQuestions.length-1) ? '交卷' : '下一題'; }
        
        const card = document.createElement('div'); card.className = 'card question-card';
        let qText = processContent(item.question, item);
        let html = `<div class="question-header">題目 ${index + 1} / ${examQuestions.length} <span class="badge bg-secondary small ms-2">${item.category || ''}</span></div><div class="question-body"><div class="mb-4">${qText}</div>`;
        if (item.image) html += `<div class="text-center mb-4"><img src="${item.image}" style="max-width:100%; border:1px solid #ddd; border-radius:4px;"></div>`;
        const optionsRaw = item.quiz || item.options || [];
        const options = Array.isArray(optionsRaw) ? optionsRaw : [optionsRaw];
        const savedAns = userAnswers[index] !== undefined ? userAnswers[index] : {};
        html += '<div class="mt-3">';
        options.forEach((opt, optIdx) => {
            const optStr = String(opt);
            let labelText = `(${String.fromCharCode(65 + optIdx)}) `;
            if (item.labelType === 'num') labelText = `${optIdx + 1}. `;
            const numStyle = (item.labelType === 'none' || item.hideLabel) ? 'style="display:none"' : '';
            
            if (optStr.includes('|')) {
                const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                const customLabelField = "question" + alphabet[optIdx];
                let customLabel = "";
                if (item[customLabelField]) {
                    customLabel = Array.isArray(item[customLabelField]) ? item[customLabelField].join('<br>') : item[customLabelField];
                }
                const displayLabel = customLabel || `選項 ${optIdx + 1}`;

                const subOpts = optStr.split('|'); html += `<div class="sub-question-label">${displayLabel}</div><div class="d-flex flex-wrap gap-2 mb-3 ms-2">`;
                subOpts.forEach((sub, subIdx) => { 
                    const isSel = (savedAns && savedAns[optIdx] === subIdx); 
                    let subLabel = `(${String.fromCharCode(65 + subIdx)}) `;
                    if (item.labelType === 'num') subLabel = `(${subIdx+1}) `;
                    html += `<div class="sub-opt-container ${isSel ? 'selected' : ''}" onclick="selectSub(${optIdx}, ${subIdx})"><span class="opt-num" ${numStyle}>${subLabel}</span>${sub}</div>`; 
                });
                html += `</div>`;
            } else {
                const isSel = Array.isArray(userAnswers[index]) ? userAnswers[index].includes(optIdx) : (userAnswers[index] === optIdx);
                html += `<div class="option-item ${isSel ? 'selected' : ''}" onclick="selectOption(${optIdx})"><span class="opt-num" ${numStyle}>${labelText}</span>${optStr}</div>`;
            }
        });
        html += '</div></div>'; card.innerHTML = html; container.appendChild(card);
        if (scrollTop) window.scrollTo(0, 0); setTimeout(() => { if(window.Prism) Prism.highlightAll(); }, 50);
    }

    function selectOption(optIdx) {
        const item = examQuestions[currentIndex];
        if (item.type === 'multiple') {
            if (!Array.isArray(userAnswers[currentIndex])) userAnswers[currentIndex] = [];
            const idx = userAnswers[currentIndex].indexOf(optIdx);
            if (idx > -1) userAnswers[currentIndex].splice(idx, 1);
            else userAnswers[currentIndex].push(optIdx);
        } else { userAnswers[currentIndex] = optIdx; }
        renderQuestion(currentIndex, false);
    }
    function selectSub(qIdx, subIdx) { if (!userAnswers[currentIndex] || typeof userAnswers[currentIndex] !== 'object') userAnswers[currentIndex] = {}; userAnswers[currentIndex][qIdx] = subIdx; renderQuestion(currentIndex, false); }
    function changeQuestion(step) { if (currentIndex + step >= 0 && currentIndex + step < examQuestions.length) { renderQuestion(currentIndex + step); } else if (currentIndex + step >= examQuestions.length) { confirmSubmit(); } }
    function confirmSubmit() { if (confirm("確定要交卷嗎？")) { submitExam(); } }

    function submitExam() {
        clearInterval(timerInterval); 
        const ui = document.getElementById('exam-ui'), rs = document.getElementById('result-screen');
        if (ui) ui.style.display = 'none'; if (rs) rs.style.display = 'block';
        let correctCount = 0, stats = {}, incorrectHTML = '';
        const catNameMap = {};
        allQuestions.forEach(q => {
            let fullCat = q.category || '一般';
            let _m = fullCat.match(/^(D\d+)/); let prefix = (_m ? _m[1] : fullCat);
            if (!catNameMap[prefix] || fullCat.length > catNameMap[prefix].length) catNameMap[prefix] = fullCat;
        });
        examQuestions.forEach((item, idx) => {
            let _m = (item.category ? item.category.match(/^(D\d+)/) : null); let prefix = (_m ? _m[1] : item.category || '一般');
            const cat = catNameMap[prefix];
            if (!stats[cat]) stats[cat] = { total: 0, correct: 0, ids: [] }; 
            stats[cat].total++;
            stats[cat].ids.push(item.id);
            const userAns = userAnswers[idx]; let isCorrect = false;
            const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
            if (item.type === 'matching') {
                const userLetters = (userAns || []).map(idx => idx === null ? "" : String.fromCharCode(65 + idx));
                isCorrect = JSON.stringify(userLetters) === JSON.stringify(answers);
            } else if (item.type === 'multioption' || (item.quiz || item.options || []).some(o => String(o).includes('|'))) {
                isCorrect = answers.every((a, i) => userAns && parseAnswerToIndex(a) === userAns[i]);
            } else if (item.type === 'multiple') {
                const cIdxs = answers.map(a => parseAnswerToIndex(a));
                isCorrect = Array.isArray(userAns) && userAns.length === cIdxs.length && userAns.every(val => cIdxs.includes(val));
            } else { isCorrect = userAns === parseAnswerToIndex(item.answer[0] || item.answer); }
            
            const isNum = (item.labelType === 'num');
            let ansText = answers.map(a => {
                if (String(a).toUpperCase() === 'Y' || String(a).toUpperCase() === 'N') return a;
                const idx = parseAnswerToIndex(a);
                if (idx < 0) return a;
                return isNum ? (idx + 1) : String.fromCharCode(65 + idx);
            }).join(', ');

            if (isCorrect) { correctCount++; stats[cat].correct++; }
            else {
                const optsRaw = item.quiz || item.options || [];
                const opts = Array.isArray(optsRaw) ? optsRaw : [optsRaw];
                let optionsHTML = '<div class="review-opts" style="margin-left:20px; margin-top:10px; font-size:0.9rem; color:#666;">';
                
                if (item.type === 'matching') {
                    optionsHTML += `<div class="matching-wrapper print-matching" id="pmock-${idx}" data-idx="${idx}" style="margin: 20px 0; position:relative; width:100%; display:block; -webkit-print-color-adjust:exact; print-color-adjust:exact;">
                        <svg class="print-svg" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:10; overflow:visible; display:block;"></svg>
                        <table style="width:100%; border-collapse:collapse; border:1px solid #333; position:relative; z-index:5;">
                            <thead>
                                <tr style="background:#f8f9fa;">
                                    <th style="width:46%; text-align:left; color:#0d6efd; border:1px solid #333; padding:8px 12px; font-size:1.1rem;">程式碼片段</th>
                                    <th style="width:8%; border:1px solid #333;"></th>
                                    <th style="width:46%; text-align:right; color:#0d6efd; border:1px solid #333; padding:8px 12px; font-size:1.1rem;">正確對應回答</th>
                                </tr>
                            </thead>
                            <tbody>`;
                    
                    const maxRows = Math.max(item.left.length, item.right.length);
                    for (let r = 0; r < maxRows; r++) {
                        const lText = item.left[r] || "";
                        const rText = item.right[r] || "";
                        optionsHTML += `<tr>
                            <td style="padding:10px; border:1px solid #333; vertical-align:middle;">
                                ${lText ? `<div style="display:flex; align-items:center; justify-content:flex-end;"><div style="font-family:Consolas,monospace;">${lText}</div><div class="match-dot" id="mdl-${idx}-${r}" style="width:18px; height:18px; margin:0 10px; border:2.5px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div></div>` : ''}
                            </td>
                            <td style="border:1px solid #333;"></td>
                            <td style="padding:10px; border:1px solid #333; vertical-align:middle;">
                                ${rText ? `<div style="display:flex; align-items:center; justify-content:flex-start;"><div class="match-dot" id="mdr-${idx}-${r}" style="width:18px; height:18px; margin:0 10px; border:2.5px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div><div style="font-family:Consolas,monospace;">${rText}</div></div>` : ''}
                            </td>
                        </tr>`;
                    }
                    optionsHTML += `</tbody></table></div>`;
                } else {
                    opts.forEach((o, i) => {
                        const isNum = (item.labelType === 'num');
                        const numStyle = (item.labelType === 'none' || item.hideLabel) ? 'style="display:none"' : '';
                        if (String(o).includes('|')) {
                            const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                            const customLabelField = "question" + alphabet[i];
                            let customLabel = "";
                            if (item[customLabelField]) {
                                customLabel = Array.isArray(item[customLabelField]) ? item[customLabelField].join(' ') : item[customLabelField];
                            }
                            const displayLabel = customLabel || `選項 ${i + 1}`;

                            const subLabels = o.split('|').map((s, si) => {
                                const lbl = isNum ? (si + 1) : String.fromCharCode(65 + si);
                                return `<span class="opt-num" ${numStyle}>(${lbl})</span>${s}`;
                            }).join(' ');
                            optionsHTML += `<div class="mb-1" style="display:flex; align-items:flex-start; gap:8px;"><span class="fw-bold">${displayLabel}</span> ${subLabels}</div>`;
                        }
                        else {
                            const lbl = isNum ? (i + 1) + "." : `(${String.fromCharCode(65 + i)})`;
                            optionsHTML += `<div class="mb-1" style="display:flex; align-items:flex-start; gap:8px;"><span class="opt-num" ${numStyle}>${lbl} </span>${o}</div>`;
                        }
                    });
                }
                optionsHTML += '</div>';
                incorrectHTML += `<div class="review-item"><div class="review-id">題目 ${idx + 1} (編號: ${item.id})</div><div class="review-q-text"><div class="q-content">${processContent(item.question, item)}</div></div>${optionsHTML}<div class="review-ans">正確答案：${ansText}</div><div class="review-exp"><b>解析：</b><br/>${processContent(item.explanation || '暫無解析。', item)}</div></div>`;
            }
        });
        const score = Math.round((correctCount / examQuestions.length) * 100);
        document.getElementById('final-score').innerText = score; document.getElementById('correct-count').innerText = correctCount;
        let catHTML = '<h5 class="text-center mb-3">各類答對率統計</h5><table class="table table-bordered"><thead><tr><th class="text-start">分類</th><th class="text-start">出題編號</th><th>題數</th><th>答對率</th></tr></thead><tbody>';
        const sortedCats = Object.keys(stats).sort();
        const CUTOFF = REPLACE_CUTOFF;
        for (let cat of sortedCats) {
            let total = stats[cat].total, correct = stats[cat].correct, p = Math.round((correct / total) * 100);
            let sortedIds = stats[cat].ids.sort((a, b) => a - b).map(id => {
                return id > CUTOFF ? `<span style="color:red; font-weight:bold;">${id}</span>` : id;
            }).join(', ');
            catHTML += `<tr><td class="text-start fw-bold">${cat}</td><td class="text-start small" style="max-width:400px; word-break:break-all;">${sortedIds}</td><td>${total}</td><td>${p}%</td></tr>`;
        }
        catHTML += '</tbody></table>'; 
        document.getElementById('category-stats').innerHTML = catHTML;
        let reportSummary = `<div class="review-item" style="border: 2px solid #0d6efd; background: #f0f7ff;"><h2 class="text-center" style="color: #0d6efd;">模擬考試成績報告</h2><div class="d-flex justify-content-around mt-3"><div class="text-center"><h4>總分: <span style="font-size: 2rem;">${score}</span></h4></div><div class="text-center"><h4>答對題數: ${correctCount} / ${examQuestions.length}</h4></div></div><div class="mt-3">${catHTML}</div></div>`;
        document.getElementById('review-list').innerHTML = reportSummary + incorrectHTML;
        // 確保結果區塊已顯示，以便正確計算 getBoundingClientRect (使用已宣告的 rs)
        if (rs) rs.style.display = 'block';
        
        // 繪製模擬考試報告中的正確連線 (視窗座標差值法修正)
        setTimeout(() => {
            document.querySelectorAll('.print-matching').forEach(wrapper => {
                const qIdx = parseInt(wrapper.getAttribute('data-idx'));
                const item = examQuestions[qIdx];
                const svg = wrapper.querySelector('.print-svg');
                const wRect = wrapper.getBoundingClientRect();
                if (wRect.width === 0) return;
                
                svg.setAttribute('width', wRect.width);
                svg.setAttribute('height', wRect.height);
                svg.style.width = wRect.width + 'px';
                svg.style.height = wRect.height + 'px';
                svg.innerHTML = ''; 
                
                const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
                answers.forEach((ansVal, lIdx) => {
                    const rIdx = parseAnswerToIndex(ansVal);
                    const dotL = document.getElementById(`mdl-${qIdx}-${lIdx}`);
                    const dotR = document.getElementById(`mdr-${qIdx}-${rIdx}`);
                    if (dotL && dotR) {
                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const x1 = rL.left - wRect.left + rL.width/2;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2;
                        const y2 = rR.top - wRect.top + rR.height/2;
                        
                        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                        line.setAttribute('x1', x1.toFixed(2)); line.setAttribute('y1', y1.toFixed(2)); 
                        line.setAttribute('x2', x2.toFixed(2)); line.setAttribute('y2', y2.toFixed(2));
                        line.setAttribute('stroke', "#198754"); line.setAttribute('stroke-width', "5"); 
                        line.setAttribute('stroke-linecap', "round"); 
                        line.setAttribute('style', "stroke-opacity:1 !important;");
                        svg.appendChild(line);
                    }
                });
                const html = svg.innerHTML; svg.innerHTML = ''; svg.innerHTML = html;
            });
            if(window.Prism) Prism.highlightAll();
        }, 2000);
        try {
            let wrongSet = new Set(JSON.parse(localStorage.getItem(WRONG_KEY) || '[]'));
            examQuestions.forEach((q, idx) => {
                const userAns = userAnswers[idx]; const answers = Array.isArray(q.answer) ? q.answer : [q.answer];
                let isCorr = false;
                if (q.type === 'multioption' || (q.quiz || q.options || []).some(o => String(o).includes('|'))) isCorr = answers.every((a, i) => userAns && parseAnswerToIndex(a) === userAns[i]);
                else if (q.type === 'multiple') { const cIdxs = answers.map(a => parseAnswerToIndex(a)); isCorr = Array.isArray(userAns) && userAns.length === cIdxs.length && userAns.every(v => cIdxs.includes(v)); }
                else isCorr = userAns === parseAnswerToIndex(q.answer[0] || q.answer);
                if (isCorr) wrongSet.delete(q.id); else wrongSet.add(q.id);
            });
            localStorage.setItem(WRONG_KEY, JSON.stringify([...wrongSet]));
        } catch(e) {}
    }
    initExam();
</script>
</body>
</html>"""

    # --- 模板 B: 自主練習模板 (含配對題支援與縮放按鈕) ---
    prac_top_tmpl = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REPLACE_TITLE 認證練習</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
    <style>
        html { scrollbar-gutter: stable; }
        body { background-color: #f8f9fa; font-family: "Microsoft JhengHei", "Segoe UI", sans-serif; overflow-x: hidden !important; }
        .main-wrapper { display: flex; min-height: 100vh; }
        .sidebar { width: 280px; background: #fff; border-right: 1px solid #dee2e6; display: flex; flex-direction: column; position: fixed; top: 0; bottom: 0; left: 0; z-index: 1000; transition: transform 0.3s ease; height: 100vh; }
        .sidebar-header { background: #212529; color: #fff; padding: 15px; border-bottom: 1px solid #dee2e6; flex-shrink: 0; }
        .sidebar-header h5 { font-size: 1.25rem; font-weight: bold; color: #fff; margin-bottom: 0; }
        #progress-stats { font-size: 1.2rem; font-weight: bold; color: #fff; }
        .sidebar-content { flex: 1; overflow-y: auto !important; padding: 15px; }
        .sidebar-footer { padding: 15px; border-top: 1px solid #dee2e6; background: #f8f9fa; flex-shrink: 0; }
        .content-area { flex: 1; margin-left: 280px; padding: 0; transition: margin-left 0.3s ease; overflow-x: hidden !important; }
        
        code:not([class*="language-"]) { display: inline-block; margin: 5px 0; line-height: 1.4; font-size: 1.0rem; color: #222222; }
        code { background-color: transparent !important; font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace; }
        code[class*="language-"], pre[class*="language-"] { color: #333 !important; text-shadow: none !important; background: #fdfdfd !important; white-space: pre-wrap !important; word-break: break-all !important; }
        .token.operator, .token.entity, .token.url, .language-css .token.string, .style .token.string { background: none !important; }

        .form-check-input { border-radius: 50% !important; width: 1.2rem; height: 1.2rem; background-image: none !important; cursor: pointer; }
        .form-check-input:checked { background-color: #0d6efd !important; border-color: #0d6efd !important; }
        .option-item { border: 1px solid #e9ecef; border-radius: 6px; padding: 10px; margin-bottom: 8px; cursor: pointer; transition: 0.2s; display: flex; align-items: flex-start; gap: 8px; }
        .option-item pre { margin: 0; display: inline-block; width: 100%; }
        .option-item.correct, .sub-opt-container.correct { background-color: #d1e7dd !important; border-color: #badbcc !important; color: #000 !important; }
        .option-item.incorrect, .sub-opt-container.incorrect { background-color: #f8d7da !important; border-color: #f5c2c7 !important; color: #000 !important; }
        .sub-opt-container.selected { background-color: #e7f1ff !important; border-color: #9ec5fe !important; color: #000 !important; }
        .q-node { aspect-ratio: 1; display: flex; align-items: center; justify-content: center; border: 1px solid #dee2e6; border-radius: 6px; background-color: #fff; cursor: pointer; font-size: 0.85rem; }
        .q-node.correct { background-color: #d1e7dd; color: #0f5132; }
        .q-node.incorrect { background-color: #f8d7da; color: #842029; }
        .q-node.corrected { background-color: #fd7e14; color: #fff; }
        .q-node.active { background-color: #0d6efd; color: white; transform: scale(1.1); z-index: 1; }
        .progress-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }
        .category-tag { font-size: 0.8rem; color: #6c757d; background-color: #f8f9fa; padding: 2px 8px; border-radius: 12px; border: 1px solid #dee2e6; margin-top: 5px; display: inline-block; }
        .type-badge { font-size: 0.75rem; vertical-align: middle; }
        .question-card { border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; }
        .question-header { border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; display: flex; justify-content: space-between; align-items: center; }
        .question-body { padding: 5px 20px; font-size: 1.0rem; word-wrap: break-word; word-break: normal; overflow-x: hidden; line-height: 1.8; }
        .answer-section { display: none; margin-top: 20px; padding: 20px; background: #fff; border: 2px solid #0d6efd; border-radius: 8px; }
        .explanation, .explanation pre, .explanation code, .review-exp-box pre, .review-exp-box code, pre[class*="language-"], code[class*="language-"] { white-space: pre-wrap !important; word-wrap: break-word !important; word-break: break-all !important; overflow-wrap: anywhere !important; }
        
        #review-area { display: none; text-align: left; padding: 20px; background: white; }
                    .review-item { border-bottom: 1px solid #eee !important; width: 100% !important; page-break-inside: auto; margin: 0 0 2px 0 !important; padding: 0 !important; }
                    .review-q-text { font-size: 1.0rem; line-height: 1.6 !important; margin-bottom: 2px !important; color: #333; }
                    .review-ans { color: #198754; font-weight: bold; padding: 4px 15px !important; margin: 2px 0 !important; border-left: 5px solid #198754; background: white; font-size: 1.0rem; }
            .review-exp-box { background: #f8f9fa; padding: 8px !important; border-radius: 10px; border: 1px solid #eeeeee; line-height: 1.5 !important; color: #333; font-size: 0.95rem; }
            
            /* 列印版配對題佈局鎖定 */
            .print-matching { display: block !important; width: 100% !important; position: relative !important; margin: 15px 0 !important; }
            .match-header-row, .matching-columns { display: block !important; width: 100% !important; clear: both !important; }
            .match-header-title, .match-col { display: inline-block !important; width: 48% !important; vertical-align: top !important; }
            .match-item { display: flex !important; width: 100% !important; margin-bottom: 5px !important; }
            .print-svg { position: absolute !important; top: 0 !important; left: 0 !important; width: 100% !important; height: 100% !important; z-index: 10 !important; background: none !important; }
        
        @media print {
            @page { size: auto; margin: 8mm !important; }
            * { box-sizing: border-box !important; -webkit-print-color-adjust: exact; overflow: visible !important; }
            html, body { margin: 0 !important; padding: 0 !important; width: 100% !important; background: white !important; font-size: 1.0rem !important; line-height: 1.8 !important; }
            .main-wrapper, .mobile-toggle, .side-nav-btn, .no-print, .sidebar { display: none !important; }
            .content-area { margin-left: 0 !important; padding: 0 !important; margin-top: 0 !important; }
            #review-area { display: block !important; width: 100% !important; padding: 0 !important; margin: 0 !important; }
            .review-item { border-bottom: 1px solid #eee !important; width: 100% !important; page-break-inside: auto; margin: 0 0 10px 0 !important; padding: 0 !important; }
            .review-ans { color: #198754 !important; font-weight: bold !important; padding: 8px 5px !important; border-left: 5px solid #198754 !important; margin: 5px 0 !important; }
            pre, code { white-space: pre-wrap !important; word-break: break-all !important; border: none !important; font-size: 1.0rem !important; margin: 0 !important; padding: 0 !important; }
            .q-table, table { font-size: 0.7rem !important; max-width: 98% !important; margin: 10px 0 !important; page-break-inside: avoid; -webkit-print-color-adjust: exact; border-collapse: collapse !important; }
            .q-table td, .q-table th, td, th { border: 1px solid #000 !important; padding: 6px !important; }
        }
        .side-nav-btn { position: fixed; top: 55%; width: 25px; height: 65px; background: rgba(108, 117, 125, 0.7); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 2000; transition: left 0.3s ease, background 0.3s, width 0.2s; text-decoration: none; font-size: 1.1rem; border: none; font-family: serif; font-weight: bold; transform: translateY(-50%); }
        .side-nav-btn:hover { background: #0d6efd; color: white; width: 30px; }
        .side-nav-prev { left: 280px; border-radius: 0 15px 15px 0; }
        .side-nav-next { right: 0; border-radius: 15px 0 0 15px; }
        @media (max-width: 992px) {
            .sidebar { transform: translateX(-100%); }
            .sidebar.active { transform: translateX(0); }
            .content-area { margin-left: 0; }
            .mobile-toggle { display: block !important; }
            .side-nav-btn { width: 22px; height: 50px; font-size: 0.9rem; background: rgba(33, 37, 41, 0.6); }
            .side-nav-btn.side-nav-prev { left: 0; border-radius: 0 15px 15px 0; }
            .sidebar.active ~ .side-nav-btn.side-nav-prev { left: 280px !important; }
        }
        .mobile-toggle { display: none; position: fixed; bottom: 20px; right: 20px; z-index: 1100; width: 50px; height: 50px; border-radius: 50%; background: #212529; color: white; border: none; }
        pre { background-color: transparent !important; border: none !important; line-height: 1.6; white-space: pre-wrap !important; word-wrap: break-word !important; word-break: break-all !important; overflow-x: hidden !important; margin: 0 !important; padding: 0 !important; }
        .question-body pre { margin-bottom: 0 !important; }
        
        /* 縮放與配對題樣式整合 */
        #zoom-controls { position: fixed; bottom: 85px; right: 20px; z-index: 2147483647; display: flex; flex-direction: column; gap: 12px; pointer-events: auto; }
        .zoom-btn { width: 52px; height: 52px; border-radius: 50%; background: #212529; color: white; border: 2px solid #fff; font-size: 26px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5); cursor: pointer; user-select: none; transition: none !important; }
        #question-container { transform-origin: top center; transition: none !important; position: relative; z-index: 1; }
        .matching-wrapper { position: relative; margin: 10px 0 15px 0 !important; padding: 0 10px 10px 10px !important; width: 100%; user-select: none; touch-action: pan-y pinch-zoom; overflow: visible !important; }
        .match-header-title { font-weight: bold; color: #666; font-size: 1.1rem; border-bottom: 1px solid #eee; margin-bottom: 10px; padding-bottom: 5px; }
        .right-col .match-header-title { margin-left: 10px; }
        .matching-columns { display: flex !important; justify-content: flex-start !important; align-items: flex-start !important; gap: 60px !important; position: relative; z-index: 2; padding-left: 10px !important; width: max-content !important; }
        .match-col { display: flex !important; flex-direction: column !important; gap: 25px !important; width: max-content !important; flex: none !important; }
        .match-item { display: flex !important; align-items: center !important; min-height: 45px !important; cursor: pointer !important; width: max-content !important; }
        .match-item-left { justify-content: flex-start !important; text-align: left !important; }
        .match-item-right { justify-content: flex-start !important; text-align: left !important; }
        .match-item-left .q-text-part { display: inline-block !important; }
        .match-dot { width: 22px !important; height: 22px !important; border: 1.5px solid #333 !important; border-radius: 50% !important; display: flex !important; align-items: center !important; justify-content: center !important; background: #fff !important; position: relative !important; flex-shrink: 0 !important; margin: 0 10px !important; }
        .match-item.matched .match-dot::after, .match-item.selected .match-dot::after { background: #333; }
        .match-item.selected .match-dot { border-color: #0d6efd; }
        #matching-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
        @media (max-width: 768px) {
            .matching-columns, .match-header-row { gap: 60px !important; }
            .match-col { min-width: 140px !important; }
            .match-header-title { font-size: 1rem !important; }
            .match-item { font-size: 0.9rem !important; }
            .match-dot { width: 18px !important; height: 18px !important; margin: 0 10px !important; }
            .match-dot::after { width: 8px !important; height: 8px !important; }
        }
    </style>
</head>
<body>
    <div id="zoom-controls">
        <button type="button" class="zoom-btn" onclick="changeZoom(0.1)"><b>+</b></button>
        <button type="button" class="zoom-btn" onclick="changeZoom(-0.1)"><b>−</b></button>
    </div>
<div class="main-wrapper">
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="d-flex align-items-center justify-content-between mb-2">
                <div class="d-flex align-items-center"><a href="../../index.html" class="text-decoration-none text-white me-2">🏠</a><h5 class="m-0" style="font-size: 1.1rem;">題庫列表</h5></div>
                <div class="d-flex gap-1">
                    <button type="button" onclick="prepareAndPrint()" class="btn btn-outline-light btn-sm py-1 px-2" style="font-size: 0.8rem;">完整解析</button>
                    <button type="button" onclick="prepareAndPrint(true)" class="btn btn-warning btn-sm py-1 px-2" style="font-size: 0.8rem; font-weight: bold;">錯題訂正</button>
                </div>
            </div>
            <div id="progress-stats">✅0 ❌0 🟠0 / REPLACE_TOTAL</div>
        </div>
        <div class="sidebar-content">
            <div class="progress-grid" id="progress-grid"></div>
        </div>
        <div class="sidebar-footer"><button class="btn btn-outline-danger btn-sm w-100" onclick="resetProgress()">重置 練習進度</button></div>
    </nav>
    <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>
    <div class="side-nav-btn side-nav-prev" id="side-btn-prev" onclick="prevQuestion()">&#10094;</div>
    <div class="side-nav-btn side-nav-next" id="side-btn-next" onclick="nextQuestion()">&#10095;</div>
    <main class="content-area"><div class="container-fluid" style="width: calc(100% - 60px); padding: 0; margin-left: auto; margin-right: auto; max-width: none;"><div id="question-container"></div></div></main>
</div>
<div id="review-area"></div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-csharp.min.js"></script>
<script>
    const quizData = """

    prac_bottom_tmpl = r"""
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
    const SUBJECT_ID = 'REPLACE_SUBJECT_ID';
    const CORR_KEY = SUBJECT_ID + '_correct_v1', INCORR_KEY = SUBJECT_ID + '_incorrect_v1', CORR_EDIT_KEY = SUBJECT_ID + '_corrected_v1', INDEX_KEY = SUBJECT_ID + '_index_v1', ANSWERS_KEY = SUBJECT_ID + '_answers_v1';
    function loadState() {
        try {
            const sCorr = localStorage.getItem(CORR_KEY), sIncorr = localStorage.getItem(INCORR_KEY), sEdit = localStorage.getItem(CORR_EDIT_KEY), sIdx = localStorage.getItem(INDEX_KEY), sAns = localStorage.getItem(ANSWERS_KEY);
            if (sCorr) correctSet = new Set(JSON.parse(sCorr));
            if (sIncorr) incorrectSet = new Set(JSON.parse(sIncorr));
            if (sEdit) correctedSet = new Set(JSON.parse(sEdit));
            if (sIdx) currentIndex = parseInt(sIdx) || 0;
            if (sAns) userAnswers = JSON.parse(sAns);
        } catch(e) {}
    }
    function saveState() {
        try {
            localStorage.setItem(CORR_KEY, JSON.stringify([...correctSet]));
            localStorage.setItem(INCORR_KEY, JSON.stringify([...incorrectSet]));
            localStorage.setItem(CORR_EDIT_KEY, JSON.stringify([...correctedSet]));
            localStorage.setItem(INDEX_KEY, currentIndex.toString());
            localStorage.setItem(ANSWERS_KEY, JSON.stringify(userAnswers));
        } catch(e) {}
    }
    function resetProgress() { 
        if(confirm('確定清除紀錄嗎？')) { 
            try { localStorage.removeItem(CORR_KEY); localStorage.removeItem(INCORR_KEY); localStorage.removeItem(CORR_EDIT_KEY); localStorage.removeItem(INDEX_KEY); localStorage.removeItem(ANSWERS_KEY); } catch(e) {}
            location.reload(); 
        } 
    }
    function toggleSidebar() { document.getElementById('sidebar').classList.toggle('active'); }
    function processContent(content, item) {
        if (!content) return '';
        const lines = Array.isArray(content) ? content : [String(content)];
        return lines.join(String.fromCharCode(10)).replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
            const num = parseInt(p1, 10);
            const src = item['image' + num] || item['image' + p1] || item['image'];
            return src ? `<img src="${src}" class="q-img">` : match;
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
            <div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizData.length}</span><span class="badge ${completed ? (isCorrected ? 'bg-warning' : 'bg-success') : (isWrong ? 'bg-danger' : 'bg-info')} type-badge">${isCorrected ? '更正題' : (isWrong ? '答錯題' : (isCorrect ? '答對題' : '配對題'))}</span></div><div class="category-tag">${item.category || '一般'}</div></div>
                                                                                    <div class="question-body" style="color:#333;">
                                                                                        <div class="mb-0" style="font-weight:600; font-size:1.1rem; margin: 0 !important; padding: 0 !important; display: block;">${processContent(item.question, item)}</div>
                                                                        `;
                                                                    html += `<div class="matching-wrapper" id="matching-wrapper" onmousemove="handleDragMove(event)" onmouseup="handleDragEnd(event)" ontouchmove="handleDragMove(event)" ontouchend="handleDragEnd(event)">
                    <svg id="matching-svg"></svg>
                    <div class="matching-columns">
                        <div class="match-col left-col">
                            <div class="match-header-title">程式碼片段</div>`;
        item.left.forEach((text, lIdx) => {
            const isMatched = currentAns[lIdx] !== null;
            const dotColor = completed ? (isCorrected ? '#fd7e14' : '#198754') : (isWrong ? '#dc3545' : (isMatched ? '#333' : 'transparent'));
            html += `<div class="match-item match-item-left ${isMatched?'matched':''}" id="left-item-${lIdx}"><div class="q-text-part" style="font-family:Consolas,monospace; white-space:nowrap;">${text}</div><div class="match-dot" id="dot-left-${lIdx}" onmousedown="${completed?'':`handleDragStart(event, 'left', ${lIdx})`}" ontouchstart="${completed?'':`handleDragStart(event, 'left', ${lIdx})`}"><div style="width:10px; height:10px; border-radius:50%; background:${dotColor};"></div></div></div>`;
        });
        html += `</div><div class="match-col right-col">
                    <div class="match-header-title">回答區</div>`;
        item.right.forEach((text, rIdx) => {
            const isMatchedByAny = currentAns.includes(rIdx);
            const dotColor = completed ? (isCorrected ? '#fd7e14' : '#198754') : (isWrong ? '#dc3545' : (isMatchedByAny ? '#333' : 'transparent'));
            html += `<div class="match-item match-item-right ${isMatchedByAny?'matched':''}" id="right-item-${rIdx}" data-right-idx="${rIdx}"><div class="match-dot" id="dot-right-${rIdx}"><div style="width:10px; height:10px; border-radius:50%; background:${dotColor};"></div></div><div style="font-family:Consolas,monospace;">${text}</div></div>`;
        });
        html += `</div></div></div>`;
        if (!completed) html += `<div class="text-center mt-5 mb-3 border-top pt-4"><button class="btn btn-primary px-5 btn-lg" onclick="submitMatching()">確認提交</button></div>`;
        else {
            const ansText = item.answer.join(', ');
            html += `<div class="answer-section" style="display:block;">
                        <div class="fw-bold mb-2 ${isCorrected?'text-warning':'text-success'}">${isCorrected?'🟠 已更正成功！':'✅ 答對了！'}</div>
                        <div class="review-ans" style="margin: 10px 0;">正確答案：${ansText}</div>
                        <div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div>
                     </div>`;
        }
        html += `</div></div></div>`; container.innerHTML = html; updateUI(); saveState();
        window.changeZoom(0); 
        // 動態偵測字寬對齊 (V3.5.3 結構化對齊)
        setTimeout(() => {
            const parts = container.querySelectorAll('.match-item-left .q-text-part');
            let maxW = 0; parts.forEach(p => maxW = Math.max(maxW, p.offsetWidth));
            parts.forEach(p => p.style.width = (maxW + 2) + 'px');
            drawLines();
        }, 30);
    }
    let isDragging = false, dragStartPoint = null, tempLine = null;
    window.handleDragStart = function(e, side, idx) {
        if (side !== 'left') return;
        if (userAnswers[currentIndex] && userAnswers[currentIndex][idx] !== null) { userAnswers[currentIndex][idx] = null; renderMatchingQuestion(currentIndex); }
        isDragging = true; if(e.cancelable) e.preventDefault();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX, clientY = e.touches ? e.touches[0].clientY : e.clientY;
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
        let x = window.lastClientX, y = window.lastClientY;
        if (e && e.changedTouches && e.changedTouches[0]) { x = e.changedTouches[0].clientX; y = e.changedTouches[0].clientY; }
        else if (e && e.clientX !== undefined) { x = e.clientX; y = e.clientY; }
        
        if (Number.isFinite(x) && Number.isFinite(y)) {
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
        svg.setAttribute('viewBox', `0 0 ${baseW} ${baseH}`);
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
        // 允許部分提交：移除 ans.includes(null) 的強制攔截
        const userAnswersAsLetters = (ans || []).map(idx => idx === null ? "" : String.fromCharCode(65 + idx));
        const isCorrect = JSON.stringify(userAnswersAsLetters) === JSON.stringify(item.answer);
        if (isCorrect) {
            if (incorrectSet.has(currentIndex)) { incorrectSet.delete(currentIndex); correctedSet.add(currentIndex); }
            else { correctSet.add(currentIndex); }
        } else {
            incorrectSet.add(currentIndex); correctSet.delete(currentIndex); correctedSet.delete(currentIndex);
        }
        renderMatchingQuestion(currentIndex);
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
            const inputs = document.querySelectorAll(`input[name="q${qIdx}"]`);
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
                document.querySelectorAll(`input[name="q${qIdx}"]`).forEach(i => i.disabled = true);
            } else {
                element.classList.add('incorrect'); incorrectSet.add(qIdx);
                const ci = document.getElementById(`o${correctIndices[0]}`); if (ci) ci.closest('.option-item').classList.add('correct');
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
            document.querySelectorAll(`input[name="q${qIdx}_opt${optIdx}"]`).forEach(i => i.disabled = true);
        } else {
            element.classList.add('incorrect'); incorrectSet.add(qIdx);
            const ci = document.getElementById(`o${optIdx}_s${correctSubIdx}`); if (ci) ci.parentElement.classList.add('correct');
            toggleExplanation(true);
        }
        saveState(); updateUI();
    }
    function evaluateCurrentQuestion() {
        const item = quizData[currentIndex], qIdx = currentIndex;
        if (correctSet.has(qIdx) || correctedSet.has(qIdx) || incorrectSet.has(qIdx)) return;
        const saved = userAnswers[qIdx]; if (!saved) return; 
        let answers = item.answer; if (!Array.isArray(answers)) answers = [answers];
        const correctIndices = answers.map(a => parseAnswerToIndex(a));
        if (item.type === 'multiple') {
            const selected = Array.isArray(saved) ? saved : []; if (selected.length === 0) return;
            if (selected.length === correctIndices.length && selected.every(v => correctIndices.includes(v))) correctSet.add(qIdx); else incorrectSet.add(qIdx);
        } else if (String(item.quiz || item.options || "").includes('|')) {
            const totalSub = (item.quiz || item.options || []).length;
            let allCorrect = (Object.keys(saved).length === totalSub);
            if (allCorrect) { for(let i=0; i<totalSub; i++) if (parseInt(saved[i]) != parseAnswerToIndex(answers[i])) { allCorrect = false; break; } }
            if (allCorrect) correctSet.add(qIdx); else incorrectSet.add(qIdx);
        }
        saveState(); updateUI();
    }
    function nextQuestion() { evaluateCurrentQuestion(); if (currentIndex < quizData.length-1) renderQuestion(currentIndex+1); }
    function prevQuestion() { evaluateCurrentQuestion(); if (currentIndex > 0) renderQuestion(currentIndex-1); }
    function jumpTo(idx) { evaluateCurrentQuestion(); renderQuestion(idx); }
            function prepareAndPrint(onlyMistakes = false) {
                const area = document.getElementById('review-area');
                if (!area) return;
                area.style.display = 'block'; // 強制顯示以計算座標
                let title = "REPLACE_TITLE 認證完整解析";
        
            let targetItems = quizData.map((item, idx) => ({ item, idx }));
            if (onlyMistakes) {
                targetItems = targetItems.filter(({ idx }) => incorrectSet.has(idx) || correctedSet.has(idx));
                if (targetItems.length === 0) { alert('目前沒有錯題或訂正紀錄可供列印！'); return; }
                title = "REPLACE_TITLE 訂正解析講義";
            }
            area.innerHTML = `<h1 class="text-center mb-4" style="color:#212529">${title}</h1>`;
            targetItems.forEach(({ item, idx }) => {
                const div = document.createElement('div'); div.className = 'review-item';
                const optsRaw = item.quiz || item.options || [];
                const opts = Array.isArray(optsRaw) ? optsRaw : [optsRaw];
                const isNum = (item.labelType === 'num');
                const numStyle = (item.labelType === 'none' || item.hideLabel) ? 'style="display:none"' : '';
                
                let optHtml = "";
                            if (item.type === 'matching') {
                                optHtml = `<div class="matching-wrapper print-matching" id="print-match-${idx}" data-idx="${idx}" style="margin: 20px 0; position:relative; width:100%; display:block; -webkit-print-color-adjust:exact; print-color-adjust:exact;">
                                    <svg class="print-svg" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:10; overflow:visible; display:block;"></svg>
                                    <table style="width:100%; border-collapse:collapse; border:1px solid #333; position:relative; z-index:5;">
                                        <thead>
                                            <tr style="background:#f8f9fa;">
                                                <th style="width:46%; text-align:left; color:#0d6efd; border:1px solid #333; padding:8px 12px; font-size:1.1rem;">程式碼片段</th>
                                                <th style="width:8%; border:1px solid #333;"></th>
                                                <th style="width:46%; text-align:right; color:#0d6efd; border:1px solid #333; padding:8px 12px; font-size:1.1rem;">正確對應回答</th>
                                            </tr>
                                        </thead>
                                        <tbody>`;
                                
                                const maxRows = Math.max(item.left.length, item.right.length);
                                for (let r = 0; r < maxRows; r++) {
                                    const lText = item.left[r] || "";
                                    const rText = item.right[r] || "";
                                    optHtml += `<tr>
                                        <td style="padding:10px; border:1px solid #333; vertical-align:middle;">
                                            ${lText ? `<div style="display:flex; align-items:center; justify-content:flex-end;"><div style="font-family:Consolas,monospace;">${lText}</div><div class="match-dot" id="pdl-${idx}-${r}" style="width:18px; height:18px; margin:0 10px; border:2.5px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div></div>` : ''}
                                        </td>
                                        <td style="border:1px solid #333;"></td>
                                        <td style="padding:10px; border:1px solid #333; vertical-align:middle;">
                                            ${rText ? `<div style="display:flex; align-items:center; justify-content:flex-start;"><div class="match-dot" id="pdr-${idx}-${r}" style="width:18px; height:18px; margin:0 10px; border:2.5px solid #198754; border-radius:50%; background:#fff; flex-shrink:0;"></div><div style="font-family:Consolas,monospace;">${rText}</div></div>` : ''}
                                        </td>
                                    </tr>`;
                                }
                                optHtml += `</tbody></table></div>`;
                            } else {
                
                    optHtml = opts.map((o, i) => {
                        if (String(o).includes('|')) {
                            const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                            const displayLabel = item["question" + alphabet[i]] || `選項 ${i + 1}`;
                            const subLabels = o.split('|').map((s, si) => `<span class="opt-num" ${numStyle}>(${isNum?(si+1):String.fromCharCode(65+si)})</span>${s}`).join(' ');
                            return `<div class="review-opt-line" style="margin-bottom:2px;"><span class="fw-bold">${displayLabel}</span> ${subLabels}</div>`;
                        } else {
                            return `<div class="review-opt-line" style="margin-bottom:2px;"><span class="opt-num" ${numStyle}>${isNum?(i+1)+'.':'('+String.fromCharCode(65+i)+')'} </span>${o}</div>`;
                        }
                    }).join('');
                }
    
                let cleanQ = Array.isArray(item.question) ? [...item.question] : [String(item.question)];
                if (cleanQ.length > 0) cleanQ[0] = cleanQ[0].replace(/^((?:<[^>]+>)*)\d+\.\s*/, '    ');
                const ansText = (Array.isArray(item.answer)?item.answer:[item.answer]).map(a => {
                    const idx = parseAnswerToIndex(a); return (idx < 0 || String(a).match(/[YN]/i)) ? a : (isNum ? (idx+1) : String.fromCharCode(65+idx));
                }).join(', ');
                div.innerHTML = `<div class="review-q-text"><b>${idx+1}.</b> <div class="q-content">${processContent(cleanQ, item)}</div></div>${item.image?`<div class="text-center my-2"><img src="${item.image}" class="q-img"></div>`:''}<div class="review-opts">${optHtml}</div><div class="review-ans">正確答案：${ansText}</div><div class="review-exp">${processContent(item.explanation || '暫無解析。', item)}</div>`;
                area.appendChild(div);
            });
            
                            // 繪製列印頁面的連線 (正確答案連線 - 標準答案畫上去)
                                                                                    // 繪製列印頁面的連線 (正確答案連線 - 視窗座標差值法)
                                                                                    setTimeout(() => {
                                                                                        document.querySelectorAll('.print-matching').forEach(wrapper => {
                                                                                            const qIdx = parseInt(wrapper.getAttribute('data-idx'));
                                                                                            const item = quizData[qIdx];
                                                                                            const svg = wrapper.querySelector('.print-svg');
                                                                                            const wRect = wrapper.getBoundingClientRect();
                                                                                            if (wRect.width === 0) return;
                                                                                            
                                                                                            svg.setAttribute('width', wRect.width);
                                                                                            svg.setAttribute('height', wRect.height);
                                                                                            svg.style.width = wRect.width + 'px';
                                                                                            svg.style.height = wRect.height + 'px';
                                                                                            svg.innerHTML = ''; 
                                                                                            
                                                                                            const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
                                                                                            answers.forEach((ansVal, lIdx) => {
                                                                                                const rIdx = parseAnswerToIndex(ansVal);
                                                                                                const dotL = document.getElementById(`pdl-${qIdx}-${lIdx}`);
                                                                                                const dotR = document.getElementById(`pdr-${qIdx}-${rIdx}`);
                                                                                                if (dotL && dotR) {
                                                                                                    const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                                                                                                    // 計算相對於 wrapper 的精確座標
                                                                                                    const x1 = rL.left - wRect.left + rL.width/2;
                                                                                                    const y1 = rL.top - wRect.top + rL.height/2;
                                                                                                    const x2 = rR.left - wRect.left + rR.width/2;
                                                                                                    const y2 = rR.top - wRect.top + rR.height/2;
                                                                                                    
                                                                                                    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                                                                                                    line.setAttribute('x1', x1.toFixed(2)); line.setAttribute('y1', y1.toFixed(2)); 
                                                                                                    line.setAttribute('x2', x2.toFixed(2)); line.setAttribute('y2', y2.toFixed(2));
                                                                                                    line.setAttribute('stroke', "#198754"); line.setAttribute('stroke-width', "5"); 
                                                                                                    line.setAttribute('stroke-linecap', "round"); 
                                                                                                    line.setAttribute('style', "stroke-opacity:1 !important;");
                                                                                                    svg.appendChild(line);
                                                                                                }
                                                                                            });
                                                                                            // 強制重繪 SVG
                                                                                            const html = svg.innerHTML; svg.innerHTML = ''; svg.innerHTML = html;
                                                                                        });
                                                                                        if(window.Prism) Prism.highlightAll(); 
                                                                                        setTimeout(() => { window.print(); }, 1000);
                                                                                    }, 2500);
                                                                                                                                                                    }
    
    function renderQuestion(index) {
        window.scrollTo(0, 0); currentIndex = index; const item = quizData[index];
        if (item.type === 'matching') { renderMatchingQuestion(index); return; }
        const container = document.getElementById('question-container');
        const opts = item.quiz || item.options || [];
        document.getElementById('side-btn-prev').style.display = (index === 0) ? 'none' : 'flex';
        let typeLabel = opts.some(o => String(o).includes('|')) ? "題組" : (item.type === 'multiple' ? "複選" : "單選");
        container.innerHTML = `<div class="card question-card"><div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizData.length}</span><span class="badge bg-info type-badge">${typeLabel}</span></div><div class="category-tag">${item.category || '一般'}</div></div><div class="question-body"><div>${processContent(item.question, item)}</div>${item.image ? `<img src="${item.image}" class="q-img">` : ''}<div class="options-area"></div><div class="text-center mt-4 pt-3 border-top"><button class="btn btn-outline-primary px-4" id="toggle-exp-btn" onclick="toggleExplanation()">👁️ 顯示答案 / 解析</button></div><div class="answer-section" id="ans-section"><h6 class="fw-bold mb-3">正確答案: <span class="text-blue">${Array.isArray(item.answer) ? item.answer.join(', ') : item.answer}</span></h6><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div></div></div>`;
        const optionsArea = container.querySelector('.options-area');
        opts.forEach((opt, oIdx) => {
            let labelText = (item.labelType === 'num') ? `${oIdx+1}. ` : `(${String.fromCharCode(65+oIdx)}) `;
            const numStyle = (item.labelType === 'none' || item.hideLabel) ? 'style="display:none"' : '';
            if (String(opt).includes('|')) {
                const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                const displayLabel = item["question" + alphabet[oIdx]] || `選項 ${oIdx + 1}`;
                let sHtml = `<div class="mt-2 mb-1"><code>${displayLabel}</code></div><div class="d-flex flex-wrap gap-2">`;
                opt.split('|').forEach((s, subIdx) => { 
                    sHtml += `<div class="sub-opt-container p-2 border rounded bg-light" onclick="checkSubAnswer(this, ${index}, ${oIdx}, ${subIdx}, event)" style="cursor:pointer; font-size:0.9rem"><input class="form-check-input" type="radio" name="q${index}_opt${oIdx}" id="o${oIdx}_s${subIdx}"><span class="opt-num" ${numStyle}>(${item.labelType==='num'?subIdx+1:String.fromCharCode(65+subIdx)})</span> ${s}</div>`; 
                });
                optionsArea.innerHTML += sHtml + '</div></div>';
            } else { optionsArea.innerHTML += `<div class="option-item" onclick="checkAnswer(this, ${index}, ${oIdx}, event)"><input class="form-check-input" type="${item.type==='multiple'?'checkbox':'radio'}" name="q${index}" id="o${oIdx}"><span class="opt-num" ${numStyle}>${labelText}</span>${opt}</div>`; }
        });
        const saved = userAnswers[index], completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);
        let answers = Array.isArray(item.answer) ? item.answer : [item.answer];
        let cIdxs = answers.map(a => parseAnswerToIndex(a));
        if (opts.some(o => String(o).includes('|'))) {
            opts.forEach((opt, r) => {
                const correctSubIdx = parseAnswerToIndex(answers[r]); const savedSubIdx = (saved && typeof saved === 'object') ? saved[r] : undefined;
                opt.split('|').forEach((_, subIdx) => {
                    const inp = document.getElementById(`o${r}_s${subIdx}`); if (!inp) return;
                    if (savedSubIdx !== undefined && parseInt(savedSubIdx) === subIdx) { inp.checked = true; inp.parentElement.classList.add('selected'); }
                    if (completed) { if (subIdx === correctSubIdx) inp.parentElement.classList.add('correct'); else if (savedSubIdx !== undefined && parseInt(savedSubIdx) === subIdx) inp.parentElement.classList.add('incorrect'); }
                });
            });
        } else if (saved !== undefined) {
            (Array.isArray(saved)?saved:[saved]).forEach(idx => { const inp = document.getElementById(`o${idx}`); if (inp) { inp.checked = true; if(completed) inp.closest('.option-item').classList.add(cIdxs.includes(idx) ? 'correct' : 'incorrect'); } });
            if(completed) cIdxs.forEach(ci => { const inp = document.getElementById(`o${ci}`); if (inp) inp.closest('.option-item').classList.add('correct'); });
        }
        if (completed) { toggleExplanation(true); document.querySelectorAll(`input[name^="q${index}"]`).forEach(i => i.disabled = true); }
        updateUI(); setTimeout(() => { if(window.Prism) Prism.highlightAll(); }, 50); saveState(); window.changeZoom(0);
    }
    function updateUI() {
        const stats = document.getElementById('progress-stats'); if (stats) stats.innerHTML = `✅${correctSet.size} ❌${incorrectSet.size} 🟠${correctedSet.size} <span class="ms-1 small" style="opacity:0.7">/ ${quizData.length}</span>`;
        const grid = document.getElementById('progress-grid'); grid.innerHTML = '';
        quizData.forEach((_, i) => {
            const n = document.createElement('div'); n.className = 'q-node'; if (i === currentIndex) { n.classList.add('active'); setTimeout(() => n.scrollIntoView({ block: 'center', behavior: 'smooth' }), 100); }
            if (incorrectSet.has(i)) n.classList.add('incorrect'); else if (correctedSet.has(i)) n.classList.add('corrected'); else if (correctSet.has(i)) n.classList.add('correct');
            n.innerText = i + 1; n.onclick = () => jumpTo(i); grid.appendChild(n);
        });
    }
    loadState(); window.addEventListener('resize', () => { if(window.drawLines) window.drawLines(); }); renderQuestion(currentIndex);
</script>
</body>
</html>"""

    for subj in config['subjects']:
        try:
            json_file = os.path.join(subj['dir'], subj['json'])
            if not os.path.exists(json_file): continue
            with open(json_file, 'rb') as f: json_bytes = f.read()
            json_cleaned = json_bytes.replace(b'</script>', b'<\\/script>')
            quiz_obj = json.loads(json_cleaned.decode('utf-8'))
            total_count = len(quiz_obj)
            
            # 1. 生成 mock_v34.html
            mock_path = os.path.join(subj['dir'], 'mock_v34.html')
            with open(mock_path, 'wb') as f:
                f.write(mock_top_tmpl.replace('REPLACE_TITLE', subj['title']).replace('REPLACE_SUBJECT_ID', subj['id']).encode('utf-8'))
                f.write(json_cleaned)
                f.write(b";")
                f.write(mock_bottom_tmpl.replace('REPLACE_CUTOFF', str(subj['cutoff'])).encode('utf-8'))
            
            # 2. 生成 自主練習頁面
            prac_path = os.path.join(subj['dir'], subj['html'])
            with open(prac_path, 'wb') as f:
                f.write(prac_top_tmpl.replace('REPLACE_TITLE', subj['title']).replace('REPLACE_TOTAL', str(total_count)).encode('utf-8'))
                f.write(json_cleaned)
                f.write(b";")
                f.write(prac_bottom_tmpl.replace('REPLACE_TITLE', subj['title']).replace('REPLACE_SUBJECT_ID', subj['id']).encode('utf-8'))
            print(f"V3.5.1 Smart Rotation Refreshed: {subj['dir']}")
        except Exception as e: print(f"Failed {subj['dir']}: {e}")

if __name__ == "__main__":
    clean_repair_all()
