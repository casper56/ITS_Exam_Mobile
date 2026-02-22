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
        .main-content { margin-top: 80px; padding-bottom: 100px; max-width: calc(100% - 50px) !important; margin-left: auto !important; margin-right: auto !important; padding-left: 0 !important; padding-right: 0 !important; }
        .question-card { border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; margin-bottom: 25px; }
                .question-header { background-color: #fff; border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; }
                .question-body, .explanation, .review-q-text, .review-exp { 
                    padding: 15px 20px; 
                    font-size: 1.05rem; 
                    background-color: #fff; 
                    color: #000; 
                    word-wrap: break-word; 
                    word-break: normal; 
                    overflow-x: hidden;
                    white-space: pre-wrap; /* 核心修正：確保陣列結合後的 \n 能正常換行 */
                }
                
                /* 預設題目與程式碼樣式 */                code:not([class*="language-"]) { 
                    display: inline-block; 
                    margin: 5px 0; 
                    line-height: 1.4; 
                    font-size: 1.0rem; 
                    color: #222222; 
                    white-space: pre-wrap; /* 確保字串陣列的 \n 換行生效 */
                }
                
                code {
                    background-color: transparent !important; 
                    font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
                    white-space: pre-wrap; /* 全域保留換行 */
                }
        code[class*="language-"] { color: inherit; }

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

        /* 表格樣式：黑色實線邊框 */
        table, .q-table { max-width: 98% !important; border-collapse: collapse !important; margin: 15px 0; border: 1px solid #000 !important; font-size: 0.9rem; line-height: 1.2; box-sizing: border-box !important; }
        th, td, .q-table th, .q-table td { border: 1px solid #000 !important; padding: 10px 8px; vertical-align: top; word-break: break-all !important; color: #000; overflow-wrap: break-word !important; }
        .w-5 { width: 5% !important; }
        .w-10 { width: 10% !important; }
        .w-15 { width: 15% !important; }
        .w-20 { width: 20% !important; }
        .w-25 { width: 25% !important; }
        .w-30 { width: 30% !important; }
        .w-35 { width: 35% !important; }
        .w-40 { width: 40% !important; }
        .w-45 { width: 45% !important; }
        .w-50 { width: 50% !important; }
        .w-60 { width: 60% !important; }
        .w-70 { width: 70% !important; }
        .w-75 { width: 75% !important; }
        .w-80 { width: 80% !important; }
        
        /* 表格對齊輔助類別 */
        .t-left { margin-left: 0 !important; margin-right: auto !important; }
        .t-center { margin-left: auto !important; margin-right: auto !important; }
        .t-right { margin-left: auto !important; margin-right: 0 !important; }
        .side-nav-btn { position: fixed; top: 55%; transform: translateY(-50%); width: 25px; height: 65px; background: rgba(108, 117, 125, 0.7); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 2000; transition: all 0.3s ease, width 0.2s; text-decoration: none; font-size: 1.1rem; border: none; font-family: serif; font-weight: bold; }
        .side-nav-btn:hover { background: #0d6efd; color: white; width: 30px; }
        .side-nav-prev { left: 0; border-radius: 0 15px 15px 0; }
        .side-nav-next { right: 0; border-radius: 15px 0 0 15px; }
        #review-area { display: none; text-align: left; margin-top: 30px; border-top: 2px solid #dee2e6; padding: 20px; background: #fff; position: relative; z-index: 2000; }
        .review-item { margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 8px; background: #fff; }
        .review-id { font-weight: bold; color: #fff; background: #212529; margin: -15px -15px 15px -15px; padding: 8px 15px; border-radius: 8px 8px 0 0; }
        .review-ans { color: #198754; font-weight: bold; background: #e9f7ef; padding: 10px; border-radius: 6px; margin: 15px 0; border-left: 5px solid #198754; }
        .review-exp { font-size: 0.95rem; color: #212529; background: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
        @media print { 
            @page { size: auto; margin: 10mm; }
            * { overflow: visible !important; max-height: none !important; height: auto !important; }
            body { background: white; width: 100%; margin: 0; padding: 0; font-size: 1.0rem !important; }
            #exam-ui, #result-screen h2, .score-circle, .lead, #result-msg, .no-print { display: none !important; }
            #result-screen { display: block !important; padding: 0 !important; width: 100% !important; margin: 0 !important; }
            #result-screen h2.text-center { margin-top: 0 !important; padding-top: 0 !important; }
            #review-area { display: block !important; border: none !important; width: 100% !important; padding: 0 !important; margin: 0 !important; }
            .review-item { border: 1px solid #eee !important; width: 100% !important; page-break-inside: auto; margin-bottom: 5px !important; padding: 0 !important; }
            .review-id { margin: 0 !important; padding: 5px 10px !important; border-radius: 0 !important; }
            .review-q-text { display: flex !important; align-items: flex-start !important; padding: 10px 15px !important; font-size: 1.0rem !important; white-space: pre-wrap !important; word-break: break-all !important; width: calc(100% - 2px) !important; }
            .review-q-text b { margin-right: 8px !important; white-space: nowrap !important; }
            .review-q-text .q-content { flex: 1 !important; }
            .review-q-text .q-content pre, .review-q-text .q-content code { margin-top: 0 !important; padding-top: 0 !important; }
            .review-item { border: 1px solid #eee !important; width: 100% !important; page-break-inside: auto; margin-bottom: 5px !important; padding: 0 !important; }
            .review-q-text { padding: 10px 15px !important; font-size: 1.0rem !important; white-space: pre-wrap !important; word-break: break-all !important; width: calc(100% - 2px) !important; }
            .review-ans { color: #198754 !important; font-weight: bold !important; padding: 8px 10px !important; border-left: 5px solid #198754 !important; margin-left: 0 !important; white-space: pre-wrap !important; word-break: break-all !important; width: calc(100% - 2px) !important; }
            .review-exp { font-size: 1.0rem !important; padding: 15px !important; border-radius: 10px !important; border: 1px solid #eee !important; margin-left: 0 !important; white-space: pre-wrap !important; word-break: break-all !important; width: calc(100% - 2px) !important; }
            .review-exp pre, .review-exp code { margin: 0 !important; padding: 0 !important; white-space: pre-wrap !important; background: transparent !important; word-break: break-all !important; }
            pre, code { white-space: pre-wrap !important; word-break: break-all !important; border: none !important; font-size: 1.0rem !important; margin: 0 !important; padding: 0 !important; }
            .q-table { font-size: 0.7rem !important; margin: 10px 0 !important; page-break-inside: avoid; -webkit-print-color-adjust: exact; }
            .q-table td, .q-table th { border: 1px solid #000 !important; padding: 6px !important; }
            .category-title, .header-bg { -webkit-print-color-adjust: exact; background-color: #f0f0f0 !important; }
        }
        .zoom-controls { position: fixed; bottom: 30px; right: 20px; z-index: 1100; display: flex; flex-direction: column; gap: 10px; }
        .zoom-btn { width: 50px; height: 50px; border-radius: 50%; background: rgba(255, 255, 255, 0.9); color: #0d6efd; border: 2px solid #0d6efd; box-shadow: 0 4px 10px rgba(0,0,0,0.2); font-size: 1.5rem; font-weight: bold; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; padding: 0; user-select: none; -webkit-tap-highlight-color: transparent; }
    </style>
</head>
<body>
<div class="zoom-controls no-print">
    <div class="zoom-btn" onclick="adjustZoom(0.1)">➕</div>
    <div class="zoom-btn" onclick="adjustZoom(-0.1)">➖</div>
</div>
<div id="exam-ui">
    <header class="exam-header d-flex justify-content-between align-items-center">
        <div><h5 class="m-0">REPLACE_TITLE 模擬考試</h5><small id="q-progress">1 / 50</small></div>
        <div class="timer-box" id="timer">50:00</div>
        <button class="btn btn-danger btn-sm" onclick="confirmSubmit()">交卷</button>
    </header>
    <div class="side-nav-btn side-nav-prev" id="side-btn-prev" onclick="changeQuestion(-1)">&#10094;</div>
    <div class="side-nav-btn side-nav-next" id="side-btn-next" onclick="changeQuestion(1)">&#10095;</div>
    <main class="container-fluid main-content" style="width: calc(100% - 50px); margin-top: 80px;"><div id="question-area"></div></main>
</div>
<div id="result-screen" class="container-fluid">
    <h2 class="mb-4">考試結束</h2><div class="score-circle" id="final-score">0</div>
    <p class="lead">答對題數：<span id="correct-count">0</span> / 50</p>
    <div id="category-stats" class="mb-4 no-print"></div><div id="result-msg" class="mb-4"></div>
    <div class="mt-5 no-print">
        <a href="../index.html" class="btn btn-primary btn-lg me-2">回首頁</a>
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
    const EXAM_LIMIT = 50, WRONG_KEY = 'REPLACE_SUBJECT_ID_exam_wrong_ids';
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
        return lines.join('\n').replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
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
        const TARGET_OFF_COUNT = Math.floor(EXAM_LIMIT * 0.95); 
        
        const categories = {};
        const catNameMap = {}; 
        allQuestions.forEach(q => {
            let fullCat = q.category || '一般';
            let m = fullCat.match(/^(D\d+)/);
            let prefix = (m ? m[1] : fullCat);
            if (!catNameMap[prefix] || fullCat.length > catNameMap[prefix].length) catNameMap[prefix] = fullCat;
        });
        allQuestions.forEach(q => {
            let m = (q.category ? q.category.match(/^(D\d+)/) : null);
            let prefix = (m ? m[1] : q.category || '一般');
            let cat = catNameMap[prefix];
            if (!categories[cat]) categories[cat] = [];
            categories[cat].push(q);
        });

        let selected = [], usedIds = new Set();
        const catNames = Object.keys(categories).sort();
        const MIN_PER_CAT = Math.max(1, Math.floor(EXAM_LIMIT * 0.05));
        const MAX_PER_CAT = Math.floor(EXAM_LIMIT * 0.40);

        catNames.forEach(cat => {
            const catOff = categories[cat].filter(q => q.id <= CUTOFF).sort(() => 0.5 - Math.random());
            const catSupp = categories[cat].filter(q => q.id > CUTOFF).sort(() => 0.5 - Math.random());
            for (let i = 0; i < MIN_PER_CAT; i++) {
                if (catOff.length > 0) { const q = catOff.shift(); selected.push(q); usedIds.add(q.id); }
                else if (catSupp.length > 0) { const q = catSupp.shift(); selected.push(q); usedIds.add(q.id); }
            }
        });

        let offPool = allQuestions.filter(q => q.id <= CUTOFF && !usedIds.has(q.id)).sort(() => 0.5 - Math.random());
        for (let q of offPool) {
            if (selected.length >= TARGET_OFF_COUNT) break;
            let qCat = catNames.find(c => categories[c].some(cq => cq.id === q.id));
            if (!qCat) continue;
            let currentInCat = selected.filter(sq => categories[qCat].some(cq => cq.id === sq.id)).length;
            if (currentInCat < MAX_PER_CAT) { selected.push(q); usedIds.add(q.id); }
        }

        let finalPool = allQuestions.filter(q => !usedIds.has(q.id)).sort((a, b) => (b.id <= CUTOFF ? 1 : 0) - (a.id <= CUTOFF ? 1 : 0) || (0.5 - Math.random()));
        while (selected.length < EXAM_LIMIT && finalPool.length > 0) { const q = finalPool.shift(); selected.push(q); usedIds.add(q.id); }

        examQuestions = selected.sort(() => 0.5 - Math.random()).slice(0, EXAM_LIMIT);
        renderQuestion(0); startTimer();
    }

    function renderQuestion(index, scrollTop = true) {
        currentIndex = index; const item = examQuestions[index]; const container = document.getElementById('question-area'); 
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
            if (!stats[cat]) stats[cat] = { total: 0, correct: 0 }; stats[cat].total++;
            const userAns = userAnswers[idx]; let isCorrect = false;
            const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
            if (item.type === 'multioption' || (item.quiz || item.options || []).some(o => String(o).includes('|'))) {
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
                        optionsHTML += `<div class="mb-1" style="display:flex; align-items:flex-start; gap:8px;"><b>${displayLabel}:</b> ${subLabels}</div>`;
                    }
                    else {
                        const lbl = isNum ? (i + 1) + "." : `(${String.fromCharCode(65 + i)})`;
                        optionsHTML += `<div class="mb-1" style="display:flex; align-items:flex-start; gap:8px;"><span class="opt-num" ${numStyle}>${lbl} </span>${o}</div>`;
                    }
                });
                optionsHTML += '</div>';
                incorrectHTML += `<div class="review-item"><div class="review-id">題目 ${idx + 1} (編號: ${item.id})</div><div class="review-q-text"><div class="q-content">${processContent(item.question, item)}</div></div>${optionsHTML}<div class="review-ans">正確答案：${ansText}</div><div class="review-exp"><b>解析：</b><br/>${processContent(item.explanation || '暫無解析。', item)}</div></div>`;
            }
        });
        const score = Math.round((correctCount / examQuestions.length) * 100);
        document.getElementById('final-score').innerText = score; document.getElementById('correct-count').innerText = correctCount;
        let catHTML = '<h5 class="text-center mb-3">各類答對率統計</h5><table class="table table-bordered"><thead><tr><th>分類</th><th>題數</th><th>答對率</th></tr></thead><tbody>';
        const sortedCats = Object.keys(stats).sort();
        for (let cat of sortedCats) {
            let total = stats[cat].total, correct = stats[cat].correct, p = Math.round((correct / total) * 100);
            catHTML += `<tr><td>${cat}</td><td>${total}</td><td>${p}%</td></tr>`;
        }
        catHTML += '</tbody></table>'; 
        document.getElementById('category-stats').innerHTML = catHTML;
        let reportSummary = `<div class="review-item" style="border: 2px solid #0d6efd; background: #f0f7ff;"><h2 class="text-center" style="color: #0d6efd;">模擬考試成績報告</h2><div class="d-flex justify-content-around mt-3"><div class="text-center"><h4>總分: <span style="font-size: 2rem;">${score}</span></h4></div><div class="text-center"><h4>答對題數: ${correctCount} / ${examQuestions.length}</h4></div></div><div class="mt-3">${catHTML}</div></div>`;
        document.getElementById('review-list').innerHTML = reportSummary + incorrectHTML;
        setTimeout(() => { if(window.Prism) Prism.highlightAll(); }, 50);
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

    # --- 模板 B: 自主練習模板 (不計時) ---
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
        
        /* 預設題目與程式碼樣式 */
        code:not([class*="language-"]) { 
            display: inline-block; 
            margin: 5px 0; 
            line-height: 1.4; 
            font-size: 1.0rem; 
            color: #222222; 
        }
        code { background-color: transparent !important; font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace; }
        code[class*="language-"] { color: inherit; }

        .form-check-input { border-radius: 50% !important; width: 1.2rem; height: 1.2rem; background-image: none !important; cursor: pointer; }
        .form-check-input:checked { background-color: #0d6efd !important; border-color: #0d6efd !important; }
        .option-item { border: 1px solid #e9ecef; border-radius: 6px; padding: 10px; margin-bottom: 8px; cursor: pointer; transition: 0.2s; display: flex; align-items: flex-start; gap: 8px; }
        .option-item pre { margin: 0; display: inline-block; width: 100%; }
        .option-item.correct, .sub-opt-container.correct { background-color: #d1e7dd !important; border-color: #badbcc !important; color: #0f5132 !important; }
        .option-item.incorrect, .sub-opt-container.incorrect { background-color: #f8d7da !important; border-color: #f5c2c7 !important; color: #842029 !important; }
        .sub-opt-container.selected { background-color: #e7f1ff !important; border-color: #9ec5fe !important; }
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
        .question-body { padding: 20px; font-size: 1.0rem; word-wrap: break-word; word-break: normal; overflow-x: hidden; line-height: 1.8; }
        .answer-section { display: none; margin-top: 20px; padding: 20px; background: #fff; border: 2px solid #0d6efd; border-radius: 8px; }
        .explanation, .explanation pre, .explanation code, .review-exp-box pre, .review-exp-box code, pre[class*="language-"], code[class*="language-"] { white-space: pre-wrap !important; word-wrap: break-word !important; word-break: break-all !important; overflow-wrap: anywhere !important; }
        .review-item { margin-bottom: 10px; padding: 0; border: none; background: white; page-break-inside: auto; border-bottom: 1px solid #eee; padding-bottom: 10px; }
        .review-q-text { display: flex; align-items: flex-start; font-size: 1.0rem; line-height: 1.8; margin-bottom: 5px; color: #333; }
        .review-q-text b { margin-right: 8px; white-space: nowrap; }
        .review-q-text .q-content { flex: 1; }
        .review-q-text .q-content pre, .review-q-text .q-content code { margin-top: 0 !important; padding-top: 0 !important; }
        .q-img { max-width: 48%; height: auto; border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); margin: 5px 5px 5px 0; display: inline-block; vertical-align: top; }
        #review-area { display: none; text-align: left; padding: 20px; background: white; }
        .review-item { margin-bottom: 10px; padding: 0; border: none; background: white; page-break-inside: auto; border-bottom: 1px solid #eee; padding-bottom: 10px; }
        .review-q-text { font-size: 1.0rem; line-height: 1.8; margin-bottom: 5px; color: #333; }
        .review-ans { color: #198754; font-weight: bold; padding: 10px 15px; margin: 5px 0; border-left: 5px solid #198754; background: white; font-size: 1.0rem; }
        .review-exp-box { background: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eeeeee; line-height: 1.8; color: #333; font-size: 1.0rem; }
        @media print {
            @page { size: auto; margin: 8mm !important; }
            * { box-sizing: border-box !important; -webkit-print-color-adjust: exact; overflow: visible !important; }
            html, body { margin: 0 !important; padding: 0 !important; width: 100% !important; background: white !important; font-size: 1.0rem !important; line-height: 1.8 !important; }
            .main-wrapper, .mobile-toggle, .side-nav-btn, .no-print, .sidebar { display: none !important; }
            .content-area { margin-left: 0 !important; padding: 0 !important; margin-top: 0 !important; }
            #review-area { display: block !important; width: 100% !important; padding: 0 !important; margin: 0 !important; }
            .review-item { border-bottom: 1px solid #eee !important; width: 100% !important; page-break-inside: auto; margin: 0 0 10px 0 !important; padding: 0 !important; border-top: none !important; border-left: none !important; border-right: none !important; }
            .review-q-text { padding: 10px 2px !important; font-size: 1.0rem !important; white-space: pre-wrap !important; word-break: break-all !important; width: calc(100% - 2px) !important; }
            .review-opt-line { padding-left: 2px !important; margin-bottom: 2px !important; white-space: pre-wrap !important; word-break: break-all !important; width: calc(100% - 2px) !important; }
            .review-ans { color: #198754 !important; font-weight: bold !important; padding: 8px 5px !important; border-left: 5px solid #198754 !important; margin: 5px 0 !important; white-space: pre-wrap !important; word-break: break-all !important; width: calc(100% - 2px) !important; font-size: 1.0rem !important; }
            .review-exp-box { font-size: 1.0rem !important; padding: 10px !important; border-radius: 10px !important; border: 1px solid #eee !important; margin: 0 !important; white-space: pre-wrap !important; word-break: break-all !important; background: #fafafa !important; width: calc(100% - 2px) !important; }
            pre, code { white-space: pre-wrap !important; word-break: break-all !important; border: none !important; font-size: 1.0rem !important; margin: 0 !important; padding: 0 !important; }
            .q-img { max-width: 300px !important; margin: 10px 0 !important; }
            h1 { font-size: 1.5rem !important; margin-bottom: 20px !important; }
            .q-table, table { font-size: 0.7rem !important; max-width: 98% !important; margin: 10px 0 !important; page-break-inside: avoid; -webkit-print-color-adjust: exact; border-collapse: collapse !important; box-sizing: border-box !important; }
            .q-table td, .q-table th, td, th { border: 1px solid #000 !important; padding: 6px !important; word-break: break-all !important; overflow-wrap: break-word !important; }
            .category-title, .header-bg { -webkit-print-color-adjust: exact; background-color: #f0f0f0 !important; }
        }
        .side-nav-btn { position: fixed; top: 55%; width: 25px; height: 65px; background: rgba(108, 117, 125, 0.7); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 2000; transition: left 0.3s ease, background 0.3s, width 0.2s; text-decoration: none; font-size: 1.1rem; border: none; box-shadow: none; outline: none !important; user-select: none; -webkit-tap-highlight-color: transparent; font-family: serif; font-weight: bold; transform: translateY(-50%); }
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

        /* 表格樣式：黑色實線邊框 */
        table, .q-table { max-width: 98% !important; border-collapse: collapse !important; margin: 15px 0; border: 1px solid #000 !important; font-size: 0.9rem; line-height: 1.2; box-sizing: border-box !important; }
        th, td, .q-table th, .q-table td { border: 1px solid #000 !important; padding: 10px 8px; vertical-align: top; word-break: break-all !important; color: #000; overflow-wrap: break-word !important; }
        .w-5 { width: 5% !important; }
        .w-10 { width: 10% !important; }
        .w-15 { width: 15% !important; }
        .w-20 { width: 20% !important; }
        .w-25 { width: 25% !important; }
        .w-30 { width: 30% !important; }
        .w-35 { width: 35% !important; }
        .w-40 { width: 40% !important; }
        .w-45 { width: 45% !important; }
        .w-50 { width: 50% !important; }
        .w-60 { width: 60% !important; }
        .w-70 { width: 70% !important; }
        .w-75 { width: 75% !important; }
        .w-80 { width: 80% !important; }
        
        /* 表格對齊輔助類別 */
        .t-left { margin-left: 0 !important; margin-right: auto !important; }
        .t-center { margin-left: auto !important; margin-right: auto !important; }
        .t-right { margin-left: auto !important; margin-right: 0 !important; }
    </style>
</head>
<body>
<div class="main-wrapper">
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="d-flex align-items-center justify-content-between mb-2">
                <div class="d-flex align-items-center"><a href="../index.html" class="text-decoration-none text-white me-2">🏠</a><h5 class="m-0" style="font-size: 1.1rem;">題庫列表</h5></div>
                <div class="d-flex gap-1">
                    <button type="button" onclick="prepareAndPrint()" class="btn btn-outline-light btn-sm py-1 px-2" style="font-size: 0.8rem;">完整解析</button>
                    <button type="button" onclick="prepareAndPrint(true)" class="btn btn-warning btn-sm py-1 px-2" style="font-size: 0.8rem; font-weight: bold;">錯題訂正</button>
                </div>
            </div>
            <div id="progress-stats">✅0 ❌0 🟠0 / REPLACE_TOTAL</div>
        </div>
        <div class="sidebar-content">
            <div class="d-flex justify-content-between small mb-3 text-muted">
                <span><span style="display:inline-block;width:10px;height:10px;background:#fff;border:1px solid #ccc"></span> 未答</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#d1e7dd"></span> 正確</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#f8d7da"></span> 錯誤</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#fd7e14"></span> 已訂正</span>
            </div>
            <div class="progress-grid" id="progress-grid"></div>
        </div>
        <div class="sidebar-footer"><button class="btn btn-outline-danger btn-sm w-100" onclick="resetProgress()">重置 練習進度</button></div>
    </nav>
    <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>
    <div class="side-nav-btn side-nav-prev" id="side-btn-prev" onclick="prevQuestion()">&#10094;</div>
    <div class="side-nav-btn side-nav-next" id="side-btn-next" onclick="nextQuestion()">&#10095;</div>
    <main class="content-area"><div class="container-fluid" style="width: calc(100% - 50px); padding: 0; margin-left: auto; margin-right: auto;"><div id="question-container"></div></div></main>
</div>
<div id="review-area"></div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-csharp.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
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
        return lines.join('\n').replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
            const num = parseInt(p1, 10);
            const src = item['image' + num] || item['image' + p1] || item['image'];
            return src ? `<img src="${src}" class="q-img">` : match;
        });
    }
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
            
            let optHtml = opts.map((o, i) => {
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
                    return `<div class="review-opt-line"><b>${displayLabel}:</b> ${subLabels}</div>`;
                } else {
                    const lbl = isNum ? (i + 1) + "." : `(${String.fromCharCode(65 + i)})`;
                    return `<div class="review-opt-line"><span class="opt-num" ${numStyle}>${lbl} </span>${o}</div>`;
                }
            }).join('');
            
            // 處理題目清理：若是陣列，僅清理第一項 (優化：支援 HTML 標籤開頭)
            let cleanQ = item.question;
            const numRegex = /^((?:<[^>]+>)*)\d+\.\s*/;
            if (Array.isArray(cleanQ)) {
                cleanQ = [...cleanQ];
                if (cleanQ.length > 0) cleanQ[0] = cleanQ[0].replace(numRegex, '$1');
            } else {
                cleanQ = String(cleanQ).replace(numRegex, '$1');
            }
            
            let imgHtml = item.image ? `<div class="text-center my-2"><img src="${item.image}" class="q-img"></div>` : '';
            const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
            const ansText = answers.map(a => {
                if (String(a).toUpperCase() === 'Y' || String(a).toUpperCase() === 'N') return a;
                const idx = parseAnswerToIndex(a);
                if (idx < 0) return a;
                return isNum ? (idx + 1) : String.fromCharCode(65 + idx);
            }).join(', ');

            div.innerHTML = `<div class="review-q-text"><b>${idx+1}.</b> <div class="q-content">${processContent(cleanQ, item)}</div></div>${imgHtml}<div class="review-opts" style="margin-left:0">${optHtml}</div><div class="review-ans">正確答案：${ansText}</div><div class="review-exp">${processContent(item.explanation || '暫無解析。', item)}</div>`;
            area.appendChild(div);
        });
        if(window.Prism) Prism.highlightAll();
        setTimeout(() => { window.print(); }, 100);
    }
    function renderQuestion(index) {
        window.scrollTo(0, 0); currentIndex = index; const item = quizData[index];
        const container = document.getElementById('question-area') || document.getElementById('question-container');
        const opts = item.quiz || item.options || [];
        const pBtn = document.getElementById('side-btn-prev'); if (pBtn) pBtn.style.display = (index === 0) ? 'none' : 'flex';
        let typeLabel = opts.some(o => String(o).includes('|')) ? "題組" : (item.type === 'multiple' ? "複選" : "單選");
        container.innerHTML = `
            <div class="card question-card">
                <div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizData.length}</span><span class="badge bg-info type-badge">${typeLabel}</span></div><div class="category-tag">${item.category || '一般'}</div></div>
                <div class="question-body"><div class="mb-3">${processContent(item.question, item)}</div>${item.image ? `<img src="${item.image}" class="q-img">` : ''}<div class="options-area mt-1"></div><div class="text-center mt-4 pt-3 border-top"><button class="btn btn-outline-primary px-4" id="toggle-exp-btn" onclick="toggleExplanation()">👁️ 顯示答案 / 解析</button></div><div class="answer-section" id="ans-section"><h6 class="fw-bold mb-3">正確答案: <span class="text-blue">${Array.isArray(item.answer) ? item.answer.join(', ') : item.answer}</span></h6><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div></div>
            </div>`;
        const optionsArea = container.querySelector('.options-area');
        opts.forEach((opt, oIdx) => {
            let labelText = `(${String.fromCharCode(65 + oIdx)}) `;
            if (item.labelType === 'num') labelText = `${oIdx + 1}. `;
            const numStyle = (item.labelType === 'none' || item.hideLabel) ? 'style="display:none"' : '';

            if (String(opt).includes('|')) {
                const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                const customLabelField = "question" + alphabet[oIdx];
                let customLabel = "";
                if (item[customLabelField]) {
                    customLabel = Array.isArray(item[customLabelField]) ? item[customLabelField].join('<br>') : item[customLabelField];
                }
                const displayLabel = customLabel || `選項 ${oIdx + 1}`;

                let sHtml = `<div class="mb-2"><div class="fw-bold mb-1 small">${displayLabel}</div><div class="d-flex flex-wrap gap-2">`;
                opt.split('|').forEach((s, subIdx) => { 
                    let subLabel = `(${String.fromCharCode(65 + subIdx)}) `;
                    if (item.labelType === 'num') subLabel = `(${subIdx+1}) `;
                    sHtml += `<div class="sub-opt-container p-2 border rounded bg-light" onclick="checkSubAnswer(this, ${index}, ${oIdx}, ${subIdx}, event)" style="cursor:pointer; font-size:0.9rem"><input class="form-check-input" type="radio" name="q${index}_opt${oIdx}" id="o${oIdx}_s${subIdx}"><span class="opt-num" ${numStyle}>${subLabel}</span> ${s}</div>`; 
                });
                optionsArea.innerHTML += sHtml + '</div></div>';
            } else { optionsArea.innerHTML += `<div class="option-item" onclick="checkAnswer(this, ${index}, ${oIdx}, event)"><input class="form-check-input" type="${item.type==='multiple'?'checkbox':'radio'}" name="q${index}" id="o${oIdx}"><span class="opt-num" ${numStyle}>${labelText}</span>${opt}</div>`; }
        });
        const saved = userAnswers[index], completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);
        let answers = item.answer; if (!Array.isArray(answers)) answers = [answers];
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
            if (Array.isArray(saved)) {
                saved.forEach(idx => { const inp = document.getElementById(`o${idx}`); if (inp) { inp.checked = true; if(completed) inp.closest('.option-item').classList.add(cIdxs.includes(idx) ? 'correct' : 'incorrect'); } });
                if(completed) cIdxs.forEach(ci => { const inp = document.getElementById(`o${ci}`); if (inp) inp.closest('.option-item').classList.add('correct'); });
            } else {
                const inp = document.getElementById(`o${saved}`); if (inp) { inp.checked = true; if(completed) inp.closest('.option-item').classList.add(cIdxs.includes(saved) ? 'correct' : 'incorrect'); }
                if(completed && !cIdxs.includes(saved)) { const ci = document.getElementById(`o${cIdxs[0]}`); if(ci) ci.closest('.option-item').classList.add('correct'); }
            }
        }
        if (completed) { toggleExplanation(true); document.querySelectorAll(`input[name^="q${index}"]`).forEach(i => i.disabled = true); }
        updateUI(); 
        setTimeout(() => { if(window.Prism) Prism.highlightAll(); }, 50);
        saveState();
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
    loadState(); renderQuestion(currentIndex);
</script>
</body>
</html>"""

    for subj in config['subjects']:
        try:
            json_file = os.path.join(subj['dir'], subj['json'])
            if not os.path.exists(json_file): continue
            
            with open(json_file, 'rb') as f:
                json_bytes = f.read()
            
            json_cleaned = json_bytes.replace(b'</script>', b'<\\/script>')
            quiz_obj = json.loads(json_cleaned.decode('utf-8'))
            total_count = len(quiz_obj)
            
            # --- 1. 生成 mock_v34.html ---
            mock_path = os.path.join(subj['dir'], 'mock_v34.html')
            with open(mock_path, 'wb') as f:
                f.write(mock_top_tmpl.replace('REPLACE_TITLE', subj['title']).replace('REPLACE_SUBJECT_ID', subj['id']).encode('utf-8'))
                f.write(json_cleaned)
                f.write(b";")
                f.write(mock_bottom_tmpl.replace('REPLACE_CUTOFF', str(subj['cutoff'])).encode('utf-8'))
            
            # --- 2. 生成 自主練習頁面 (學科名.html) ---
            prac_path = os.path.join(subj['dir'], subj['html'])
            with open(prac_path, 'wb') as f:
                f.write(prac_top_tmpl.replace('REPLACE_TITLE', subj['title']).replace('REPLACE_TOTAL', str(total_count)).encode('utf-8'))
                f.write(json_cleaned)
                f.write(b";")
                f.write(prac_bottom_tmpl.replace('REPLACE_TITLE', subj['title']).replace('REPLACE_SUBJECT_ID', subj['id']).encode('utf-8'))
            
            print(f"V3.5.0 Standard Refreshed: {subj['dir']}")
        except Exception as e:
            print(f"Failed {subj['dir']}: {e}")

if __name__ == "__main__":
    clean_repair_all()
