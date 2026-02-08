import json
import re
import os

# 1. 定義分類特徵關鍵字 (完全對應官方 Domain)
def get_domain(text):
    text = text.lower()
    rules = {
        'D1_資料型別與運算子': ['type(', 'str', 'float', 'int', 'bool', 'list', 'slice', '索引', '切片', '優先順序', '**', '//', ' % ', ' is ', ' in ', 'ord(', 'chr('],
        'D2_流程控制': ['if ', 'elif', 'else', 'while', 'for ', 'break', 'continue', 'range', '迴圈', 'nested'],
        'D3_輸入與輸出': ['input', 'print', 'format', 'f-string', 'open(', 'read', 'write', 'file', '檔案'],
        'D4_程式碼文件與結構': ['def ', 'return', 'class', 'docstring', '註解', 'argument', '參數', 'pass'],
        'D5_錯誤處理與測試': ['try', 'except', 'raise', 'error', 'test', 'assert', 'unittest', '除錯'],
        'D6_模組與工具': ['import', 'math', 'random', 'datetime', 'os.', 'sys.', 'time.'],
        'D7_進階題(APCS/演算法)': ['演算法', 'apcs', 'stack', 'queue', '堆疊', '佇列', '遞迴']
    }
    for domain, keywords in rules.items():
        for kw in keywords:
            if kw in text: return domain
    return 'D1_資料型別與運算子'

