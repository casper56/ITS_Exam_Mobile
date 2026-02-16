
import json
import os

html_path = 'www/ITS_Database/mock_exam.html'
json_path = 'www/ITS_Database/questions_ITS_Database.json'

# 1. 讀取乾淨數據 (使用 bytes 讀取以確保原汁原味)
with open(json_path, 'rb') as f:
    json_bytes = f.read()

# 2. 定義模板 (使用 bytes)
html_top = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>ITS Database 模擬考試</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f7f6; font-family: sans-serif; }
        .exam-header { position: fixed; top: 0; left: 0; right: 0; background: #212529; color: white; padding: 10px; z-index: 1000; }
        .main-content { margin-top: 80px; padding: 20px; max-width: 1000px; margin-left: auto; margin-right: auto; }
        .question-card { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .option-item { border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px; cursor: pointer; }
        .option-item.selected { background: #cfe2ff; border-color: #0d6efd; }
        #result-screen { display: none; text-align: center; padding: 50px; }
        .no-print { display: block; }
        @media print { .no-print { display: none; } #review-area { display: block; } }
    </style>
</head>
<body>
<div id="exam-ui">
    <header class="exam-header d-flex justify-content-between">
        <h5 id="q-title">模擬考試</h5>
        <div id="timer">50:00</div>
        <button class="btn btn-danger btn-sm" onclick="submitExam()">交卷</button>
    </header>
    <main class="main-content"><div id="question-area"></div></main>
</div>
<div id="result-screen"><h2>考試結束</h2><h1 id="score">0</h1><button class="btn btn-primary" onclick="window.print()">列印報告</button><div id="review-area"></div></div>
<script>
    const EXAM_LIMIT = 50;
    let currentIndex = 0, userAnswers = {}, examQuestions = [];
    
    function parseAnswerToIndex(val) {
        if (typeof val === 'number') return val - 1;
        if (typeof val === 'string') {
            const code = val.toUpperCase().charCodeAt(0);
            if (code >= 65 && code <= 90) return code - 65;
            return parseInt(val) - 1;
        }
        return -1;
    }

    const allQuestions = """.encode('utf-8')

html_bottom = """;

    function initExam() {
        const shuffled = [...allQuestions].sort(() => 0.5 - Math.random());
        examQuestions = shuffled.slice(0, EXAM_LIMIT);
        renderQuestion(0);
    }

    function renderQuestion(index) {
        currentIndex = index; const item = examQuestions[index];
        const container = document.getElementById('question-area');
        let html = `<h4>題目 ${index+1} / ${examQuestions.length}</h4><p>${item.question}</p>`;
        const opts = item.quiz || item.options || [];
        opts.forEach((opt, i) => {
            const isSel = userAnswers[index] === i;
            html += `<div class="option-item ${isSel?'selected':''}" onclick="selectOption(${i})">${i+1}. ${opt}</div>`;
        });
        container.innerHTML = html;
    }

    function selectOption(i) { userAnswers[currentIndex] = i; renderQuestion(currentIndex); }

    function submitExam() {
        document.getElementById('exam-ui').style.display = 'none';
        document.getElementById('result-screen').style.display = 'block';
        let correct = 0;
        examQuestions.forEach((item, idx) => {
            const correctIdx = parseAnswerToIndex(Array.isArray(item.answer) ? item.answer[0] : item.answer);
            if (userAnswers[idx] === correctIdx) correct++;
        });
        document.getElementById('score').innerText = Math.round(correct/examQuestions.length*100);
    }

    initExam();
</script>
</body>
</html>""".encode('utf-8')

# 3. 寫入 (Binary)
with open(html_path, 'wb') as f:
    f.write(html_top)
    f.write(json_bytes)
    f.write(html_bottom)

print("ITS_Database 重建完成。")
