import json
import os

def generate_fresh_mock():
    # 這是標準的 V3.1 模擬考模板 (不包含 JSON 資料的部分)
    template_start = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} 模擬考試</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-solarized-light.min.css" rel="stylesheet" />
    <style>
        body { background-color: #f8f9fa; font-family: "Microsoft JhengHei", sans-serif; overflow-y: auto; }
        .exam-header { position: fixed; top: 0; left: 0; right: 0; z-index: 1050; background: #212529; color: white; padding: 10px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .timer-box { font-size: 1.5rem; font-weight: bold; color: #ffc107; }
        .main-content { margin-top: 80px; padding-bottom: 100px; }
        .question-card { border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; margin-bottom: 25px; overflow: visible !important; }
        .question-header { background-color: #fff; border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; }
        .question-body { padding: 15px 20px; font-size: 0.85rem; overflow: visible !important; background-color: #fff; color: #212529; }
        .option-item { list-style: none; margin-bottom: 8px; padding: 8px 12px; border: 1px solid #e9ecef; border-radius: 8px; cursor: pointer; transition: all 0.2s; background-color: #fff; font-size: 0.9rem; }
        .option-item:hover { background-color: #f8f9fa; border-color: #adb5bd; }
        .option-item.selected { background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }
        .sub-opt-container { padding: 6px 10px; border: 1px solid #dee2e6; border-radius: 6px; cursor: pointer; background: #fff; transition: all 0.2s; font-size: 0.85rem; }
        .sub-opt-container.selected { background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }
        .sub-question-label { font-weight: bold; margin-top: 15px; margin-bottom: 8px; color: #212529; border-left: 4px solid #198754; padding-left: 10px; font-size: 0.9rem; }
        #result-screen { display: none; text-align: center; padding: 50px 20px; }
        .score-circle { width: 150px; height: 150px; border-radius: 50%; border: 8px solid #0d6efd; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: bold; margin: 20px auto; color: #0d6efd; }
        code { color: inherit !important; background-color: transparent !important; }
        pre { background-color: transparent !important; border: none !important; }
        .preview-active .no-print { display: none !important; }
        .side-nav-btn { position: fixed; top: 55%; transform: translateY(-50%); width: 40px; height: 100px; background: rgba(13, 110, 253, 0.85); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 1060; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); text-decoration: none; font-size: 1.5rem; border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.2); outline: none !important; user-select: none; -webkit-tap-highlight-color: transparent; font-family: serif; font-weight: bold; }
        .side-nav-btn:hover { background: #0d6efd; width: 50px; color: white; }
        .side-nav-prev { left: 0; border-radius: 0 50px 50px 0; padding-right: 8px; }
        .side-nav-next { right: 0; border-radius: 50px 0 0 50px; padding-left: 8px; }
        .side-nav-btn.disabled { display: none; }
        @media (max-width: 768px) { .side-nav-btn { width: 35px; height: 80px; font-size: 1.2rem; background: rgba(33, 37, 41, 0.7); } .side-nav-btn:hover { width: 40px; } }
        #review-area { display: none; text-align: left; margin-top: 30px; border-top: 2px solid #dee2e6; padding: 20px; background: #fff; position: relative; z-index: 2000; }
        .review-item { margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 8px; background: #fff; }
        .review-id { font-weight: bold; color: #fff; background: #212529; margin: -15px -15px 15px -15px; padding: 8px 15px; border-radius: 8px 8px 0 0; }
        .review-ans { color: #198754; font-weight: bold; background: #e9f7ef; padding: 10px; border-radius: 6px; margin: 15px 0; border-left: 5px solid #198754; }
        .review-exp { font-size: 0.95rem; color: #212529; background: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
        @media print { @page { size: auto; margin: 10mm; } * { overflow: visible !important; max-height: none !important; height: auto !important; } html, body { background: white; width: 100%; margin: 0; padding: 0; } #exam-ui, #result-screen h2, .score-circle, .lead, #result-msg, .no-print { display: none !important; } #result-screen { display: block !important; padding: 0 !important; width: 100% !important; margin: 0 !important; } #review-area { display: block !important; border: none !important; width: 100% !important; padding: 0 !important; } .review-item { border: 1px solid #eee !important; width: 100% !important; page-break-inside: avoid; margin-bottom: 15px !important; padding: 10px !important; } pre, code { white-space: pre-wrap !important; word-break: break-all !important; border: none !important; font-size: 0.8rem !important; } }
        .zoom-controls { position: fixed; bottom: 30px; right: 20px; z-index: 1100; display: flex; flex-direction: column; gap: 10px; }
        .zoom-btn { width: 50px; height: 50px; border-radius: 50%; background: rgba(255, 255, 255, 0.9); color: #0d6efd; border: 2px solid #0d6efd; box-shadow: 0 4px 10px rgba(0,0,0,0.2); font-size: 1.5rem; font-weight: bold; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; padding: 0; user-select: none; -webkit-tap-highlight-color: transparent; }
        .zoom-btn:active { transform: scale(0.9); background: #0d6efd; color: #fff; }
    </style>
</head>
<body>
<div class="zoom-controls no-print">
    <div class="zoom-btn" onclick="adjustZoom(0.1)" title="放大">➕</div>
    <div class="zoom-btn" onclick="adjustZoom(-0.1)" title="縮小">➖</div>
</div>
<div id="exam-ui">
    <header class="exam-header d-flex justify-content-between align-items-center">
        <div><h5 class="m-0">{{TITLE}} 模擬考試</h5><small id="q-progress">1 / {{COUNT}}</small></div>
        <div class="timer-box" id="timer">50:00</div>
        <button class="btn btn-danger btn-sm" onclick="confirmSubmit()">交卷</button>
    </header>
    <div class="side-nav-btn side-nav-prev" id="side-btn-prev" onclick="changeQuestion(-1)" title="上一題">&#10094;</div>
    <div class="side-nav-btn side-nav-next" id="side-btn-next" onclick="changeQuestion(1)" title="下一題">&#10095;</div>
    <main class="container-fluid main-content" style="max-width: 100%; margin-top: 80px; padding-left: 15px; padding-right: 15px;"><div id="question-area"></div></main>
</div>
<div id="result-screen" class="container-fluid" style="max-width: 100%; margin: 0; padding-left: 15px; padding-right: 15px;">
    <h2 class="mb-4">考試結束</h2><div class="score-circle" id="final-score">0</div>
    <p class="lead">答對題數：<span id="correct-count">0</span> / {{COUNT}}</p>
    <div id="category-stats" class="mb-4"></div><div id="result-msg" class="mb-4"></div>
    <div class="mt-5 no-print">
        <a href="../index.html" class="btn btn-primary btn-lg me-2">回首頁</a>
        <button class="btn btn-outline-secondary btn-lg me-2" onclick="location.reload()">重新挑戰</button>
        <button class="btn btn-outline-danger btn-lg me-2" onclick="clearWrongHistory()">🗑️ 清除錯題紀錄</button>
        <button id="btn-export-pdf" class="btn btn-success btn-lg" onclick="exportIncorrectPDF()" style="display:none;">💾 匯出錯誤題目 PDF</button>
    </div>
    <div id="review-area">
        <div class="d-flex justify-content-between align-items-center mb-4 no-print"><h3 class="m-0">錯誤題目回顧報告</h3><button class="btn btn-success" onclick="window.print()">🖨️ 列印 / 另存 PDF</button></div>
        <div id="review-list"></div>
    </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-csharp.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<script>
    let currentZoom = 1.0;
    let savedZoomBeforePreview = 1.0;
    function applyZoom() { document.body.style.zoom = currentZoom; if (!document.body.style.zoom) { document.body.style.transform = `scale(${currentZoom})`; document.body.style.transformOrigin = "top center"; document.body.style.width = (100 / currentZoom) + "%"; } }
    function adjustZoom(delta) { currentZoom = Math.max(0.5, Math.min(3.0, currentZoom + delta)); applyZoom(); }
    window.addEventListener('DOMContentLoaded', () => { if (window.innerWidth < 600) { currentZoom = 0.85; applyZoom(); } });

    const allQuestions = """

    template_end = r""";
    let examQuestions = [];
    let userAnswers = {}; 
    let timeLeft = 50 * 60; 
    let timerInterval;
    const SUBJECT_ID = '{{SUB_ID}}';
    const WRONG_KEY = SUBJECT_ID + '_wrong_ids';
    const PERF_KEY = SUBJECT_ID + '_performance';

    function clearWrongHistory() { if (confirm('確定要清除所有累積的錯題紀錄與表現數據嗎？')) { localStorage.removeItem(WRONG_KEY); localStorage.removeItem(PERF_KEY); alert('紀錄已清除'); location.reload(); } }
    
    function startExam() {
        const categories = [...new Set(allQuestions.map(q => q.category || '未分類'))];
        const wrongIds = new Set(JSON.parse(localStorage.getItem(WRONG_KEY) || '[]'));
        const performance = JSON.parse(localStorage.getItem(PERF_KEY) || '{}');
        const groups = {};
        allQuestions.forEach(q => { const cat = q.category || '未分類'; if (!groups[cat]) groups[cat] = []; groups[cat].push(q); });
        
        let selected = [];
        let remainingPool = [];
        const prioritySort = (a, b) => { const aW = wrongIds.has(a.id) ? 1 : 0; const bW = wrongIds.has(b.id) ? 1 : 0; return (bW - aW) || (0.5 - Math.random()); };

        categories.forEach(cat => {
            if (groups[cat]) {
                const sorted = [...groups[cat]].sort(prioritySort);
                let minNeeded = 4;
                if (performance[cat] && performance[cat].total > 0) {
                    const rate = (performance[cat].correct / performance[cat].total) * 100;
                    if (rate < 60) minNeeded = 6;
                }
                const minPick = sorted.slice(0, Math.min(minNeeded, sorted.length));
                selected = selected.concat(minPick);
                remainingPool = remainingPool.concat(sorted.slice(minPick.length));
            }
        });

        remainingPool.sort(prioritySort);
        const limit = {{COUNT}};
        while (selected.length < limit && remainingPool.length > 0) { selected.push(remainingPool.shift()); }
        examQuestions = selected.slice(0, limit).sort(() => 0.5 - Math.random());
        renderQuestion(0);
        startTimer();
    }

    function startTimer() { timerInterval = setInterval(() => { timeLeft--; let mins = Math.floor(timeLeft / 60); let secs = timeLeft % 60; document.getElementById('timer').innerText = `${mins}:${secs.toString().padStart(2, '0')}`; if (timeLeft <= 0) { alert("時間到！系統自動交卷。"); submitExam(); } }, 1000); }

    function renderQuestion(index, scrollTop = true) {
        currentIndex = index; const item = examQuestions[index]; const container = document.getElementById('question-area'); container.innerHTML = '';
        document.getElementById('q-progress').innerText = `題目 ${index + 1} / {{COUNT}}`;
        const sidePrev = document.getElementById('side-btn-prev'), sideNext = document.getElementById('side-btn-next');
        if (sidePrev) sidePrev.style.display = index === 0 ? 'none' : 'flex';
        if (sideNext) { sideNext.style.display = 'flex'; sideNext.title = index === (examQuestions.length-1) ? '交卷' : '下一題'; }
        const card = document.createElement('div'); card.className = 'card question-card';
        let qText = item.question.replace(/●/g, '<br/>●').replace(/^\d+\.\s*/, '');
        let html = `<div class="question-header">Question ${index + 1} / {{COUNT}}</div><div class="question-body"><div class="mb-4">${qText}</div>`;
        if (item.image) html += `<div class="text-center mb-4"><img src="${item.image}" style="max-width:100%; border:1px solid #ddd; border-radius:4px;"></div>`;
        const options = item.quiz || item.options || [];
        const savedAns = userAnswers[index];
        html += '<div class="mt-3">';
        options.forEach((opt, optIdx) => {
            const optStr = String(opt);
            if (optStr.includes('|')) {
                const subOpts = optStr.split('|');
                html += `<div class="sub-question-label">選項 ${optIdx + 1}</div><div class="d-flex flex-wrap gap-2 mb-3 ms-2">`;
                subOpts.forEach((sub, subIdx) => { const isSel = (savedAns && savedAns[optIdx] === subIdx); html += `<div class="sub-opt-container ${isSel ? 'selected' : ''}" onclick="selectSub(${optIdx}, ${subIdx})">(${subIdx+1}) ${sub}</div>`; });
                html += `</div>`;
            } else {
                const isSel = Array.isArray(savedAns) ? savedAns.includes(optIdx) : savedAns === optIdx;
                html += `<div class="option-item ${isSel ? 'selected' : ''}" onclick="selectOption(${optIdx})">${optIdx + 1}. ${optStr}</div>`;
            }
        });
        html += '</div></div>'; card.innerHTML = html; container.appendChild(card); Prism.highlightAll(); if (scrollTop) window.scrollTo(0, 0);
    }

    function selectOption(optIdx) {
        const item = examQuestions[currentIndex];
        if (item.type === 'multiple') { if (!Array.isArray(userAnswers[currentIndex])) userAnswers[currentIndex] = []; const idx = userAnswers[currentIndex].indexOf(optIdx); if (idx > -1) userAnswers[currentIndex].splice(idx, 1); else userAnswers[currentIndex].push(optIdx); }
        else { userAnswers[currentIndex] = optIdx; }
        renderQuestion(currentIndex, false);
    }

    function selectSub(quizIdx, subIdx) { if (typeof userAnswers[currentIndex] !== 'object' || userAnswers[currentIndex] === null) userAnswers[currentIndex] = {}; userAnswers[currentIndex][quizIdx] = subIdx; renderQuestion(currentIndex, false); }
    function changeQuestion(dir) { let next = currentIndex + dir; if (next >= 0 && next < examQuestions.length) renderQuestion(next); else if (next === examQuestions.length) confirmSubmit(); }
    function confirmSubmit() { const answeredCount = Object.keys(userAnswers).length; if (answeredCount < examQuestions.length) { if (!confirm(`您還有 ${examQuestions.length - answeredCount} 題未作答，確定要交卷嗎？`)) return; } else { if (!confirm('確定要交卷嗎？')) return; } submitExam(); }

    function submitExam() {
        clearInterval(timerInterval); let correctCount = 0, incorrectHTML = ''; const stats = {};
        let wrongIds = new Set(JSON.parse(localStorage.getItem(WRONG_KEY) || '[]'));
        examQuestions.forEach((item, idx) => {
            const cat = item.category || '未分類'; if (!stats[cat]) stats[cat] = { total: 0, correct: 0 }; stats[cat].total++;
            const userAns = userAnswers[idx]; let isCorrect = false;
            if (item.type === 'multioption' || (item.quiz || item.options || []).some(o => String(o).includes('|'))) {
                const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
                isCorrect = answers.every((a, i) => userAns && (parseInt(a) - 1) === userAns[i]);
            } else if (item.type === 'multiple') {
                const answers = item.answer.map(a => parseInt(a) - 1);
                isCorrect = Array.isArray(userAns) && userAns.length === answers.length && userAns.every(val => answers.includes(val));
            } else { isCorrect = userAns === (parseInt(item.answer) - 1); }
            if (isCorrect) { correctCount++; stats[cat].correct++; wrongIds.delete(item.id); }
            else {
                wrongIds.add(item.id); let qText = item.question.replace(/●/g, '<br/>●');
                let ansText = Array.isArray(item.answer) ? item.answer.join(', ') : item.answer;
                let optionsHTML = '<hr class="my-2"><div class="fw-bold mb-1">選擇：</div><ul class="list-group list-group-flush mb-3" style="font-size: 0.85rem;">';
                (item.quiz || item.options || []).forEach((opt, oIdx) => { optionsHTML += `<li class="list-group-item p-1" style="background: transparent; border: none;">${oIdx + 1}. ${opt}</li>`; });
                optionsHTML += '</ul>';
                let expText = item.explanation || '暫無解析。'; if (Array.isArray(expText)) expText = expText.join('<br/>'); expText = expText.replace(/●/g, '<br/>●');
                incorrectHTML += `<div class="review-item"><div class="review-id">題目 ${idx + 1} (原始編號: ${item.id})</div><div class="mb-2">${qText}</div>${optionsHTML}<div class="review-ans">正確答案：${ansText}</div><div class="review-exp"><b>解析：</b><br/>${expText}</div></div>`;
            }
        });
        localStorage.setItem(WRONG_KEY, JSON.stringify([...wrongIds])); localStorage.setItem(PERF_KEY, JSON.stringify(stats));
        let statsHTML = '<div class="row justify-content-center"><div class="col-md-10"><div class="card shadow-sm border-0"><div class="card-header bg-dark text-white fw-bold">各類題數佔比與答對率</div><div class="table-responsive"><table class="table table-hover mb-0 text-start align-middle"><thead><tr><th>題目分類</th><th class="text-center">題數</th><th class="text-center">佔比</th><th class="text-center">答對率</th></tr></thead><tbody>';
        Object.keys(stats).sort().forEach(cat => {
            const data = stats[cat], percent = ((data.total / examQuestions.length) * 100).toFixed(1), accuracy = ((data.correct / data.total) * 100).toFixed(0);
            const badgeClass = accuracy >= 70 ? 'bg-success' : (accuracy >= 40 ? 'bg-warning text-dark' : 'bg-danger');
            statsHTML += `<tr><td>${cat}</td><td class="text-center">${data.total}</td><td class="text-center">${percent}%</td><td class="text-center"><div class="progress" style="height:20px;"><div class="progress-bar ${badgeClass}" style="width:${accuracy}%">${accuracy}%</div></div></td></tr>`;
        });
        statsHTML += '</tbody></table></div></div></div></div>';
        document.getElementById('category-stats').innerHTML = statsHTML; document.getElementById('exam-ui').style.display = 'none'; document.getElementById('result-screen').style.display = 'block';
        document.getElementById('correct-count').innerText = correctCount; const score = Math.round((correctCount / examQuestions.length) * 100); document.getElementById('final-score').innerText = score;
        if (correctCount < examQuestions.length) { document.getElementById('btn-export-pdf').style.display = 'inline-block'; document.getElementById('review-list').innerHTML = incorrectHTML; }
        if (score >= 70) { document.getElementById('result-msg').innerHTML = '<h4 class="text-success fw-bold">恭喜通過！🎉</h4>'; launchFireworks(); } else { document.getElementById('result-msg').innerHTML = '<h4 class="text-danger fw-bold">未達及格分數 (70分)，再接再厲！</h4>'; }
    }

    function exportIncorrectPDF() { document.getElementById('review-area').style.display = 'block'; document.body.classList.add('preview-active'); if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) { setTimeout(() => { window.print(); }, 500); } else { savedZoomBeforePreview = currentZoom; currentZoom = 0.7; applyZoom(); const closeBtn = document.createElement('button'); closeBtn.innerHTML = '⬅️ 結束預覽'; closeBtn.className = 'btn btn-dark btn-lg fixed-bottom m-3 no-print'; closeBtn.onclick = () => { document.getElementById('review-area').style.display = 'none'; document.body.classList.remove('preview-active'); currentZoom = savedZoomBeforePreview; applyZoom(); closeBtn.remove(); }; document.body.appendChild(closeBtn); } }
    function launchFireworks() { var duration = 5 * 1000, animationEnd = Date.now() + duration, defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 }; var interval = setInterval(function() { var timeLeft = animationEnd - Date.now(); if (timeLeft <= 0) return clearInterval(interval); var particleCount = 50 * (timeLeft / duration); confetti(Object.assign({}, defaults, { particleCount, origin: { x: Math.random()*0.2+0.1, y: Math.random()-0.2 } })); confetti(Object.assign({}, defaults, { particleCount, origin: { x: Math.random()*0.2+0.7, y: Math.random()-0.2 } })); }, 250); }
    startExam();
</script>
</body>
</html>
"""

    subject_map = {
        "AI900": {"title": "Microsoft AI-900", "count": 50},
        "AZ900": {"title": "Microsoft AZ-900", "count": 50},
        "Generative_AI": {"title": "Generative AI Foundations", "count": 40},
        "ITS_AI": {"title": "ITS Artificial Intelligence", "count": 40},
        "ITS_Database": {"title": "ITS Database Administration", "count": 40},
        "ITS_Python": {"title": "ITS Python Programming", "count": 50},
        "ITS_softdevelop": {"title": "ITS Software Development", "count": 50}
    }

    for sub, info in subject_map.items():
        dir_path = os.path.join('www', sub)
        html_path = os.path.join(dir_path, 'mock_exam.html')
        json_files = [f for f in os.listdir(dir_path) if f.startswith('questions_') and f.endswith('.json')]
        if not json_files: continue
        
        with open(os.path.join(dir_path, json_files[0]), 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)
            
        res = template_start.replace('{{TITLE}}', info['title']).replace('{{COUNT}}', str(info['count']))
        res += json.dumps(quiz_data, ensure_ascii=False)
        res += template_end.replace('{{SUB_ID}}', sub.lower()).replace('{{COUNT}}', str(info['count']))
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(res)
        print(f"Force Re-generated: {sub}/mock_exam.html")

if __name__ == "__main__":
    generate_fresh_mock()
