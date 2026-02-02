import json
import os

def create_html(json_file, output_html):
    # Derive title from filename (e.g., "ITS_Database.html" -> "ITS Database")
    base_name = os.path.splitext(os.path.basename(output_html))[0]
    display_title = base_name.replace('_', ' ')
    if not display_title:
        display_title = "ITS Exam"

    # Load JSON data
    try:
        with open(json_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file {json_file}: {e}")
        return

    # Serialize data for embedding in JS
    json_str = json.dumps(data, ensure_ascii=False)

    # Create unique keys based on the filename
    safe_name = os.path.splitext(os.path.basename(output_html))[0].lower().replace(' ', '_').replace('-', '_')
    storage_key = f"{safe_name}_visited_v1"
    index_key = f"{safe_name}_current_idx_v1"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title} 模擬測驗</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Prism.js for Syntax Highlighting -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
    <style>
        body {{
            background-color: #f8f9fa;
            font-family: "Microsoft JhengHei", "Segoe UI", Roboto, sans-serif;
            overflow-y: scroll; /* Always show scrollbar to prevent shift */
        }}
        
        /* Layout */
        .main-wrapper {{
            display: flex;
            min-height: 100vh;
        }}
        
        /* Sidebar */
        .sidebar {{
            width: 280px;
            background: #fff;
            border-right: 1px solid #dee2e6;
            display: flex;
            flex-direction: column;
            position: fixed;
            top: 0;
            bottom: 0;
            left: 0;
            z-index: 1000;
            transition: transform 0.3s ease;
        }}
        
        .sidebar-header {{
            padding: 15px;
            border-bottom: 1px solid #dee2e6;
            background: #212529;
            color: #fff;
        }}
        
        .sidebar-content {{
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }}
        
        .sidebar-footer {{
            padding: 15px;
            border-top: 1px solid #dee2e6;
            background: #f8f9fa;
        }}

        /* Main Content */
        .content-area {{
            flex: 1;
            margin-left: 280px; /* Match sidebar width */
            padding: 30px;
            transition: margin-left 0.3s ease;
        }}

        /* Mobile Responsive */
        @media (max-width: 992px) {{
            .sidebar {{
                transform: translateX(-100%);
            }}
            .sidebar.active {{
                transform: translateX(0);
            }}
            .content-area {{
                margin-left: 0;
            }}
            .mobile-toggle {{
                display: block !important;
            }}
        }}

        /* Question Card */
        .question-card {{
            min-height: 500px;
            border: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            background: #fff;
            border-radius: 8px;
            overflow: hidden;
        }}
        .question-header {{
            background-color: #fff;
            border-bottom: 2px solid #0d6efd;
            padding: 20px;
            font-weight: bold;
            color: #0d6efd;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .question-body {{
            padding: 40px;
            font-size: 1.1rem;
        }}
        .question-image {{
            max-width: 100%;
            height: auto;
            margin: 15px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        /* Options */
        .option-item {{
            list-style: none;
            margin-bottom: 12px;
            padding: 15px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .option-item:hover {{
            background-color: #f8f9fa;
            border-color: #adb5bd;
        }}
        .option-item.correct {{
            background-color: #d1e7dd !important;
            border-color: #badbcc !important;
            color: #0f5132 !important;
        }}
        .option-item.incorrect {{
            background-color: #f8d7da !important;
            border-color: #f5c2c7 !important;
            color: #842029 !important;
        }}
        .sub-opt-container.correct {{
            background-color: #d1e7dd !important;
            border-color: #badbcc !important;
        }}
        .sub-opt-container.incorrect {{
            background-color: #f8d7da !important;
            border-color: #f5c2c7 !important;
        }}
        .sub-question-label {{
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #495057;
            border-left: 4px solid #198754;
            padding-left: 10px;
            font-size: 1.05rem;
        }}

        /* Answer Section */
        .answer-section {{
            display: none;
            margin-top: 30px;
            padding: 25px;
            background-color: #f0f7ff;
            border-left: 5px solid #0d6efd;
            border-radius: 4px;
        }}

        /* Grid Nodes */
        .progress-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 6px;
        }}
        .q-node {{
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            background-color: #fff;
            cursor: pointer;
            font-size: 0.85rem;
            color: #6c757d;
        }}
        .q-node:hover {{
            background-color: #e9ecef;
        }}
        .q-node.visited {{
            background-color: #d1e7dd;
            border-color: #badbcc;
            color: #0f5132;
        }}
        .q-node.active {{
            background-color: #0d6efd;
            color: white;
            border-color: #0d6efd;
            font-weight: bold;
            transform: scale(1.1);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}

        /* Navigation Buttons */
        .nav-btn-group {{
            display: flex;
            gap: 15px;
            margin-top: 30px;
            justify-content: center;
        }}
        .nav-btn {{
            min-width: 120px;
        }}

        .mobile-toggle {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1100;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: #212529;
            color: white;
            border: none;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}

        code {{
            font-family: Consolas, Monaco, monospace;
            color: #d63384;
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>

<div class="main-wrapper">
    <!-- Sidebar -->
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header d-flex justify-content-between align-items-center">
            <h5 class="m-0">題目列表</h5>
            <small class="text-white-50" id="progress-stats">0/{len(data)}</small>
        </div>
        
        <div class="sidebar-content">
            <div class="d-flex justify-content-between small mb-2 text-muted">
                <span><span style="display:inline-block;width:10px;height:10px;background:#fff;border:1px solid #ccc"></span> 未讀</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#d1e7dd;border:1px solid #badbcc"></span> 已讀</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#0d6efd"></span> 當前</span>
            </div>
            <div class="progress-grid" id="progress-grid">
                <!-- Grid items generated by JS -->
            </div>
        </div>

        <div class="sidebar-footer">
            <button class="btn btn-outline-danger btn-sm w-100" onclick="resetProgress()">
                🗑️ 重置進度
            </button>
        </div>
    </nav>

    <!-- Mobile Toggle -->
    <button class="mobile-toggle" onclick="toggleSidebar()">
        ☰
    </button>

    <!-- Main Content -->
    <main class="content-area" id="main-content">
        <div class="container-fluid" style="max-width: 1000px;">
            <h2 class="text-center mb-4">{display_title} 模擬測驗</h2>
            <div id="question-container">
                <!-- Question injected here -->
            </div>

            <div class="nav-btn-group">
                <button class="btn btn-secondary nav-btn" id="btn-prev" onclick="prevQuestion()">⬅️ 上一題</button>
                <button class="btn btn-primary nav-btn" id="btn-next" onclick="nextQuestion()">下一題 ➡️</button>
            </div>
        </div>
    </main>
</div>

<!-- Scripts -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>

<script>
    const quizData = {json_str};
    
    // State
    let currentIndex = 0;
    let visitedSet = new Set();
    const STORAGE_KEY = '{storage_key}';
    const INDEX_KEY = '{index_key}';

    const typeMapping = {{
        'single': '單選題',
        'multiple': '複選題',
        'multioption': '題組'
    }};

    function loadState() {{
        const savedVisited = localStorage.getItem(STORAGE_KEY);
        if (savedVisited) {{
            visitedSet = new Set(JSON.parse(savedVisited));
        }}
        const savedIndex = localStorage.getItem(INDEX_KEY);
        if (savedIndex !== null) {{
            currentIndex = parseInt(savedIndex, 10);
            if (isNaN(currentIndex) || currentIndex < 0 || currentIndex >= quizData.length) {{
                currentIndex = 0;
            }}
        }}
    }}

    function saveState() {{
        localStorage.setItem(STORAGE_KEY, JSON.stringify([...visitedSet]));
        localStorage.setItem(INDEX_KEY, currentIndex.toString());
    }}

    function resetProgress() {{
        if(confirm('確定要清除所有閱讀進度嗎？')) {{
            localStorage.removeItem(STORAGE_KEY);
            localStorage.removeItem(INDEX_KEY);
            location.reload();
        }}
    }}

    function toggleSidebar() {{
        document.getElementById('sidebar').classList.toggle('active');
    }}

    function checkAnswer(element, qIdx, optIdx, event) {{
        const item = quizData[qIdx];
        const isMultiple = item.type === 'multiple';
        let answers = item.answer;
        if (!Array.isArray(answers)) answers = [answers];
        const correctIndices = answers.map(a => parseInt(a) - 1);
        const input = element.querySelector('input');

        if (event && event.target !== input) {{
            // Clicked on div/label, manually toggle input
            if (isMultiple) {{
                input.checked = !input.checked;
            }} else {{
                input.checked = true;
            }}
        }}
        // If clicked on input directly, browser handles toggle.

        if (!isMultiple) {{
            // Single choice - prevent multiple clicks
            if (item.answered) return;
            item.answered = true;

            // Disable all inputs for this question
            const inputs = document.querySelectorAll(`input[name="q${{qIdx}}"]`);
            inputs.forEach(i => i.disabled = true);

            if (correctIndices.includes(optIdx)) {{
                element.classList.add('correct');
            }} else {{
                element.classList.add('incorrect');
                // Find and highlight correct one
                const correctInput = document.querySelector(`input[name="q${{qIdx}}"][id="o${{correctIndices[0]}}"]`);
                if (correctInput) correctInput.closest('.option-item').classList.add('correct');
            }}
            // Auto show answer section
            const el = document.getElementById('ans-section');
            el.style.display = 'block';
        }} else {{
            // Multiple choice - allow toggling and re-evaluating
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
        }}
    }}

    function checkSubAnswer(element, qIdx, optIdx, subIdx, event) {{
        const item = quizData[qIdx];
        let answers = item.answer;
        if (!Array.isArray(answers)) answers = [answers];
        const correctSubIdx = parseInt(answers[optIdx]) - 1;
        const input = element.querySelector('input');

        if (event && event.target !== input) {{
            input.checked = true;
        }}

        if (element.classList.contains('correct') || element.classList.contains('incorrect')) return;

        // Disable other radios in this sub-question group
        const inputs = document.querySelectorAll(`input[name="q${{qIdx}}_opt${{optIdx}}"]`);
        inputs.forEach(i => i.disabled = true);

        if (subIdx === correctSubIdx) {{
            element.classList.add('correct');
        }} else {{
            element.classList.add('incorrect');
            // Highlight correct one
            const correctInput = document.getElementById(`o${{optIdx}}_s${{correctSubIdx}}`);
            if (correctInput) correctInput.parentElement.classList.add('correct');
        }}
    }}

    function renderQuestion(index) {{
        if (index < 0) index = 0;
        if (index >= quizData.length) index = quizData.length - 1;
        currentIndex = index;

        visitedSet.add(index);
        saveState();

        const item = quizData[index];
        const container = document.getElementById('question-container');
        
        container.innerHTML = '';

        const card = document.createElement('div');
        card.className = 'card question-card';

        // Header
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

        // Body
        const body = document.createElement('div');
        body.className = 'question-body';
        
        let qText = (item.question || '').replace(/●/g, '<br/>●');
        body.innerHTML += `<div class="mb-4">${{qText}}</div>`;

        if (item.image) {{
            body.innerHTML += `<div class="text-center mb-4"><img src="${{item.image}}" class="question-image" alt="Question Image"></div>`;
        }}

        // Options
        const options = item.quiz || item.options || [];
        let optionsHtml = '<div class="mt-4">';
        let isComplex = options.some(opt => typeof opt === 'string' && opt.includes('|'));

        options.forEach((opt, optIdx) => {{
            const optStr = String(opt);
            
            if (optStr.includes('|')) {{
                const subOpts = optStr.split('|');
                optionsHtml += `<div class="sub-question-label">Quiz ${{optIdx + 1}}</div>`;
                optionsHtml += `<div class="d-flex flex-wrap gap-2 mb-3 ms-2">`;
                subOpts.forEach((sub, subIdx) => {{
                    optionsHtml += `
                        <div class="form-check form-check-inline p-2 border rounded bg-light sub-opt-container" onclick="checkSubAnswer(this, ${{index}}, ${{optIdx}}, ${{subIdx}}, event)">
                            <input class="form-check-input" type="radio" name="q${{index}}_opt${{optIdx}}" id="o${{optIdx}}_s${{subIdx}}">
                            <label class="form-check-label ms-1" style="cursor:pointer" for="o${{optIdx}}_s${{subIdx}}">
                                ${{subIdx+1}}. ${{sub}}
                            </label>
                        </div>
                    `;
                }});
                optionsHtml += `</div>`;
            }} else {{
                optionsHtml += `
                    <div class="option-item" onclick="checkAnswer(this, ${{index}}, ${{optIdx}}, event)">
                        <div class="form-check">
                            <input class="form-check-input" type="${{item.type === 'multiple' ? 'checkbox' : 'radio'}}" 
                                   name="q${{index}}" id="o${{optIdx}}" style="transform: scale(1.2); margin-top: 0.3rem;">
                            <label class="form-check-label w-100 ps-2" for="o${{optIdx}}" style="cursor:pointer">
                                ${{optIdx + 1}}. ${{optStr}}
                            </label>
                        </div>
                    </div>
                `;
            }}
        }});
        optionsHtml += '</div>';
        body.innerHTML += optionsHtml;

        // Footer Actions
        const footer = document.createElement('div');
        footer.className = 'mt-5 pt-4 border-top text-center';
        
        const btn = document.createElement('button');
        btn.className = 'btn btn-outline-primary px-4';
        btn.innerHTML = '👁️ 顯示答案 / 解析';
        btn.onclick = () => {{
            const el = document.getElementById('ans-section');
            if(el.style.display === 'block') {{
                el.style.display = 'none';
                btn.classList.remove('active');
            }} else {{
                el.style.display = 'block';
                btn.classList.add('active');
                // Scroll to answer if it's far down
                setTimeout(() => el.scrollIntoView({{behavior: 'smooth', block: 'nearest'}}), 100);
            }}
        }};
        footer.appendChild(btn);

        // Answer Section
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
                        if (subs[ansIdx]) {{
                            mappedAnswers.push(`Quiz ${{i+1}}: <b>${{subs[ansIdx]}}</b>`);
                        }} else {{
                            mappedAnswers.push(`Quiz ${{i+1}}: ${{ans}}`);
                        }}
                    }} else {{
                        mappedAnswers.push(`${{ans}}`);
                    }}
                }}
            }});
            ansDisplay = mappedAnswers.join(', ');
        }} else {{
            ansDisplay = answers.join(', ');
        }}

        answerDiv.innerHTML = `
            <h5 class="mb-3">正確答案:</h5>
            <div class="alert alert-success fs-5 fw-bold">${{ansDisplay}}</div>
            <h5 class="mb-3 mt-4">解析:</h5>
            <div class="explanation">${{(item.explanation || '暫無解析。').replace(/●/g, '<br/>●')}}</div>
        `;
        
        footer.appendChild(answerDiv);
        body.appendChild(footer);
        card.appendChild(body);
        container.appendChild(card);

        updateUI();
        Prism.highlightAll();
        
        // Auto-close sidebar on mobile after selection
        if (window.innerWidth < 992) {{
            document.getElementById('sidebar').classList.remove('active');
        }}
    }}

    function nextQuestion() {{
        if (currentIndex < quizData.length - 1) {{
            renderQuestion(currentIndex + 1);
            window.scrollTo(0, 0);
        }}
    }}

    function prevQuestion() {{
        if (currentIndex > 0) {{
            renderQuestion(currentIndex - 1);
            window.scrollTo(0, 0);
        }}
    }}
    
    function jumpTo(index) {{
        renderQuestion(index);
    }}

    function updateUI() {{
        // Update Buttons
        document.getElementById('btn-prev').disabled = (currentIndex === 0);
        document.getElementById('btn-next').disabled = (currentIndex === quizData.length - 1);
        
        // Update Sidebar Stats
        document.getElementById('progress-stats').innerText = `${{visitedSet.size}} / ${{quizData.length}}`;

        // Update Grid
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

        // Update Grid Classes
        for (let i = 0; i < quizData.length; i++) {{
            const node = document.getElementById(`node-${{i}}`);
            if (node) {{
                node.className = 'q-node';
                if (i === currentIndex) node.classList.add('active');
                else if (visitedSet.has(i)) node.classList.add('visited');
            }}
        }}
    }}

    // Init
    loadState();
    renderQuestion(currentIndex);

</script>
</body>
</html>"""

    try:
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully created {output_html}")
    except Exception as e:
        print(f"Error writing HTML file: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        create_html(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        # If only one arg, assume it is the input JSON and generate a default HTML name
        input_json = sys.argv[1]
        output_name = os.path.basename(input_json).replace('.json', '.html')
        # If output name is something like 'questions_ITS_python.html', clean it up
        output_name = output_name.replace('questions_', '')
        create_html(input_json, output_name)
    else:
        # Default fallback
        create_html('questions_ITS_python.json', 'ITS_Python.html')
