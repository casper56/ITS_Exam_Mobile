import json
import re
import os

# 1. 定義分類特徵關鍵字 (與 Domain 對應)
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

# 2. 定義出題藍圖與結果分析 JavaScript
BLUEPRINT_JS = """
    // === 自動平衡出題與弱點分析系統 ===
    const blueprint = {
        'D1_資料型別與運算子': 12,
        'D2_流程控制': 10,
        'D3_輸入與輸出': 8,
        'D4_程式碼文件與結構': 8,
        'D5_錯誤處理與測試': 6,
        'D6_模組與工具': 6,
        'D7_進階題(APCS/演算法)': 0 // 若題庫中有 D7，會自動補足
    };

    function startExam() {
        let selectedQuestions = [];
        let buckets = {};
        allQuestions.forEach(q => {
            let cat = q.category || 'D1_資料型別與運算子';
            if (!buckets[cat]) buckets[cat] = [];
            buckets[cat].push(q);
        });

        for (let [cat, count] of Object.entries(blueprint)) {
            if (buckets[cat] && buckets[cat].length > 0) {
                let shuffled = buckets[cat].sort(() => 0.5 - Math.random());
                selectedQuestions.push(...shuffled.slice(0, count));
            }
        }

        if (selectedQuestions.length < 50) {
            let usedIds = new Set(selectedQuestions.map(q => q.id));
            let remaining = allQuestions.filter(q => !usedIds.has(q.id));
            let need = 50 - selectedQuestions.length;
            selectedQuestions.push(...remaining.sort(() => 0.5 - Math.random()).slice(0, need));
        }

        examQuestions = selectedQuestions.sort(() => 0.5 - Math.random());
        renderQuestion(0);
        startTimer();
    }

    function showWeaknessAnalysis(stats) {
        let html = `
            <div class="card mt-4 shadow-sm">
                <div class="card-header bg-dark text-white fw-bold">各領域表現分析 (Weakness Analysis)</div>
                <div class="card-body p-0">
                    <table class="table table-hover m-0" style="font-size: 0.9rem;">
                        <thead class="table-light">
                            <tr>
                                <th>知識領域 (Domain)</th>
                                <th class="text-center">題數</th>
                                <th class="text-center">答對</th>
                                <th class="text-center">答對率</th>
                            </tr>
                        </thead>
                        <tbody>`;
        
        for (let [domain, data] of Object.entries(stats)) {
            let rate = Math.round((data.correct / data.total) * 100);
            let colorClass = rate >= 80 ? 'text-success' : (rate >= 60 ? 'text-warning' : 'text-danger');
            html += `
                <tr>
                    <td>${domain}</td>
                    <td class="text-center">${data.total}</td>
                    <td class="text-center">${data.correct}</td>
                    <td class="text-center fw-bold ${colorClass}">${rate}%</td>
                </tr>`;
        }
        html += '</tbody></table></div></div>';
        document.getElementById('weakness-analysis').innerHTML = html;
    }
"""

def generate_balanced_exam():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'questions_ITS_python.json')
    html_path = os.path.join(base_dir, 'mock_exam.html')

    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    for q in questions:
        content = (q.get('question', '') + str(q.get('explanation', ''))).lower()
        q['category'] = get_domain(content)

    json_str = json.dumps(questions, ensure_ascii=False)

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 1. 注入題目資料
    new_html = re.sub(r'const allQuestions = \[.*?\];', f'const allQuestions = {json_str};', html_content, flags=re.DOTALL)

    # 2. 注入弱點分析容器 UI
    if 'id="weakness-analysis"' not in new_html:
        new_html = new_html.replace('<div id="result-msg" class="mb-4"></div>', 
                                   '<div id="result-msg" class="mb-4"></div>\n    <div id="weakness-analysis" class="mb-4 text-start"></div>')

    # 3. 更新 startExam 邏輯 (包含分析函式)
    new_html = re.sub(r'function startExam\(\)\s*\{[\s\S]*?startTimer\(\);\s*\}', '', new_html)
    if 'function showWeaknessAnalysis' not in new_html:
        new_html = new_html.replace('let timerInterval;', 'let timerInterval;' + BLUEPRINT_JS)

    # 4. 修改 submitExam 呼叫分析
    # 尋找 submitExam 內部的計算邏輯並植入統計
    analysis_logic = """
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
            } else {
                isCorrect = userAns === (parseInt(item.answer) - 1);
            }
            if (isCorrect) { catStats[cat].correct++; correctCount++; }
            else {
    """
    # 替換掉原本 submitExam 中的簡單 correctCount++ 邏輯
    # 注意：這裡的正則替換需要精確匹配
    new_html = re.sub(r'examQuestions\.forEach\(\(item, idx\) => \{[\s\S]*?if \(isCorrect\) \{[\s\S]*?correctCount\+\+;[\s\S]*?\} else \{', 
                      'examQuestions.forEach((item, idx) => {' + analysis_logic, new_html)
    
    # 在 submitExam 結尾前呼叫 showWeaknessAnalysis(catStats);
    if 'showWeaknessAnalysis(catStats);' not in new_html:
        new_html = new_html.replace("document.getElementById('final-score').innerText = score;", 
                                   "document.getElementById('final-score').innerText = score;\n        showWeaknessAnalysis(catStats);")

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"Success! Balanced Exam & Analysis Table updated in {html_path}.")

if __name__ == "__main__":
    generate_balanced_exam()
