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
        body {{ background-color: #f8f9fa; font-family: "Microsoft JhengHei", sans-serif; }}
        .exam-header {{ position: fixed; top: 0; left: 0; right: 0; z-index: 1050; background: #212529; color: white; padding: 10px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
        .timer-box {{ font-size: 1.5rem; font-weight: bold; color: #ffc107; }}
        .main-content {{ margin-top: 80px; padding-bottom: 100px; }}
        .question-card {{ border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; margin-bottom: 25px; }}
        .question-header {{ background-color: #fff; border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; }}
        .question-body {{ padding: 20px 25px; font-size: 1rem; }}
        .option-item {{ list-style: none; margin-bottom: 8px; padding: 10px 15px; border: 1px solid #e9ecef; border-radius: 8px; cursor: pointer; transition: all 0.2s; }}
        .option-item:hover {{ background-color: #f8f9fa; border-color: #adb5bd; }}
        .option-item.selected {{ background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }}
        .sub-opt-container {{ padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 6px; cursor: pointer; background: #f8f9fa; transition: all 0.2s; }}
        .sub-opt-container.selected {{ background-color: #cfe2ff; border-color: #0d6efd; color: #084298; font-weight: bold; }}
        .sub-question-label {{ font-weight: bold; margin-top: 15px; margin-bottom: 8px; color: #495057; border-left: 4px solid #198754; padding-left: 10px; }}
        #result-screen {{ display: none; text-align: center; padding: 50px 20px; }}
        .score-circle {{ width: 150px; height: 150px; border-radius: 50%; border: 8px solid #0d6efd; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: bold; margin: 20px auto; color: #0d6efd; }}
        code {{ font-family: Consolas, Monaco, monospace; color: #d63384; background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; }}
    </style>
</head>
<body>

<div id="exam-ui">
    <header class="exam-header d-flex justify-content-between align-items-center">
        <div><h5 class="m-0">{display_title}</h5><small id="q-progress">1 / 40</small></div>
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
    <p class="lead">答對題數：<span id="correct-count">0</span> / 40</p>
    <div id="result-msg" class="mb-4"></div>
    <div class="mt-5">
        <a href="../index.html" class="btn btn-primary btn-lg me-2">回首頁</a>
        <button class="btn btn-outline-secondary btn-lg" onclick="location.reload()">重新挑戰</button>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>

<script>
    const allQuestions = {json_str};
    let examQuestions = [];
    let currentIndex = 0;
    let userAnswers = {{}}; 
    let timeLeft = 50 * 60; 
    let timerInterval;

    function startExam() {{
        // 隨機抽取 40 題
        examQuestions = [...allQuestions].sort(() => 0.5 - Math.random()).slice(0, 40);
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

    function renderQuestion(index) {{
        currentIndex = index;
        const item = examQuestions[index];
        const container = document.getElementById('question-area');
        container.innerHTML = '';

        document.getElementById('q-progress').innerText = `題目 ${{index + 1}} / 40`;
        document.getElementById('btn-prev').disabled = index === 0;
        document.getElementById('btn-next').innerText = index === 39 ? '完成答題 (交卷)' : '下一題 ➡️';

        const card = document.createElement('div');
        card.className = 'card question-card';
        
        let qText = item.question.replace(/●/g, '<br/>●').replace(/^\d+\.\s*/, '');
        
        let html = `
            <div class="question-header">Question ${{index + 1}} / 40</div>
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
                html += `<div class="sub-question-label">子題目 ${{optIdx + 1}}</div>`;
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
        window.scrollTo(0, 0);
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
        renderQuestion(currentIndex);
    }}

    function selectSub(quizIdx, subIdx) {{
        if (typeof userAnswers[currentIndex] !== 'object' || userAnswers[currentIndex] === null) {{
            userAnswers[currentIndex] = {{}};
        }}
        userAnswers[currentIndex][quizIdx] = subIdx;
        renderQuestion(currentIndex);
    }}

    function changeQuestion(dir) {{
        let next = currentIndex + dir;
        if (next >= 0 && next < 40) renderQuestion(next);
        else if (next === 40) confirmSubmit();
    }}

    function confirmSubmit() {{
        const answeredCount = Object.keys(userAnswers).length;
        if (answeredCount < 40) {{
            if (!confirm(`您還有 ${{40 - answeredCount}} 題未作答，確定要交卷嗎？`)) return;
        }} else {{
            if (!confirm('確定要交卷嗎？')) return;
        }}
        submitExam();
    }}

    function submitExam() {{
        clearInterval(timerInterval);
        let correctCount = 0;

        examQuestions.forEach((item, idx) => {{
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

            if (isCorrect) correctCount++;
        }});

        document.getElementById('exam-ui').style.display = 'none';
        document.getElementById('result-screen').style.display = 'block';
        document.getElementById('correct-count').innerText = correctCount;
        
        const score = Math.round((correctCount / 40) * 100);
        document.getElementById('final-score').innerText = score;
        
        if (score >= 70) document.getElementById('result-msg').innerHTML = '<h4 class="text-success fw-bold">恭喜通過！🎉</h4>';
        else document.getElementById('result-msg').innerHTML = '<h4 class="text-danger fw-bold">未達及格分數 (70分)，再接再厲！</h4>';
    }}

    // 自動啟動
    startExam();
</script>
</body>
</html>"""
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully created Mock Exam: {output_html}")

if __name__ == "__main__":
    create_mock_exam_html('questions_ITS_python.json', 'mock_exam.html', 'ITS Python')
