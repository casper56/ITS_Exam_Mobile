import json
import os

def get_domain(text):
    text = text.lower()
    if any(k in text for k in ['stack', 'queue', '堆疊', '佇列', '遞迴', 'recursive', '演算法', 'apcs']):
        return 'D7_進階題(APCS/演算法)'
    if any(k in text for k in ['try:', 'except', 'finally', 'raise', 'unittest', 'assert', '斷言', '除錯', 'error']):
        return 'D5_錯誤處理與測試'
    if any(k in text for k in ['import ', 'math.', 'random.', 'datetime.', 'os.', 'sys.', 'time.', 'randint', 'strftime', 'floor(', 'ceil(']):
        return 'D6_模組與工具'
    if any(k in text for k in ['def ', 'return', 'class ', 'docstring', '註解', 'comment', '引數', '參數']):
        return 'D4_程式碼文件與結構'
    if any(k in text for k in ['input(', 'print(', 'format(', 'f-string', '檔案', 'open(', 'read(', 'write(']):
        return 'D3_輸入與輸出'
    if any(k in text for k in ['if ', 'elif', 'else:', 'while', 'for ', 'break', 'continue', 'range', '迴圈']):
        return 'D2_流程控制'
    return 'D1_資料型別與運算子'

def generate_exam():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'questions_ITS_python.json')
    html_path = os.path.join(base_dir, 'mock_exam.html')

    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    for q in questions:
        content = (q.get('question', '') + str(q.get('explanation', ''))).lower()
        q['category'] = get_domain(content)
    
    json_str = json.dumps(questions, ensure_ascii=False)

    html_head = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ITS Python 模擬考試</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-solarized-light.min.css" rel="stylesheet" />
    <style>
        body { background-color: #f8f9fa; font-family: "Microsoft JhengHei", sans-serif; -webkit-font-smoothing: antialiased; }
        .exam-header { position: fixed; top: 0; left: 0; right: 0; z-index: 1050; background: #212529; color: white; padding: 10px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .timer-box { font-size: 1.5rem; font-weight: bold; color: #ffc107; }
        .main-content { margin-top: 80px; padding-bottom: 100px; }
        .question-card { border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; margin-bottom: 25px; }
        .question-header { background-color: #fff; border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; }
        .question-body { padding: 20px 25px; font-size: 1rem; }
        .option-item { list-style: none; margin-bottom: 8px; padding: 10px 15px; border: 1px solid #e9ecef; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
        .option-item:hover { background-color: #f8f9fa; border-color: #adb5bd; }
        .option-item.selected { background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }
        .sub-opt-container { padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 6px; cursor: pointer; background: #f8f9fa; transition: all 0.2s; }
        .sub-opt-container.selected { background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }
        .sub-question-label { font-weight: bold; margin-top: 15px; margin-bottom: 8px; color: #495057; border-left: 4px solid #198754; padding-left: 10px; }
        #result-screen { display: none; text-align: center; padding: 50px 20px; }
        .score-circle { width: 150px; height: 150px; border-radius: 50%; border: 8px solid #0d6efd; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: bold; margin: 20px auto; color: #0d6efd; }
        code { font-family: Consolas, Monaco, monospace; color: #d63384; background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; }
        
        #loading-overlay {
            display: none;
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 99999;
            color: white;
            text-align: center;
            padding-top: 20%;
            font-size: 1.5rem;
        }
        
        #review-container { 
            display: none; 
            background: white; 
            color: black;
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
        }
        .review-block {
            background: white;
            padding: 15px;
            border: 1px solid #000;
            margin-bottom: 15px;
            color: black;
        }
        
        @media print {
            #exam-ui, #result-screen, .no-print { display: none !important; }
            #review-container { display: block !important; padding: 0; }
            body { background: white; }
        }
    </style>
</head>
<body>

<div id="loading-overlay">
    <div class="spinner-border text-light mb-3" role="status"></div><br>
    <div id="loading-text">正在準備資料...</div>
    <div class="progress mt-3" style="width: 50%; margin: 0 auto; height: 20px;">
        <div id="pdf-progress-bar" class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" style="width: 0%"></div>
    </div>
</div>

<div id="exam-ui">
    <header class="exam-header d-flex justify-content-between align-items-center">
        <div><h5 class="m-0">ITS Python 模擬考試</h5><small id="q-progress">1 / 50</small></div>
        <div class="timer-box" id="timer">50:00</div>
        <button class="btn btn-danger btn-sm" onclick="confirmSubmit()">交卷</button>
    </header>

    <main class="container main-content">
        <div id="question-area"></div>
        <div class="d-flex justify-content-between mt-4">
            <button class="btn btn-secondary px-4" id="btn-prev" onclick="changeQuestion(-1)">⬅️ 上一題</button>
            <button class="btn btn-primary px-5" id="btn-next" onclick="changeQuestion(1)">下一題 ➡️</button>
        </div>
    </main>
</div>

<div id="result-screen" class="container">
    <h2 class="mb-4">考試結束</h2>
    <div class="score-circle" id="final-score">0</div>
    <p class="lead">答對題數：<span id="correct-count">0</span> / 50</p>
    <div id="result-msg" class="mb-4"></div>
    <div id="weakness-analysis" class="mb-4 text-start"></div>
    <div class="mt-5 no-print">
        <a href="../index.html" class="btn btn-primary btn-lg me-2">回首頁</a>
        <button class="btn btn-outline-secondary btn-lg me-2" onclick="location.reload()">重新挑戰</button>
        <button id="btn-export-pdf" class="btn btn-success btn-lg" onclick="showReviewReport()">下載PDF</button>
    </div>
</div>

<div id="review-container">
    <div class="review-header" style="text-align:center; padding:20px; border-bottom:2px solid #000; margin-bottom:20px;">
        <h2 style="color:#000; font-weight:900;">ITS Python 模擬考檢討報告</h2>
        <p style="color:#666;">產出時間：<span id="report-time"></span></p>
        <div class="no-print" style="margin-top:15px; background:#e8f4fd; padding:10px; border-radius:5px; border:1px solid #b6effb;">
            <button class="btn btn-primary btn-sm me-2" onclick="downloadPDF()">下載PDF</button>
            <button class="btn btn-secondary btn-sm me-2" onclick="window.print()">🖨️ 瀏覽器列印</button>
            <button class="btn btn-outline-dark btn-sm" onclick="location.reload()">❌ 關閉</button>
        </div>
    </div>
    <div id="review-content"></div>
</div>

<div id="pdf-sandbox" style="position:fixed; top:0; left:-9999px; width:750px; background:white; z-index:-1;"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

<script>
"""

    js_logic = """
    const allQuestions = """ + json_str + """;

    const categories = [
        'D1_資料型別與運算子',
        'D2_流程控制',
        'D3_輸入與輸出',
        'D4_程式碼文件與結構',
        'D5_錯誤處理與測試',
        'D6_模組與工具',
        'D7_進階題(APCS/演算法)'
    ];

    let examQuestions = [];
    let currentIndex = 0;
    let userAnswers = {}; 
    let timeLeft = 50 * 60; 
    let timerInterval;
    let incorrectItems = [];
    let globalIncorrectHTML = "";

    function startExam() {
        let selectedQuestions = [];
        let buckets = {};
        
        // 1. 初始化桶子
        categories.forEach(cat => {
            buckets[cat] = allQuestions.filter(q => q.category === cat)
                                       .sort(() => 0.5 - Math.random());
        });

        // 2. 核心：混合限額抽題
        // 先從 D7 抽取 3 題 (硬上限)
        let d7pool = buckets['D7_進階題(APCS/演算法)'];
        let d7take = Math.min(d7pool.length, 3);
        selectedQuestions.push(...d7pool.splice(0, d7take));

        // 計算剩餘所需題目 (目標 50 題)
        let remainingNeed = 50 - selectedQuestions.length;
        const mainCategories = categories.filter(c => c !== 'D7_進階題(APCS/演算法)');
        
        // 使用平衡配額抽剩餘題目
        let cap = Math.ceil(remainingNeed / mainCategories.length); // 初始配額約 8 題
        
        while(selectedQuestions.length < 50 && cap < 50) {
            let currentSelectionCount = selectedQuestions.length;
            mainCategories.forEach(cat => {
                if (selectedQuestions.length < 50) {
                    let pool = buckets[cat];
                    let canTake = Math.min(pool.length, cap) - (50 - remainingNeed); // 此處邏輯微調
                    // 簡化抽法：在 mainCategories 間輪流抽，直到滿
                }
            });
            
            // 重新實作更穩健的輪流抽法
            let tempPool = [];
            mainCategories.forEach(cat => {
                tempPool.push(...buckets[cat].slice(0, cap));
            });
            
            if (tempPool.length >= remainingNeed) {
                selectedQuestions.push(...tempPool.sort(() => 0.5 - Math.random()).slice(0, remainingNeed));
                break;
            }
            cap++;
        }

        examQuestions = selectedQuestions.sort(() => 0.5 - Math.random());
        renderQuestion(0);
        startTimer();
        console.log("出題完成。D7數量:", d7take);
    }

    function startTimer() {
        timerInterval = setInterval(() => {
            timeLeft--;
            let mins = Math.floor(timeLeft / 60);
            let secs = timeLeft % 60;
            document.getElementById('timer').innerText = `${mins}:${secs.toString().padStart(2, '0')}`;
            if (timeLeft <= 0) { alert("時間到！系統自動交卷。"); submitExam(); }
        }, 1000);
    }

    function renderQuestion(index) {
        currentIndex = index;
        const item = examQuestions[index];
        const container = document.getElementById('question-area');
        container.innerHTML = '';
        document.getElementById('q-progress').innerText = `題目 ${index + 1} / 50`;
        document.getElementById('btn-prev').disabled = index === 0;
        document.getElementById('btn-next').innerText = index === 49 ? '完成答題 (交卷)' : '下一題 ➡️';

        let qText = item.question.replace(/●/g, '<br/>●').replace(/^\\d+\\.\\s*/, '');
        let html = `<div class="card question-card"><div class="question-header">Question ${index + 1} / 50 <span class="badge bg-light text-dark float-end">${item.category || ''}</span></div><div class="question-body"><div class="mb-4">${qText}</div>`;
        if (item.image) html += `<div class="text-center mb-4"><img src="${item.image}" style="max-width:100%; border:1px solid #ddd; border-radius:4px;"></div>`;
        const options = item.quiz || item.options || [];
        const savedAns = userAnswers[index];
        html += '<div class="mt-3">';
        options.forEach((opt, optIdx) => {
            const optStr = String(opt);
            if (optStr.includes('|')) {
                const subOpts = optStr.split('|');
                html += `<div class="sub-question-label">子題目 ${optIdx + 1}</div><div class="d-flex flex-wrap gap-2 mb-3 ms-2">`;
                subOpts.forEach((sub, subIdx) => {
                    const isSel = (savedAns && savedAns[optIdx] === subIdx);
                    html += `<div class="sub-opt-container ${isSel ? 'selected' : ''}" onclick="selectSub(${optIdx}, ${subIdx})">(${subIdx+1}) ${sub}</div>`;
                });
                html += `</div>`;
            } else {
                const isSel = Array.isArray(savedAns) ? savedAns.includes(optIdx) : savedAns === optIdx;
                html += `<div class="option-item ${isSel ? 'selected' : ''}" onclick="selectOption(${optIdx})">${optIdx + 1}. ${optStr}</div>`;
            }
        });
        html += '</div></div></div>';
        container.innerHTML = html;
        Prism.highlightAll();
    }

    function selectOption(optIdx) {
        const item = examQuestions[currentIndex];
        if (item.type === 'multiple') {
            if (!Array.isArray(userAnswers[currentIndex])) userAnswers[currentIndex] = [];
            const idx = userAnswers[currentIndex].indexOf(optIdx);
            if (idx > -1) userAnswers[currentIndex].splice(idx, 1); else userAnswers[currentIndex].push(optIdx);
        } else userAnswers[currentIndex] = optIdx;
        renderQuestion(currentIndex);
    }

    function selectSub(qIdx, sIdx) {
        if (!userAnswers[currentIndex] || typeof userAnswers[currentIndex] !== 'object') userAnswers[currentIndex] = {};
        userAnswers[currentIndex][qIdx] = sIdx;
        renderQuestion(currentIndex);
    }

    function changeQuestion(dir) {
        let next = currentIndex + dir;
        if (next >= 0 && next < 50) renderQuestion(next); else if (next === 50) confirmSubmit();
    }

    function confirmSubmit() {
        if (confirm('確定要交卷嗎？')) submitExam();
    }

    function showWeaknessAnalysis(stats) {
        let html = `<div class="card mt-4 shadow-sm"><div class="card-header bg-dark text-white fw-bold">各領域表現分析</div><div class="card-body p-0"><table class="table table-hover m-0" style="font-size: 0.9rem;"><thead class="table-light"><tr><th>領域 (Domain)</th><th class="text-center">題數</th><th class="text-center">答對</th><th class="text-center">答對率</th></tr></thead><tbody>`;
        categories.forEach(cat => {
            if (!stats[cat]) return;
            let data = stats[cat];
            let rate = Math.round((data.correct / data.total) * 100);
            let color = rate >= 80 ? 'text-success' : (rate >= 60 ? 'text-warning' : 'text-danger');
            html += `<tr><td>${cat}</td><td class="text-center">${data.total}</td><td class="text-center">${data.correct}</td><td class="text-center fw-bold ${color}">${rate}%</td></tr>`;
        });
        html += '</tbody></table></div></div>';
        document.getElementById('weakness-analysis').innerHTML = html;
    }

    function submitExam() {
        clearInterval(timerInterval);
        let correctCount = 0;
        let catStats = {};
        incorrectItems = [];
        globalIncorrectHTML = "";

        examQuestions.forEach((item, idx) => {
            let cat = item.category || 'D1_資料型別與運算子';
            if(!catStats[cat]) catStats[cat] = { total: 0, correct: 0 };
            catStats[cat].total++;
            const userAns = userAnswers[idx];
            let isCorrect = false;
            if (item.type === 'multioption') {
                const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
                isCorrect = answers.every((a, i) => userAns && (parseInt(a) - 1) === userAns[i]);
            } else if (item.type === 'multiple') {
                const answers = item.answer.map(a => parseInt(a) - 1);
                isCorrect = Array.isArray(userAns) && userAns.length === answers.length && userAns.every(v => answers.includes(v));
            } else isCorrect = userAns === (parseInt(item.answer) - 1);

            if (isCorrect) { correctCount++; catStats[cat].correct++; } 
            else {
                let qClean = item.question.replace(/<pre[^>]*>([\s\S]*?)<\/pre>/gi, '<div style="font-family:monospace; font-size:10pt; white-space: pre-wrap; background:#f4f4f4; border:1px solid #000; padding:8px; margin:10px 0; color:#000 !important;">$1</div>').replace(/<br[^>]*>/gi, " ");
                qClean = qClean.replace(/<code[^>]*>([\s\S]*?)<\\/code>/gi, '<code style="color:#000 !important; font-weight:bold;">$1</code>');
                let options = item.quiz || item.options || [];
                let optsHTML = '<ul style="margin: 10px 0 10px 20px; padding: 0; font-size: 10pt; color: #000; list-style:none;">';
                options.forEach((o, i) => { optsHTML += `<li style="margin-bottom: 4px; color:#000 !important;">(${i+1}) ${o}</li>`; });
                optsHTML += '</ul>';
                let block = `<div class="review-block" style="border: 1px solid #000; padding: 15px; margin-bottom: 20px; color:#000 !important; background:white;"><div style="font-weight:900; color:#000 !important; font-size:12pt; margin-bottom:8px; border-bottom: 1px solid #000; padding-bottom: 5px;">題目 ${idx+1} [${cat}]</div><div style="font-size:11pt; line-height:1.6; font-weight: 600; color:#000 !important;">${qClean}</div><div style="margin:10px 0; color:#000 !important;">${optsHTML}</div><div style="font-weight:900; color:#198754 !important; background:#e9f7ef; padding:5px 10px; border-radius:4px; display:inline-block; border:1px solid #badbcc;">正確答案：${item.answer}</div><div style="font-size:10pt; color:#333; background:#f8f9fa; padding:10px; border-left:4px solid #000; margin-top:10px;"><b>解析：</b><br/>${(item.explanation || '無').replace(/●/g, '<br/>●')}</div></div>`;
                incorrectItems.push(block);
                globalIncorrectHTML += block;
            }
        });

        document.getElementById('exam-ui').style.display = 'none';
        document.getElementById('result-screen').style.display = 'block';
        document.getElementById('correct-count').innerText = correctCount;
        const score = Math.round((correctCount / 50) * 100);
        document.getElementById('final-score').innerText = score;
        showWeaknessAnalysis(catStats);
        if (correctCount < 50) document.getElementById('btn-export-pdf').style.display = 'inline-block';
    }

    function showReviewReport() {
        document.getElementById('result-screen').style.display = 'none';
        document.getElementById('report-time').innerText = new Date().toLocaleString();
        document.getElementById('review-content').innerHTML = globalIncorrectHTML;
        document.getElementById('review-container').style.display = 'block';
        window.scrollTo(0, 0);
        setTimeout(downloadPDF, 1500); 
    }

    async function downloadPDF() {
        try {
            if (incorrectItems.length === 0) { alert("恭喜！沒有錯誤題目。"); return; }
            document.getElementById('loading-overlay').style.display = 'block';
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF('p', 'mm', 'a4');
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = pdf.internal.pageSize.getHeight();
            const margin = 10;
            let currentY = margin;
            const sandbox = document.getElementById('pdf-sandbox');

            sandbox.innerHTML = `<div style="text-align:center; padding: 20px; border-bottom: 3px solid #000; margin-bottom: 20px; background:white; width: 750px;"><h1 style="margin:0; font-size: 28pt; color: #000 !important; font-family: sans-serif; font-weight:900;">ITS Python 模擬考檢討報告</h1><p style="margin:10px 0 0 0; font-size: 14pt; color: #000 !important;">產出時間：${new Date().toLocaleString()}</p></div>`;
            const hCanvas = await html2canvas(sandbox, { scale: 2, useCORS: true });
            const hData = hCanvas.toDataURL('image/jpeg', 0.95);
            pdf.addImage(hData, 'JPEG', margin, currentY, pdfWidth - margin * 2, (hCanvas.height * (pdfWidth - margin * 2)) / hCanvas.width);
            currentY += (hCanvas.height * (pdfWidth - margin * 2)) / hCanvas.width + 10;

            for (let i = 0; i < incorrectItems.length; i++) {
                document.getElementById('pdf-progress-bar').style.width = Math.round(((i + 1) / incorrectItems.length) * 100) + '%';
                document.getElementById('loading-text').innerText = `正在處理第 ${i+1} / ${incorrectItems.length} 題...`;
                sandbox.innerHTML = incorrectItems[i];
                const canvas = await html2canvas(sandbox, { scale: 2, useCORS: true, width: 750 });
                const imgData = canvas.toDataURL('image/jpeg', 0.95);
                const imgHeight = (canvas.height * (pdfWidth - margin * 2)) / canvas.width;
                if (currentY + imgHeight > pdfHeight - margin) { pdf.addPage(); currentY = margin; }
                pdf.addImage(imgData, 'JPEG', margin, currentY, pdfWidth - margin * 2, imgHeight);
                currentY += imgHeight + 5;
                await new Promise(r => setTimeout(r, 20));
            }
            const ts = `${new Date().getFullYear().toString().slice(-2)}${(new Date().getMonth()+1).toString().padStart(2,'0')}${new Date().getDate().toString().padStart(2,'0')}${new Date().getHours().toString().padStart(2,'0')}${new Date().getMinutes().toString().padStart(2,'0')}`;
            pdf.save(`PYTHON_wrongcheck_${ts}.pdf`);
            document.getElementById('loading-overlay').style.display = 'none';
        } catch (e) { alert("PDF 失敗: " + e); document.getElementById('loading-overlay').style.display = 'none'; }
    }
    startExam();
    """

    final_content = html_head + js_logic + "\n</script>\n</body>\n</html>"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Fixed D7 quota to 3 questions and optimized balancing in {html_path}")

if __name__ == "__main__":
    generate_exam()
