import json
import os
import sys

def create_html(json_file, output_html):
    # Derive title from filename
    base_name = os.path.splitext(os.path.basename(output_html))[0]
    display_title = base_name.replace('_', ' ')
    if not display_title:
        display_title = "ITS Exam"

    # Derive generic storage key base from filename
    # e.g. "ITS_Python.html" -> "its_python"
    storage_base = base_name.lower().replace(' ', '_')
    
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
    <title>{display_title} 模擬測驗</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Prism.js -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-solarized-light.min.css" rel="stylesheet" />
    <style>
        body {{
            background-color: #f8f9fa;
            font-family: "Microsoft JhengHei", "Segoe UI", Roboto, sans-serif;
            overflow-y: scroll;
        }}
        .main-wrapper {{ display: flex; min-height: 100vh; }}
        .sidebar {{
            width: 280px; background: #fff; border-right: 1px solid #dee2e6;
            display: flex; flex-direction: column; position: fixed;
            top: 0; bottom: 0; left: 0; z-index: 1000; transition: transform 0.3s ease;
        }}
        .sidebar-header {{ padding: 15px; border-bottom: 1px solid #dee2e6; background: #212529; color: #fff; }}
        .sidebar-content {{ flex: 1; overflow-y: auto; padding: 15px; }}
        .sidebar-footer {{ padding: 15px; border-top: 1px solid #dee2e6; background: #f8f9fa; }}
        .content-area {{ flex: 1; margin-left: 280px; padding: 30px; transition: margin-left 0.3s ease; }}
        @media (max-width: 992px) {{
            .sidebar {{ transform: translateX(-100%); }}
            .sidebar.active {{ transform: translateX(0); }}
            .content-area {{ margin-left: 0; }}
            .mobile-toggle {{ display: block !important; }}
        }}
        .question-card {{
            min-height: 400px; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            background: #fff; border-radius: 6px; overflow: hidden;
        }}
        .question-header {{
            background-color: #fff; border-bottom: 2px solid #0d6efd; padding: 20px;
            font-weight: bold; color: #0d6efd; display: flex; justify-content: space-between; align-items: center;
        }}
        .question-body {{ padding: 15px 25px 10px 25px; font-size: 1rem; }}
        .question-image {{ max-width: 100%; height: auto; margin: 15px 0; border: 1px solid #ddd; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .option-item {{ list-style: none; margin-bottom: 5px; padding: 5px 12px; border: 1px solid #e9ecef;
            border-radius: 6px; cursor: pointer; transition: all 0.2s;
        }}
        .option-item:hover {{ background-color: #f8f9fa; border-color: #adb5bd; }}
        .option-item.correct {{ background-color: #d1e7dd !important; border-color: #badbcc !important; color: #0f5132 !important; }}
        .option-item.incorrect {{ background-color: #f8d7da !important; border-color: #f5c2c7 !important; color: #842029 !important; }}
        .sub-opt-container.correct {{ background-color: #d1e7dd !important; border-color: #badbcc !important; }}
        .sub-opt-container.incorrect {{ background-color: #f8d7da !important; border-color: #f5c2c7 !important; }}
        .sub-question-label {{ font-weight: bold; margin-top: 15px; margin-bottom: 8px; color: #495057; border-left: 4px solid #198754; padding-left: 10px; font-size: 1.05rem; }}
        .answer-section {{ display: none; margin-top: 12px; padding: 10px 15px 5px 15px; background-color: #f0f7ff;
            border-left: 5px solid #0d6efd; border-radius: 6px;
        }}
        .progress-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }}
        .q-node {{
            aspect-ratio: 1; display: flex; align-items: center; justify-content: center;
            border: 1px solid #dee2e6; border-radius: 6px; background-color: #fff;
            cursor: pointer; font-size: 0.85rem; color: #6c757d;
        }}
        .q-node:hover {{ background-color: #e9ecef; }}
        /* Colors for Grid */
        .q-node.correct {{ background-color: #d1e7dd; border-color: #badbcc; color: #0f5132; }}
        .q-node.incorrect {{ background-color: #f8d7da; border-color: #f5c2c7; color: #842029; }}
        .q-node.active {{
            background-color: #0d6efd; color: white; border-color: #0d6efd;
            font-weight: bold; transform: scale(1.1); box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        .nav-btn-group {{ display: flex; gap: 15px; margin-top: 15px; justify-content: center; }}
        .nav-btn {{ min-width: 180px; }}
        .mobile-toggle {{
            display: none; position: fixed; bottom: 20px; right: 20px; z-index: 1100;
            width: 50px; height: 50px; border-radius: 50%; background: #212529;
            color: white; border: none; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}
        .home-float-btn {{
            position: fixed; bottom: 85px; right: 20px; z-index: 1090;
            width: 50px; height: 50px; border-radius: 50%; background: #0d6efd;
            color: white !important; display: flex; align-items: center; justify-content: center;
            text-decoration: none !important; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: transform 0.2s, background 0.3s; font-size: 1.5rem; border: 2px solid #fff;
        }}
        .home-float-btn:hover {{ background: #0a58ca; transform: scale(1.1); color: white !important; }}
        code {{ font-family: Consolas, Monaco, monospace; color: #d63384; background-color: #f8f9fa; padding: 2px 4px; border-radius: 6px; }}
        .explanation {{ font-size: 1rem; margin: 0; }}
    </style>
</head>
<body>

<div class="main-wrapper">
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header d-flex justify-content-between align-items-center">
            <a href="../index.html" class="text-decoration-none text-white me-2" title="回首頁">🏠</a><h5 class="m-0">題目列表</h5>
            <small class="text-white-50" id="progress-stats">0/{len(data)}</small>
        </div>
        <div class="sidebar-content">
            <div class="d-flex justify-content-between small mb-2 text-muted">
                <span><span style="display:inline-block;width:10px;height:10px;background:#fff;border:1px solid #ccc"></span> 未讀</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#d1e7dd;border:1px solid #badbcc"></span> 答對</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#f8d7da;border:1px solid #f5c2c7"></span> 答錯</span>
            </div>
            <div class="progress-grid" id="progress-grid"></div>
        </div>
        <div class="sidebar-footer">
            <button class="btn btn-outline-danger btn-sm w-100" onclick="resetProgress()">🗑️ 重置進度</button>
        </div>
    </nav>
    <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>
    <a href="../../index.html" class="home-float-btn no-print">🏠</a>
    <main class="content-area" id="main-content">
        <div class="container-fluid" style="max-width: 1000px;">
            <h2 class="text-center mb-4">{display_title} 模擬測驗</h2>
            <div id="question-container"></div>
            <div class="nav-btn-group">
                <button class="btn btn-secondary nav-btn" id="btn-prev" onclick="prevQuestion()">⬅️ 上一題</button>
                <button class="btn btn-primary nav-btn" id="btn-next" onclick="nextQuestion()">下一題 ➡️</button>
            </div>
        </div>
    </main>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>

<script>
    const quizData = {json_str};
    let currentIndex = 0;
    let correctSet = new Set();
    let incorrectSet = new Set();
    let userAnswers = {{}}; // Store user choices: {{ questionIndex: choice }}
    
    // Dynamic keys
    const CORR_KEY = '{storage_base}_correct_v1';
    const INCORR_KEY = '{storage_base}_incorrect_v1';
    const INDEX_KEY = '{storage_base}_index_v1';
    const ANSWERS_KEY = '{storage_base}_answers_v1';

    const typeMapping = {{ 'single': '單選題', 'multiple': '複選題', 'multioption': '題組' }};

    function loadState() {{
        const savedCorr = localStorage.getItem(CORR_KEY);
        if (savedCorr) correctSet = new Set(JSON.parse(savedCorr));
        
        const savedIncorr = localStorage.getItem(INCORR_KEY);
        if (savedIncorr) incorrectSet = new Set(JSON.parse(savedIncorr));

        const savedIndex = localStorage.getItem(INDEX_KEY);
        if (savedIndex !== null) {{
            currentIndex = parseInt(savedIndex, 10);
            if (isNaN(currentIndex) || currentIndex < 0 || currentIndex >= quizData.length) currentIndex = 0;
        }}

        const savedAns = localStorage.getItem(ANSWERS_KEY);
        if (savedAns) userAnswers = JSON.parse(savedAns);
    }}

    function saveState() {{
        localStorage.setItem(CORR_KEY, JSON.stringify([...correctSet]));
        localStorage.setItem(INCORR_KEY, JSON.stringify([...incorrectSet]));
        localStorage.setItem(INDEX_KEY, currentIndex.toString());
        localStorage.setItem(ANSWERS_KEY, JSON.stringify(userAnswers));
    }}

    function resetProgress() {{
        if(confirm('確定要清除所有紀錄嗎？')) {{
            localStorage.removeItem(CORR_KEY);
            localStorage.removeItem(INCORR_KEY);
            localStorage.removeItem(INDEX_KEY);
            localStorage.removeItem(ANSWERS_KEY);
            location.reload();
        }}
    }}

    function toggleSidebar() {{ document.getElementById('sidebar').classList.toggle('active'); }}
    document.addEventListener('click', function(e) {{
        const sidebar = document.getElementById('sidebar');
        const toggle = document.querySelector('.mobile-toggle');
        if (sidebar && sidebar.classList.contains('active') && !sidebar.contains(e.target) && !toggle.contains(e.target)) {{
            sidebar.classList.remove('active');
        }
    }});

    function checkAnswer(element, qIdx, optIdx, event) {{
        const item = quizData[qIdx];
        const isMultiple = item.type === 'multiple';
        let answers = item.answer;
        if (!Array.isArray(answers)) answers = [answers];
        const correctIndices = answers.map(a => parseInt(a) - 1);
        const input = element.querySelector('input');

        if (event && event.target !== input) {{
            if (isMultiple) input.checked = !input.checked;
            else input.checked = true;
        }}

        // Record User Answer
        if (isMultiple) {{
            // For multiple, we store an array of selected indices
            const inputs = document.querySelectorAll(`input[name="q${{qIdx}}"]`);
            let selected = [];
            inputs.forEach((inp, idx) => {{ if (inp.checked) selected.push(idx); }});
            userAnswers[qIdx] = selected;
        }} else {{
            // For single, store the index
            userAnswers[qIdx] = optIdx;
        }}
        saveState();

        if (!isMultiple) {{
            if (item.answered) return;
            item.answered = true;
            document.querySelectorAll(`input[name="q${{qIdx}}"]`).forEach(i => i.disabled = true);

            if (correctIndices.includes(optIdx)) {{
                element.classList.add('correct');
                correctSet.add(qIdx);
                incorrectSet.delete(qIdx);
            }} else {{
                element.classList.add('incorrect');
                incorrectSet.add(qIdx);
                correctSet.delete(qIdx);
                const correctInput = document.querySelector(`input[name="q${{qIdx}}"][id="o${{correctIndices[0]}}"]`);
                if (correctInput) correctInput.closest('.option-item').classList.add('correct');
            }}
            saveState();
            document.getElementById('ans-section').style.display = 'block';
            updateUI();
        }} else {{
            // For multiple choice, we update UI dynamically but only finalize when correct?
            // Actually, existing logic checks correctness immediately on click?
            // No, the previous logic was: if (input.checked) check correctness.
            // Let's keep the existing visual logic:
            
            if (input.checked) {{
                if (correctIndices.includes(optIdx)) {{
                    element.classList.add('correct');
                    element.classList.remove('incorrect');
                }} else {{
                    element.classList.add('incorrect');
                    element.classList.remove('correct');
                }}
            }} else {{
                element.classList.remove('correct');
                element.classList.remove('incorrect');
            }}

            // Check overall status for Multiple Choice
            const allOptions = document.querySelectorAll(`input[name="q${{qIdx}}"]`);
            let allCorrect = true;
            let anyWrong = false;

            allOptions.forEach((inp, idx) => {{
                if (inp.checked) {{
                    if (!correctIndices.includes(idx)) {{
                        anyWrong = true; // Selected a wrong one
                        allCorrect = false;
                    }}
                }} else {{
                    if (correctIndices.includes(idx)) {{
                        allCorrect = false; // Missed a correct one
                    }}
                }}
            }});

            if (allCorrect) {{
                correctSet.add(qIdx);
                incorrectSet.delete(qIdx);
                document.getElementById('ans-section').style.display = 'block';
            }} else {{
                correctSet.delete(qIdx);
                if (anyWrong) {{
                     incorrectSet.add(qIdx);
                }}
            }}
            saveState();
            updateUI();
        }}
    }}

    function checkSubAnswer(element, qIdx, optIdx, subIdx, event) {{
        const item = quizData[qIdx];
        let answers = item.answer;
        if (!Array.isArray(answers)) answers = [answers];
        const correctSubIdx = parseInt(answers[optIdx]) - 1;
        const input = element.querySelector('input');

        if (event && event.target !== input) input.checked = true;
        
        // Record User Answer for Sub-Question
        if (!userAnswers[qIdx]) userAnswers[qIdx] = {{}};
        userAnswers[qIdx][optIdx] = subIdx;
        saveState();

        if (element.classList.contains('correct') || element.classList.contains('incorrect')) return;

        document.querySelectorAll(`input[name="q${{qIdx}}_opt${{optIdx}}"]`).forEach(i => i.disabled = true);

        if (subIdx === correctSubIdx) {{
            element.classList.add('correct');
            const totalSub = (quizData[qIdx].quiz || quizData[qIdx].options || []).length;
            const currentCorrect = document.querySelectorAll('.sub-opt-container.correct').length;
            if (currentCorrect === totalSub) {{
                correctSet.add(qIdx);
                incorrectSet.delete(qIdx);
                saveState();
                updateUI();
                document.getElementById('ans-section').style.display = 'block';
            }}
        }} else {{
            element.classList.add('incorrect');
            const correctInput = document.getElementById(`o${{optIdx}}_s${{correctSubIdx}}`);
            if (correctInput) correctInput.parentElement.classList.add('correct');
            incorrectSet.add(qIdx);
            correctSet.delete(qIdx);
            saveState();
            updateUI();
        }}
    }}

    function renderQuestion(index) {{
        if (index < 0) index = 0;
        if (index >= quizData.length) index = quizData.length - 1;
        currentIndex = index;
        saveState();

        const item = quizData[index];
        const container = document.getElementById('question-container');
        container.innerHTML = '';
        
        const card = document.createElement('div');
        card.className = 'card question-card';
        const typeLabel = typeMapping[item.type] || '單選題';
        card.innerHTML += `
            <div class="question-header">
                <div>
                    <span class="fs-5 me-2">Question ${{index + 1}}</span>
                    <span class="badge bg-light text-dark border">${{typeLabel}}</span>
                </div>
                <div class="text-muted small">Total: ${{quizData.length}}</div>
            </div>
        `;
        
        const body = document.createElement('div');
        body.className = 'question-body';
        let qText = (item.question || '').replace(/●/g, '<br/>●').replace(/^<br\/>/, '');
        body.innerHTML += `<div class="mb-3">${{qText}}</div>`;
        if (item.image) body.innerHTML += `<div class="text-center mb-3"><img src="${{item.image}}" class="question-image" alt="Question Image"></div>`;
        
        const options = item.quiz || item.options || [];
        let optionsHtml = '<div class="mt-3">';
        let isComplex = options.some(opt => typeof opt === 'string' && opt.includes('|'));

        options.forEach((opt, optIdx) => {{
            const optStr = String(opt);
            if (optStr.includes('|')) {{
                const subOpts = optStr.split('|');
                optionsHtml += `<div class="sub-question-label">Quiz ${{optIdx + 1}}</div>`;
                optionsHtml += `<div class="d-flex flex-wrap gap-2 mb-3 ms-2">`;
                subOpts.forEach((sub, subIdx) => {{
                    optionsHtml += `
                        <div class="form-check form-check-inline p-1 border rounded bg-light sub-opt-container" onclick="checkSubAnswer(this, ${{index}}, ${{optIdx}}, ${{subIdx}}, event)">
                            <input class="form-check-input" type="radio" name="q${{index}}_opt${{optIdx}}" id="o${{optIdx}}_s${{subIdx}}">
                            <label class="form-check-label ms-1" style="cursor:pointer" for="o${{optIdx}}_s${{subIdx}}">(${{subIdx+1}}) ${{sub}}</label>
                        </div>`;
                }});
                optionsHtml += `</div>`;
            }} else {{
                optionsHtml += `
                    <div class="option-item" onclick="checkAnswer(this, ${{index}}, ${{optIdx}}, event)">
                        <div class="form-check">
                            <input class="form-check-input" type="${{item.type === 'multiple' ? 'checkbox' : 'radio'}}" 
                                   name="q${{index}}" id="o${{optIdx}}" style="transform: scale(1.1); margin-top: 0.2rem;">
                            <label class="form-check-label w-100 ps-2" for="o${{optIdx}}" style="cursor:pointer">${{optIdx + 1}}. ${{optStr}}</label>
                        </div>
                    </div>`;
            }}
        }});
        optionsHtml += '</div>';
        body.innerHTML += optionsHtml;

        const footer = document.createElement('div');
        footer.className = 'mt-4 pt-3 border-top text-center';
        const btn = document.createElement('button');
        btn.className = 'btn btn-outline-primary px-4';
        btn.innerHTML = '👁️ 顯示答案 / 解析';
        btn.onclick = () => {{
            const el = document.getElementById('ans-section');
            if(el.style.display === 'block') {{ el.style.display = 'none'; btn.classList.remove('active'); }}
            else {{ el.style.display = 'block'; btn.classList.add('active'); setTimeout(() => el.scrollIntoView({{behavior: 'smooth', block: 'nearest'}}), 100); }}
        }};
        footer.appendChild(btn);

        const answerDiv = document.createElement('div');
        answerDiv.id = 'ans-section';
        answerDiv.className = 'answer-section text-start';
        let ansDisplay = '';
        let answers = item.answer;
        if (!Array.isArray(answers)) answers = [answers];

        if (isComplex) {{
            let mappedAnswers = [];
            answers.forEach((ans, i) => {{
                if (i < options.length) {{
                    const optStr = String(options[i]);
                    if (optStr.includes('|')) {{
                        const subs = optStr.split('|');
                        const ansIdx = parseInt(ans) - 1;
                        if (subs[ansIdx]) mappedAnswers.push(`Quiz ${{i+1}}: <b>${{subs[ansIdx]}}</b>`);
                        else mappedAnswers.push(`Quiz ${{i+1}}: ${{ans}}`);
                    }} else mappedAnswers.push(`${{ans}}`);
                }}
            }});
            ansDisplay = mappedAnswers.join(', ');
        }} else ansDisplay = answers.join(', ');

        answerDiv.innerHTML = `
            <h6 class="mb-0 fw-bold">正確答案:</h6>
            <div class="alert alert-success fs-6 fw-bold mb-1 p-1">${{ansDisplay}}</div>
            <h6 class="mb-0 mt-1 fw-bold">解析:</h6>
            <div class="explanation">${{(item.explanation || '暫無解析。').replace(/●/g, '<br/>●').replace(/^<br\/>/, '')}}</div>
        `;
        footer.appendChild(answerDiv);
        body.appendChild(footer);
        card.appendChild(body);
        container.appendChild(card);

        // Restore User Answer State
        // Single/Multiple Choice
        const savedAns = userAnswers[index];
        const isMultiple = item.type === 'multiple';
        let correctIndices = answers.map(a => parseInt(a) - 1);

        // Check if question is already answered (completed)
        const isCompleted = correctSet.has(index) || incorrectSet.has(index);

        if (savedAns !== undefined) {{
            if (isComplex) {{
                // Quiz Type: savedAns is object {{ rowIdx: colIdx }}
                for (const [r, c] of Object.entries(savedAns)) {{
                    const rowIdx = parseInt(r);
                    const colIdx = parseInt(c);
                    const input = document.getElementById(`o${{rowIdx}}_s${{colIdx}}`);
                    if (input) {{
                        input.checked = true;
                        // Restore colors if completed
                        if (isCompleted) {{
                            const wrapper = input.closest('.sub-opt-container');
                            let correctSub = parseInt(answers[rowIdx]) - 1;
                            
                            if (colIdx === correctSub) {{
                                wrapper.classList.add('correct');
                            }} else {{
                                wrapper.classList.add('incorrect');
                                const corrInput = document.getElementById(`o${{rowIdx}}_s${{correctSub}}`);
                                if (corrInput) corrInput.closest('.sub-opt-container').classList.add('correct');
                            }}
                            // Disable inputs
                            document.querySelectorAll(`input[name="q${{index}}_opt${{rowIdx}}"]`).forEach(i => i.disabled = true);
                        }}
                    }}
                }}
            }} else if (isMultiple) {{
                // Array of indices
                if (Array.isArray(savedAns)) {{
                    savedAns.forEach(idx => {{
                        const input = document.querySelector(`input[name="q${{index}}"][id="o${{idx}}"]`);
                        if (input) {{
                            input.checked = true;
                            if (isCompleted) {{
                                const wrapper = input.closest('.option-item');
                                if (correctIndices.includes(idx)) wrapper.classList.add('correct');
                                else wrapper.classList.add('incorrect');
                            }}
                        }}
                    }});
                }}
            }} else {{
                // Single Index
                const input = document.querySelector(`input[name="q${{index}}"][id="o${{savedAns}}"]`);
                if (input) {{
                    input.checked = true;
                    if (isCompleted) {{
                        const wrapper = input.closest('.option-item');
                        if (correctIndices.includes(savedAns)) wrapper.classList.add('correct');
                        else wrapper.classList.add('incorrect');
                        
                        // Disable all
                        document.querySelectorAll(`input[name="q${{index}}"]`).forEach(i => i.disabled = true);
                    }}
                }}
            }}
        }}

        // If completed, always show answer section
        if (isCompleted) {{
            document.getElementById('ans-section').style.display = 'block';
             // Also ensure correct answers are highlighted for single/multiple if they weren't selected
            if (!isComplex && !isMultiple) {{
                 const correctInput = document.querySelector(`input[name="q${{index}}"][id="o${{correctIndices[0]}}"]`);
                 if (correctInput) correctInput.closest('.option-item').classList.add('correct');
            }}
        }}

        updateUI();
        Prism.highlightAll();
        if (window.innerWidth < 992) document.getElementById('sidebar').classList.remove('active');
    }}

    function nextQuestion() {{
        if (currentIndex < quizData.length - 1) {{ renderQuestion(currentIndex + 1); window.scrollTo(0, 0); }}
    }}
    function prevQuestion() {{
        if (currentIndex > 0) {{ renderQuestion(currentIndex - 1); window.scrollTo(0, 0); }}
    }}
    function jumpTo(index) {{ renderQuestion(index); }}

    function updateUI() {{
        document.getElementById('btn-prev').disabled = (currentIndex === 0);
        document.getElementById('btn-next').disabled = (currentIndex === quizData.length - 1);
        document.getElementById('progress-stats').innerText = `答對:${{correctSet.size}} 答錯:${{incorrectSet.size}} / 共:${{quizData.length}}`;

        const grid = document.getElementById('progress-grid');
        if (grid.children.length !== quizData.length) {{
            grid.innerHTML = '';
            quizData.forEach((_, idx) => {{
                const node = document.createElement('div');
                node.className = 'q-node';
                node.innerText = idx + 1;
                node.onclick = () => jumpTo(idx);
                node.id = `node-${{idx}}`;
                grid.appendChild(node);
            }});
        }}

        for (let i = 0; i < quizData.length; i++) {{
            const node = document.getElementById(`node-${{i}}`);
            if (node) {{
                node.className = 'q-node';
                if (i === currentIndex) node.classList.add('active');
                else if (incorrectSet.has(i)) node.classList.add('incorrect');
                else if (correctSet.has(i)) node.classList.add('correct');
            }}
        }}
    }}

    loadState();
    renderQuestion(currentIndex);
</script>
</body>
</html>"""
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully created {output_html}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        create_html(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        input_json = sys.argv[1]
        output_name = os.path.basename(input_json).replace('.json', '.html')
        output_name = output_name.replace('questions_', '')
        create_html(input_json, output_name)
    else:
        create_html('questions_Generative_AI_Foundations.json', 'Generative_AI.html')