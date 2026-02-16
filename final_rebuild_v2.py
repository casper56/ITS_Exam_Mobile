
import json
import os

html_path = 'www/ITS_Python/mock_exam.html'
json_path = 'www/ITS_Python/questions_ITS_python.json'

# 1. 讀取乾淨數據 (UTF-8)
with open(json_path, 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)
json_str = json.dumps(quiz_data, ensure_ascii=False, indent=2)

# 2. 定義 HTML 結構 (使用單純字串，避免 f-string 轉義錯誤)
html_top = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ITS Python Programming 模擬考試</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-solarized-light.min.css" rel="stylesheet" />
    <style>
        body { background-color: #f4f7f6; font-family: 'Segoe UI', "Microsoft JhengHei", sans-serif; }
        .exam-header { position: fixed; top: 0; left: 0; right: 0; z-index: 1050; background: #212529; color: white; padding: 10px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .timer-box { font-size: 1.5rem; font-weight: bold; color: #ffc107; }
        .main-content { margin-top: 80px; padding-bottom: 100px; max-width: calc(100% - 60px) !important; margin-left: auto !important; margin-right: auto !important; padding-left: 0 !important; padding-right: 0 !important; }
        .question-card { border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; margin-bottom: 25px; }
        .question-header { background-color: #fff; border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; }
        .question-body { padding: 15px 20px; font-size: 1.05rem; background-color: #fff; color: #000; }
        .option-item { list-style: none; margin-bottom: 8px; padding: 8px 12px; border: 1px solid #e9ecef; border-radius: 8px; cursor: pointer; transition: all 0.2s; background-color: #fff; font-size: 1rem; }
        .option-item:hover { background-color: #f8f9fa; border-color: #adb5bd; }
        .option-item.selected { background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }
        .sub-opt-container { padding: 6px 10px; border: 1px solid #dee2e6; border-radius: 6px; cursor: pointer; background: #fff; transition: all 0.2s; font-size: 0.85rem; }
        .sub-opt-container.selected { background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }
        .sub-question-label { font-weight: bold; margin-top: 15px; margin-bottom: 8px; color: #212529; border-left: 4px solid #198754; padding-left: 10px; font-size: 0.9rem; }
        #result-screen { display: none; text-align: center; padding: 50px 20px; }
        .score-circle { width: 150px; height: 150px; border-radius: 50%; border: 8px solid #0d6efd; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: bold; margin: 20px auto; color: #0d6efd; }
        code, pre code { color: #000 !important; background-color: transparent !important; }
        pre { background-color: transparent !important; border: none !important; }
        .side-nav-btn { position: fixed; top: 55%; transform: translateY(-50%); width: 25px; height: 65px; background: rgba(13, 110, 253, 0.7); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 2000; transition: all 0.3s ease; text-decoration: none; font-size: 1.1rem; border: none; font-family: serif; font-weight: bold; }
        .side-nav-btn:hover { background: #0d6efd; color: white; width: 25px; }
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
            body { background: white; width: 100%; margin: 0; padding: 0; }
            #exam-ui, #result-screen h2, .score-circle, .lead, #result-msg, .no-print { display: none !important; }
            #result-screen { display: block !important; padding: 0 !important; width: 100% !important; margin: 0 !important; }
            #review-area { display: block !important; border: none !important; width: 100% !important; padding: 0 !important; }
            .review-item { border: 1px solid #eee !important; width: 100% !important; page-break-inside: avoid; margin-bottom: 15px !important; padding: 10px !important; }
            pre, code { white-space: pre-wrap !important; word-break: break-all !important; border: none !important; font-size: 0.8rem !important; }
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
        <div><h5 class="m-0">ITS Python Programming 模擬考試</h5><small id="q-progress">1 / 50</small></div>
        <div class="timer-box" id="timer">50:00</div>
        <button class="btn btn-danger btn-sm" onclick="confirmSubmit()">交卷</button>
    </header>
    <div class="side-nav-btn side-nav-prev" id="side-btn-prev" onclick="changeQuestion(-1)">&#10094;</div>
    <div class="side-nav-btn side-nav-next" id="side-btn-next" onclick="changeQuestion(1)">&#10095;</div>
    <main class="container-fluid main-content" style="width: calc(100% - 60px); margin-top: 80px;"><div id="question-area"></div></main>
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
<script>
    const EXAM_LIMIT = 50, WRONG_KEY = 'its_python_wrong_ids';
    let currentIndex = 0, userAnswers = {}, timeLeft = 50 * 60, timerInterval;
    let examQuestions = [];

    function parseAnswerToIndex(val) {
        if (typeof val === 'number') return val - 1;
        if (typeof val === 'string') {
            const code = val.toUpperCase().charCodeAt(0);
            if (code >= 65 && code <= 90) return code - 65;
            return parseInt(val) - 1;
        }
        return -1;
    }
"""

html_bottom = """
    function startTimer() {
        timerInterval = setInterval(() => {
            timeLeft--;
            const m = Math.floor(timeLeft / 60), s = timeLeft % 60;
            document.getElementById('timer').innerText = `${m}:${s < 10 ? '0' : ''}${s}`;
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
        return lines.map(line => {
            let html = String(line);
            html = html.replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
                const src = item['image' + p1];
                return src ? `<img src="${src}" style="max-width:100%; margin: 10px 0;">` : match;
            });
            return html;
        }).join('<br/>');
    }

    function initExam() {
        if (typeof allQuestions === 'undefined' || allQuestions.length === 0) {
            console.error("allQuestions is empty!");
            return;
        }
        const shuffled = [...allQuestions].sort(() => 0.5 - Math.random());
        examQuestions = shuffled.slice(0, EXAM_LIMIT);
        renderQuestion(0); startTimer();
    }

    function renderQuestion(index, scrollTop = true) {
        currentIndex = index; const item = examQuestions[index]; const container = document.getElementById('question-area'); container.innerHTML = '';
        document.getElementById('q-progress').innerText = `${index + 1} / ${examQuestions.length}`;
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
            if (optStr.includes('|')) {
                const subOpts = optStr.split('|'); html += `<div class="sub-question-label">選項 ${optIdx + 1}</div><div class="d-flex flex-wrap gap-2 mb-3 ms-2">`;
                subOpts.forEach((sub, subIdx) => { 
                    const isSel = (savedAns && savedAns[optIdx] === subIdx); 
                    html += `<div class="sub-opt-container ${isSel ? 'selected' : ''}" onclick="selectSub(${optIdx}, ${subIdx})">(${subIdx+1}) ${sub}</div>`; 
                });
                html += `</div>`;
            } else {
                const isSel = Array.isArray(userAnswers[index]) ? userAnswers[index].includes(optIdx) : (userAnswers[index] === optIdx);
                html += `<div class="option-item ${isSel ? 'selected' : ''}" onclick="selectOption(${optIdx})">${optIdx + 1}. ${optStr}</div>`;
            }
        });
        html += '</div></div>'; card.innerHTML = html; container.appendChild(card);
        if (scrollTop) window.scrollTo(0, 0); if (typeof Prism !== 'undefined') Prism.highlightAll();
    }

    function selectOption(optIdx) {
        const item = examQuestions[currentIndex];
        if (item.type === 'multiple') {
            if (!Array.isArray(userAnswers[currentIndex])) userAnswers[currentIndex] = [];
            const idx = userAnswers[currentIndex].indexOf(optIdx);
            if (idx > -1) userAnswers[currentIndex].splice(idx, 1);
            else userAnswers[currentIndex].push(optIdx);
        } else {
            userAnswers[currentIndex] = optIdx;
        }
        renderQuestion(currentIndex, false);
    }
    function selectSub(qIdx, subIdx) { if (!userAnswers[currentIndex] || typeof userAnswers[currentIndex] !== 'object') userAnswers[currentIndex] = {}; userAnswers[currentIndex][qIdx] = subIdx; renderQuestion(currentIndex, false); }
    function changeQuestion(step) { if (currentIndex + step >= 0 && currentIndex + step < examQuestions.length) { renderQuestion(currentIndex + step); } else if (currentIndex + step >= examQuestions.length) { confirmSubmit(); } }
    function confirmSubmit() { if (confirm("確定要交卷嗎？")) { submitExam(); } }

    function submitExam() {
        clearInterval(timerInterval); document.getElementById('exam-ui').style.display = 'none'; document.getElementById('result-screen').style.display = 'block';
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
                const correctIndices = answers.map(a => parseAnswerToIndex(a));
                isCorrect = Array.isArray(userAns) && userAns.length === correctIndices.length && userAns.every(val => correctIndices.includes(val));
            } else { 
                isCorrect = userAns === parseAnswerToIndex(item.answer[0] || item.answer); 
            }

            if (isCorrect) { correctCount++; stats[cat].correct++; }
            else {
                let ansText = answers.join(', ');
                const optsRaw = item.quiz || item.options || [];
                const opts = Array.isArray(optsRaw) ? optsRaw : [optsRaw];
                let optionsHTML = '<div class="review-opts" style="margin-left:20px; margin-top:10px; font-size:0.9rem; color:#666;">';
                opts.forEach((o, i) => {
                    if (String(o).includes('|')) {
                        optionsHTML += `<div class="mb-1"><b>選項 ${i+1}:</b> ${o.split('|').map((s, si)=>`(${si+1})${s}`).join(' ')}</div>`;
                    } else {
                        optionsHTML += `<div class="mb-1">${i+1}. ${o}</div>`;
                    }
                });
                optionsHTML += '</div>';
                incorrectHTML += `<div class="review-item"><div class="review-id">題目 ${idx + 1} (編號: ${item.id})</div><div class="mb-2">${processContent(item.question, item)}</div>${optionsHTML}<div class="review-ans">正確答案：${ansText}</div><div class="review-exp"><b>解析：</b><br/>${processContent(item.explanation || '暫無解析。', item)}</div></div>`;
            }
        });
        
        const score = Math.round((correctCount / examQuestions.length) * 100);
        document.getElementById('final-score').innerText = score;
        document.getElementById('correct-count').innerText = correctCount;
        
        let catHTML = '<h5 class="text-center mb-3">各類答對率統計</h5><table class="table table-bordered"><thead><tr><th>分類</th><th>題數</th><th>答對率</th></tr></thead><tbody>';
        const sortedCats = Object.keys(stats).sort();
        for (let cat of sortedCats) {
            let total = stats[cat].total, correct = stats[cat].correct, p = Math.round((correct / total) * 100);
            catHTML += `<tr><td>${cat}</td><td>${total}</td><td>${p}%</td></tr>`;
        }
        catHTML += '</tbody></table>'; document.getElementById('category-stats').innerHTML = catHTML;

        let reportSummary = `
            <div class="review-item" style="border: 2px solid #0d6efd; background: #f0f7ff;">
                <h2 class="text-center" style="color: #0d6efd;">模擬考試成績報告</h2>
                <div class="d-flex justify-content-around mt-3">
                    <div class="text-center"><h4>總分: <span style="font-size: 2rem;">${score}</span></h4></div>
                    <div class="text-center"><h4>答對題數: ${correctCount} / ${examQuestions.length}</h4></div>
                </div>
                <div class="mt-3">${catHTML}</div>
            </div>
        `;
        document.getElementById('review-list').innerHTML = reportSummary + incorrectHTML;
    }

    initExam();
</script>
</body>
</html>"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_top)
    f.write("    const allQuestions = ")
    f.write(json_str)
    f.write(";")
    f.write(html_bottom)

print("ITS_Python/mock_exam.html 再次終極重建完成（排除 f-string 轉義問題）。")
