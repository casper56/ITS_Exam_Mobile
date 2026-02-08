import json
import os
import sys

def create_mock_exam_html(json_file, output_html, subject_name):
    display_title = f"{subject_name} 模擬考試"
    
    # Load JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file {json_file}: {e}")
        return

    json_str = json.dumps(data, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-solarized-light.min.css" rel="stylesheet" />
    <style>
        body {{ background-color: #f8f9fa; font-family: "Microsoft JhengHei", sans-serif; overflow-y: auto; }}
        .exam-header {{ position: fixed; top: 0; left: 0; right: 0; z-index: 1050; background: #212529; color: white; padding: 10px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
        .timer-box {{ font-size: 1.5rem; font-weight: bold; color: #ffc107; }}
        .main-content {{ margin-top: 80px; padding-bottom: 100px; }}
        .question-card {{ border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; margin-bottom: 25px; overflow: visible !important; }}
        .question-header {{ background-color: #fff; border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; }}
        .question-body {{ padding: 20px 25px; font-size: 1rem; overflow: visible !important; }}
        .option-item {{ list-style: none; margin-bottom: 8px; padding: 10px 15px; border: 1px solid #e9ecef; border-radius: 8px; cursor: pointer; transition: all 0.2s; }}
        .option-item:hover {{ background-color: #f8f9fa; border-color: #adb5bd; }}
        .option-item.selected {{ background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }}
        .sub-opt-container {{ padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 6px; cursor: pointer; background: #f8f9fa; transition: all 0.2s; }}
        .sub-opt-container.selected {{ background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }}
        .sub-question-label {{ font-weight: bold; margin-top: 15px; margin-bottom: 8px; color: #495057; border-left: 4px solid #198754; padding-left: 10px; }}
        #result-screen {{ display: none; text-align: center; padding: 50px 20px; }}
        .score-circle {{ width: 150px; height: 150px; border-radius: 50%; border: 8px solid #0d6efd; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: bold; margin: 20px auto; color: #0d6efd; }}
        code {{ font-family: Consolas, Monaco, monospace; color: #212529; background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; border: 1px solid #dee2e6; white-space: pre-wrap !important; word-break: break-all !important; overflow: visible !important; }}
        pre {{ white-space: pre-wrap !important; word-break: break-all !important; overflow: visible !important; margin: 0; }}
        
        /* Semi-circle Side Buttons */
        .side-nav-btn {{
            position: fixed;
            top: 55%;
            transform: translateY(-50%);
            width: 40px;
            height: 100px;
            background: rgba(13, 110, 253, 0.85);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 1060;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            font-size: 1.5rem;
            border: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            outline: none !important;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
            font-family: serif;
            font-weight: bold;
        }}
        .side-nav-btn:hover {{
            background: #0d6efd;
            width: 50px;
            color: white;
        }}
        .side-nav-prev {{ 
            left: 0; 
            border-radius: 0 50px 50px 0; 
            padding-right: 8px;
        }}
        .side-nav-next {{ 
            right: 0; 
            border-radius: 50px 0 0 50px;
            padding-left: 8px;
        }}
        .side-nav-btn.disabled {{
            display: none;
        }}

        @media (max-width: 768px) {{
            .side-nav-btn {{ width: 35px; height: 80px; font-size: 1.2rem; background: rgba(33, 37, 41, 0.7); }}
            .side-nav-btn:hover {{ width: 40px; }}
        }}

        /* 列印與預覽錯誤題目樣式 */
        #review-area {{ display: none; text-align: left; margin-top: 30px; border-top: 2px solid #dee2e6; padding-top: 20px; }}
        .review-item {{ margin-bottom: 30px; padding: 15px; border: 1px solid #eee; border-radius: 8px; page-break-inside: avoid; }}
        .review-id {{ font-weight: bold; color: #212529; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
        .review-ans {{ color: #198754; font-weight: bold; background: #e9f7ef; padding: 5px 10px; border-radius: 4px; margin: 10px 0; }}
        .review-exp {{ font-size: 0.95rem; color: #666; border-left: 3px solid #0d6efd; padding-left: 10px; }}

        @media print {{
            @page {{ size: auto; margin: 10mm; }}
            * {{ 
                overflow: visible !important; 
                max-height: none !important; 
                height: auto !important;
            }}
            html, body {{ 
                background: white; 
                width: 100%; 
                margin: 0; 
                padding: 0; 
            }}
            #exam-ui, #result-screen h2, .score-circle, .lead, #result-msg, .no-print {{ display: none !important; }}
            #result-screen {{ display: block !important; padding: 0 !important; width: 100% !important; }}
            #review-area {{ display: block !important; border: none !important; width: 100% !important; }}
            .review-item {{ border: 1px solid #ccc !important; width: 100% !important; page-break-inside: avoid; margin-bottom: 20px !important; }}
            pre, code {{ 
                white-space: pre-wrap !important; 
                word-break: break-all !important; 
                border: none !important;
            }}
        }}
    </style>
</head>
<body>

<div id="exam-ui">
    <header class="exam-header d-flex justify-content-between align-items-center">
        <div><h5 class="m-0">{display_title}</h5><small id="q-progress">1 / 50</small></div>
        <div class="timer-box" id="timer">50:00</div>
        <button class="btn btn-danger btn-sm" onclick="confirmSubmit()">交卷</button>
    </header>

    <div class="side-nav-btn side-nav-prev" id="side-btn-prev" onclick="changeQuestion(-1)" title="上一題">&#10094;</div>
    <div class="side-nav-btn side-nav-next" id="side-btn-next" onclick="changeQuestion(1)" title="下一題">&#10095;</div>

    <main class="container main-content">
        <div id="question-area"></div>
    </main>
</div>

<div id="result-screen" class="container">
    <h2 class="mb-4">考試結束</h2>
    <div class="score-circle" id="final-score">0</div>
    <p class="lead">答對題數：<span id="correct-count">0</span> / 50</p>
    <div id="category-stats" class="mb-4"></div>
    <div id="result-msg" class="mb-4"></div>
    <div class="mt-5 no-print">
        <a href="../index.html" class="btn btn-primary btn-lg me-2">回首頁</a>
        <button class="btn btn-outline-secondary btn-lg me-2" onclick="location.reload()">重新挑戰</button>
        <button id="btn-export-pdf" class="btn btn-success btn-lg" onclick="exportIncorrectPDF()" style="display:none;">💾 匯出錯誤題目 PDF</button>
    </div>

    <!-- 錯誤題目回顧區 (預覽與列印用) -->
    <div id="review-area">
        <h3 class="mb-4 text-center">錯誤題目回顧報告</h3>
        <div id="review-list"></div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

<script>
    const allQuestions = {json_str};
    let examQuestions = [];
    let currentIndex = 0;
    let userAnswers = {{}}; 
    let timeLeft = 50 * 60; 
    let timerInterval;

    function startExam() {{
        // Group questions by category
        const groups = {{}};
        allQuestions.forEach(q => {{
            const cat = q.category || 'D7_其他進階題型';
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(q);
        }});

        const d1Key = 'D1_資料型別與運算子';
        let selected = [];
        
        // 1. Handle D1 specifically (max 17)
        if (groups[d1Key]) {{
            const d1Pool = [...groups[d1Key]].sort(() => 0.5 - Math.random());
            selected = d1Pool.slice(0, Math.min(17, d1Pool.length));
        }}

        // 2. Fill the rest from other categories
        let otherPool = [];
        Object.keys(groups).forEach(cat => {{
            if (cat !== d1Key) {{
                otherPool = otherPool.concat(groups[cat]);
            }}
        }});
        
        // Add remaining D1 questions back to otherPool if needed (though usually we just want to limit them)
        // If we strictly want MAX 22, we don't add the rest of D1 back.
        
        otherPool.sort(() => 0.5 - Math.random());
        const needed = 50 - selected.length;
        selected = selected.concat(otherPool.slice(0, needed));

        // 3. Final Shuffle
        examQuestions = selected.sort(() => 0.5 - Math.random());
        
        renderQuestion(0);
        startTimer();
    }}

    function startTimer() {{
        timerInterval = setInterval(() => {{
            timeLeft--;
            let mins = Math.floor(timeLeft / 60);
            let secs = timeLeft % 60;
            document.getElementById('timer').innerText = `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
            if (timeLeft <= 0) {{
                alert("時間到！系統自動交卷。");
                submitExam();
            }}
        }}, 1000);
    }}

    function renderQuestion(index, scrollTop = true) {{
        currentIndex = index;
        const item = examQuestions[index];
        const container = document.getElementById('question-area');
        container.innerHTML = '';

        document.getElementById('q-progress').innerText = `題目 ${{index + 1}} / 50`;
        
        // Update Side Buttons
        const sidePrev = document.getElementById('side-btn-prev');
        const sideNext = document.getElementById('side-btn-next');
        if (sidePrev) sidePrev.style.display = index === 0 ? 'none' : 'flex';
        if (sideNext) {{
            sideNext.style.display = 'flex';
            sideNext.title = index === 49 ? '交卷' : '下一題';
        }}

        const card = document.createElement('div');
        card.className = 'card question-card';
        
        let qText = item.question.replace(/●/g, '<br/>●').replace(/^\d+\.\s*/, '');
        
        let html = `
            <div class="question-header">Question ${{index + 1}} / 50</div>
            <div class="question-body">
                <div class="mb-4">${{qText}}</div>
        `;

        if (item.image) html += `<div class="text-center mb-4"><img src="${{item.image}}" style="max-width:100%; border:1px solid #ddd; border-radius:4px;"></div>`;

        const options = item.quiz || item.options || [];
        const savedAns = userAnswers[index];

        html += '<div class="mt-3">';
        options.forEach((opt, optIdx) => {{
            const optStr = String(opt);
            if (optStr.includes('|')) {{
                const subOpts = optStr.split('|');
                html += `<div class="sub-question-label">選項 ${{optIdx + 1}}</div>`;
                html += `<div class="d-flex flex-wrap gap-2 mb-3 ms-2">`;
                subOpts.forEach((sub, subIdx) => {{
                    const isSel = (savedAns && savedAns[optIdx] === subIdx);
                    html += `
                        <div class="sub-opt-container ${{isSel ? 'selected' : ''}}" onclick="selectSub(${{optIdx}}, ${{subIdx}})">
                            (${{subIdx+1}}) ${{sub}}
                        </div>`;
                }});
                html += `</div>`;
            }} else {{
                const isSel = Array.isArray(savedAns) ? savedAns.includes(optIdx) : savedAns === optIdx;
                html += `
                    <div class="option-item ${{isSel ? 'selected' : ''}}" onclick="selectOption(${{optIdx}})">
                        ${{optIdx + 1}}. ${{optStr}}
                    </div>`;
            }}
        }});
        html += '</div></div>';
        card.innerHTML = html;
        container.appendChild(card);
        Prism.highlightAll();
        if (scrollTop) window.scrollTo(0, 0);
    }}

    function selectOption(optIdx) {{
        const item = examQuestions[currentIndex];
        if (item.type === 'multiple') {{
            if (!Array.isArray(userAnswers[currentIndex])) userAnswers[currentIndex] = [];
            const idx = userAnswers[currentIndex].indexOf(optIdx);
            if (idx > -1) userAnswers[currentIndex].splice(idx, 1);
            else userAnswers[currentIndex].push(optIdx);
        }} else {{
            userAnswers[currentIndex] = optIdx;
        }}
        renderQuestion(currentIndex, false);
    }}

    function selectSub(quizIdx, subIdx) {{
        if (typeof userAnswers[currentIndex] !== 'object' || userAnswers[currentIndex] === null) {{
            userAnswers[currentIndex] = {{}};
        }}
        userAnswers[currentIndex][quizIdx] = subIdx;
        renderQuestion(currentIndex, false);
    }}

    function changeQuestion(dir) {{
        let next = currentIndex + dir;
        if (next >= 0 && next < 50) renderQuestion(next);
        else if (next === 50) confirmSubmit();
    }}

    function confirmSubmit() {{
        const answeredCount = Object.keys(userAnswers).length;
        if (answeredCount < 50) {{
            if (!confirm(`您還有 ${{50 - answeredCount}} 題未作答，確定要交卷嗎？`)) return;
        }} else {{
            if (!confirm('確定要交卷嗎？')) return;
        }}
        submitExam();
    }}

    function submitExam() {{
        clearInterval(timerInterval);
        let correctCount = 0;
        let incorrectHTML = '';
        const stats = {{}}; // {{ category: {{ total: 0, correct: 0 }} }}

        examQuestions.forEach((item, idx) => {{
            const cat = item.category || '未分類';
            if (!stats[cat]) stats[cat] = {{ total: 0, correct: 0 }};
            stats[cat].total++;

            const userAns = userAnswers[idx];
            let isCorrect = false;

            if (item.type === 'multioption') {{
                const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
                isCorrect = answers.every((a, i) => userAns && (parseInt(a) - 1) === userAns[i]);
            }} else if (item.type === 'multiple') {{
                const answers = item.answer.map(a => parseInt(a) - 1);
                isCorrect = Array.isArray(userAns) && 
                            userAns.length === answers.length && 
                            userAns.every(val => answers.includes(val));
            }} else {{
                isCorrect = userAns === (parseInt(item.answer) - 1);
            }}

            if (isCorrect) {{
                correctCount++;
                stats[cat].correct++;
            }} else {{
                let qText = item.question.replace(/●/g, '<br/>●');
                let ansText = Array.isArray(item.answer) ? item.answer.join(', ') : item.answer;
                incorrectHTML += `
                    <div class="review-item">
                        <div class="review-id">題目 ${{idx + 1}} (原始編號: ${{item.id}})</div>
                        <div class="mb-2">${{qText}}</div>
                        <div class="review-ans">正確答案：${{ansText}}</div>
                        <div class="review-exp"><b>解析：</b><br/>${{(item.explanation || '暫無解析。').replace(/●/g, '<br/>●')}}</div>
                    </div>`;
            }}
        }});

        // Generate Stats HTML
        let statsHTML = '<div class="row justify-content-center"><div class="col-md-10"><div class="card shadow-sm border-0"><div class="card-header bg-dark text-white fw-bold">各類題數佔比與答對率</div><div class="table-responsive"><table class="table table-hover mb-0 text-start align-middle"><thead><tr><th>題目分類</th><th class="text-center">題數</th><th class="text-center">佔比</th><th class="text-center">答對率</th></tr></thead><tbody>';
        
        // Sort categories D1, D2, D3...
        const sortedCats = Object.keys(stats).sort();

        sortedCats.forEach(cat => {{
            const data = stats[cat];
            const percent = ((data.total / 50) * 100).toFixed(1);
            const accuracy = ((data.correct / data.total) * 100).toFixed(0);
            const badgeClass = accuracy >= 70 ? 'bg-success' : (accuracy >= 40 ? 'bg-warning text-dark' : 'bg-danger');
            
            statsHTML += `<tr>
                <td class="fw-bold">${{cat}}</td>
                <td class="text-center"><span class="badge bg-secondary rounded-pill">${{data.total}}</span></td>
                <td class="text-center text-muted small">${{percent}}%</td>
                <td class="text-center"><div class="progress" style="height: 20px;"><div class="progress-bar ${{badgeClass}}" role="progressbar" style="width: ${{accuracy}}%">${{accuracy}}%</div></div></td>
            </tr>`;
        }});
        statsHTML += '</tbody></table></div></div></div></div>';
        document.getElementById('category-stats').innerHTML = statsHTML;

        document.getElementById('exam-ui').style.display = 'none';
        document.getElementById('result-screen').style.display = 'block';
        document.getElementById('correct-count').innerText = correctCount;
        
        const score = Math.round((correctCount / 50) * 100);
        document.getElementById('final-score').innerText = score;
        
        if (correctCount < 50) {{
            document.getElementById('btn-export-pdf').style.display = 'inline-block';
            document.getElementById('review-list').innerHTML = incorrectHTML;
        }}

        if (score >= 70) {{
            document.getElementById('result-msg').innerHTML = '<h4 class="text-success fw-bold">恭喜通過！🎉</h4>';
            launchFireworks();
        }}
        else document.getElementById('result-msg').innerHTML = '<h4 class="text-danger fw-bold">未達及格分數 (70分)，再接再厲！</h4>';
    }}

    function exportIncorrectPDF() {{
        document.getElementById('review-area').style.display = 'block';
        window.print();
        setTimeout(() => {{ document.getElementById('review-area').style.display = 'none'; }}, 1000);
    }}

    function launchFireworks() {{
        var duration = 5 * 1000;
        var animationEnd = Date.now() + duration;
        var defaults = {{ startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 }};
        function randomInRange(min, max) {{ return Math.random() * (max - min) + min; }}
        var interval = setInterval(function() {{
            var timeLeft = animationEnd - Date.now();
            if (timeLeft <= 0) return clearInterval(interval);
            var particleCount = 50 * (timeLeft / duration);
            confetti(Object.assign({{}}, defaults, {{ particleCount, origin: {{ x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 }} }}));
            confetti(Object.assign({{}}, defaults, {{ particleCount, origin: {{ x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 }} }}));
        }}, 250);
    }}

    startExam();
</script>
</body>
</html>"""
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully created Mock Exam: {output_html}")

if __name__ == "__main__":
    create_mock_exam_html('questions_ITS_python.json', 'mock_exam.html', 'ITS Python')