# 2. 完整的考試系統 JavaScript (包含占比統計版)
CORE_EXAM_JS = r"""
    let examQuestions = [];
    let currentIndex = 0;
    let userAnswers = {}; 
    let timeLeft = 50 * 60; 
    let timerInterval;

    const baseBlueprint = {
        'D1_資料型別與運算子': 10,
        'D2_流程控制': 12,
        'D3_輸入與輸出': 8,
        'D4_程式碼文件與結構': 6,
        'D5_錯誤處理與測試': 2,
        'D6_模組與工具': 2
    };

    const MAX_CAPS = {
        'D1_資料型別與運算子': 13, // 25%
        'D2_流程控制': 16,        // 32%
        'D3_輸入與輸出': 12,       // 24%
        'D4_程式碼文件與結構': 10,  // 20%
        'D5_錯誤處理與測試': 5,
        'D6_模組與工具': 5
    };

    function saveWeaknessStats(stats) {
        localStorage.setItem('its_python_stats', JSON.stringify(stats));
    }

    function loadWeaknessStats() {
        const data = localStorage.getItem('its_python_stats');
        return data ? JSON.parse(data) : null;
    }

    function startExam() {
        let selectedQuestions = [];
        let currentBlueprint = { ...baseBlueprint };
        
        const history = loadWeaknessStats();
        if (history) {
            let weakDomains = [];
            for (let [domain, stats] of Object.entries(history)) {
                let rate = stats.total > 0 ? (stats.correct / stats.total) : 1;
                if (rate < 0.6 && domain !== 'D1_資料型別與運算子' && domain !== 'D7_進階題(APCS/演算法)') {
                    weakDomains.push(domain);
                }
            }
            weakDomains.forEach(d => {
                if (currentBlueprint[d] < MAX_CAPS[d]) {
                    currentBlueprint[d] += 2;
                    currentBlueprint['D1_資料型別與運算子'] = Math.max(5, currentBlueprint['D1_資料型別與運算子'] - 2);
                }
            });
        }

        const getCount = (cat) => selectedQuestions.filter(q => q.category === cat).length;

        // --- 1. 核心抽取 ---
        for (let [cat, count] of Object.entries(currentBlueprint)) {
            let pool = allQuestions.filter(q => q.id < 89 && q.category === cat).sort(() => 0.5 - Math.random());
            selectedQuestions.push(...pool.slice(0, count));
        }

        // --- 2. 補充抽取 ---
        let suppPool = allQuestions.filter(q => q.id >= 89).sort(() => 0.5 - Math.random());
        for (let q of suppPool) {
            if (selectedQuestions.length >= 50) break;
            if (MAX_CAPS[q.category] && getCount(q.category) >= MAX_CAPS[q.category]) continue;
            selectedQuestions.push(q);
        }

        // --- 3. 補足名額 ---
        if (selectedQuestions.length < 50) {
            let usedIds = new Set(selectedQuestions.map(q => q.id));
            let remainPool = allQuestions.filter(q => !usedIds.has(q.id)).sort(() => 0.5 - Math.random());
            for (let q of remainPool) {
                if (selectedQuestions.length >= 50) break;
                if (MAX_CAPS[q.category] && getCount(q.category) >= MAX_CAPS[q.category]) continue;
                selectedQuestions.push(q);
            }
        }

        // --- 4. 強制平衡檢核 ---
        while (getCount('D1_資料型別與運算子') > MAX_CAPS['D1_資料型別與運算子']) {
            let idx = selectedQuestions.findIndex(q => q.category === 'D1_資料型別與運算子');
            selectedQuestions.splice(idx, 1);
            let usedIds = new Set(selectedQuestions.map(q => q.id));
            let backup = allQuestions.find(q => !usedIds.has(q.id) && q.category !== 'D1_資料型別與運算子');
            if (backup) selectedQuestions.push(backup);
        }

        // --- 5. 輸出統計到控制台 (包含占比) ---
        console.log("%c=== 官方藍圖比例檢查 (總數: " + selectedQuestions.length + " 題) ===", "color: blue; font-weight: bold;");
        let counts = selectedQuestions.reduce((a,q)=>{a[q.category]=(a[q.category]||0)+1; return a;}, {});
        let statsWithPercent = {};
        for (let cat in counts) {
            let count = counts[cat];
            let percent = Math.round((count / selectedQuestions.length) * 100) + "%";
            statsWithPercent[cat] = { "題數": count, "占比": percent };
        }
        console.table(statsWithPercent);

        examQuestions = selectedQuestions.sort(() => 0.5 - Math.random());
        renderQuestion(0);
        startTimer();
    }

    function startTimer() {
        if(timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            timeLeft--;
            let mins = Math.floor(timeLeft / 60);
            let secs = timeLeft % 60;
            document.getElementById('timer').innerText = mins + ":" + secs.toString().padStart(2, '0');
            if (timeLeft <= 0) { alert("時間到！系統自動交卷。"); submitExam(); }
        }, 1000);
    }

    function renderQuestion(index) {
        currentIndex = index;
        const item = examQuestions[index];
        const container = document.getElementById('question-area');
        document.getElementById('q-progress').innerText = "題目 " + (index + 1) + " / 50";
        document.getElementById('btn-prev').disabled = index === 0;
        document.getElementById('btn-next').innerText = index === 49 ? '完成答題 (交卷)' : '下一題 ➡️';

        let qText = item.question.replace(/●/g, '<br/>●').replace(/^\d+\.\s*/, '');
        let html = '<div class="card question-card"><div class="question-header">Question ' + (index + 1) + ' / 50 <span class="badge bg-light text-dark float-end">' + (item.category || '') + '</span></div><div class="question-body"><div class="mb-4">' + qText + '</div>';
        if (item.image) html += '<div class="text-center mb-4"><img src="' + item.image + '" style="max-width:100%; border:1px solid #ddd; border-radius:4px;"></div>';
        
        const options = item.quiz || item.options || [];
        const savedAns = userAnswers[index];
        html += '<div class="mt-3">';
        options.forEach((opt, optIdx) => {
            const optStr = String(opt);
            if (optStr.includes('|')) {
                const subOpts = optStr.split('|');
                html += '<div class="sub-question-label">子題目 ' + (optIdx + 1) + '</div><div class="d-flex flex-wrap gap-2 mb-3 ms-2">';
                subOpts.forEach((sub, subIdx) => {
                    const isSel = (savedAns && savedAns[optIdx] === subIdx);
                    html += '<div class="sub-opt-container ' + (isSel ? 'selected' : '') + '" onclick="selectSub(' + optIdx + ', ' + subIdx + ')">(' + (subIdx+1) + ') ' + sub + '</div>';
                });
                html += '</div>';
            } else {
                const isSel = Array.isArray(savedAns) ? savedAns.includes(optIdx) : savedAns === optIdx;
                html += '<div class="option-item ' + (isSel ? 'selected' : '') + '" onclick="selectOption(' + optIdx + ')">' + (optIdx + 1) + '. ' + optStr + '</div>';
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

    function submitExam() {
        clearInterval(timerInterval);
        let correctCount = 0;
        let catStats = {};
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
        });
        document.getElementById('exam-ui').style.display = 'none';
        document.getElementById('result-screen').style.display = 'block';
        document.getElementById('correct-count').innerText = correctCount;
        document.getElementById('final-score').innerText = Math.round((correctCount / 50) * 100);
        showWeaknessAnalysis(catStats);
    }

    function showWeaknessAnalysis(stats) {
        saveWeaknessStats(stats);
        let html = '<div class="card mt-4 shadow-sm"><div class="card-header bg-dark text-white fw-bold">各領域表現分析</div><div class="card-body p-0"><table class="table table-hover m-0"><thead><tr><th>領域</th><th>題數</th><th>答對</th><th>率</th></tr></thead><tbody>';
        for (let [domain, data] of Object.entries(stats)) {
            let rate = Math.round((data.correct / data.total) * 100);
            html += '<tr><td>' + domain + '</td><td>' + data.total + '</td><td>' + data.correct + '</td><td>' + rate + '%</td></tr>';
        }
        html += '</tbody></table></div></div>';
        document.getElementById('weakness-analysis').innerHTML = html;
    }

    window.onload = () => { if(typeof allQuestions !== 'undefined') startExam(); };
"""

def generate_balanced_exam():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'questions_ITS_python.json')
    html_path = os.path.join(base_dir, 'mock_exam.html')
    js_data_path = os.path.join(base_dir, 'questions_data.js')

    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    for q in questions:
        content = (q.get('question', '') + str(q.get('explanation', ''))).lower()
        q['category'] = get_domain(content)

    with open(js_data_path, 'w', encoding='utf-8') as f:
        f.write('const allQuestions = ' + json.dumps(questions, ensure_ascii=False) + ';')

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    start_tag = "/* JS_LOGIC_START */"
    end_tag = "/* JS_LOGIC_END */"
    
    if start_tag in html_content and end_tag in html_content:
        parts = html_content.split(start_tag)
        top = parts[0]
        bottom = parts[1].split(end_tag)[1]
        new_html = top + start_tag + CORE_EXAM_JS + end_tag + bottom
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"Success! Console stats now include Percentage column.")
    else:
        print("Error: Tags not found in HTML.")

if __name__ == "__main__":
    generate_balanced_exam()
