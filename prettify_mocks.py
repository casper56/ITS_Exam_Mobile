import os
import glob

# 黃金格式化版 JS (V3.4 絕對平衡版 + 修正 Typo)
def get_clean_js(cutoff, limit, wrong_key):
    return """
    const EXAM_LIMIT = """ + str(limit) + """, WRONG_KEY = '""" + wrong_key + """';
    let currentIndex = 0;
    let userAnswers = {};
    let timeLeft = 50 * 60;
    let timerInterval;
    const allQuestions = [];
    let examQuestions = []; // end_marker

    function initExam() {
        if (!allQuestions || allQuestions.length === 0) {
            console.error("題庫資料載入失敗！");
            return;
        }

        const CUTOFF = """ + str(cutoff) + """;
        const TARGET_OFF_COUNT = Math.floor(EXAM_LIMIT * 0.95);
        const MIN_PER_CAT = Math.max(1, Math.floor(EXAM_LIMIT * 0.05));

        const categories = {};
        allQuestions.forEach(q => {
            const cat = q.category || '一般';
            if (!categories[cat]) categories[cat] = [];
            categories[cat].push(q);
        });

        let selected = [];
        let usedIds = new Set();

        for (const cat in categories) {
            const catAll = categories[cat].sort(() => 0.5 - Math.random());
            const catOff = catAll.filter(q => q.id <= CUTOFF);
            const catSupp = catAll.filter(q => q.id > CUTOFF);
            
            let pickedFromCat = 0;
            const offToPick = Math.min(catOff.length, MIN_PER_CAT);
            for(let i=0; i<offToPick; i++) {
                selected.push(catOff[i]);
                usedIds.add(catOff[i].id);
                pickedFromCat++;
            }
            if (pickedFromCat < MIN_PER_CAT) {
                const suppToPick_count = Math.min(catSupp.length, MIN_PER_CAT - pickedFromCat);
                for(let i=0; i<suppToPick_count; i++) {
                    selected.push(catSupp[i]); // FIXED: catSupp[i] instead of suppToPick[i]
                    usedIds.add(catSupp[i].id);
                }
            }
        }

        const allRemainingOff = allQuestions.filter(q => q.id <= CUTOFF && !usedIds.has(q.id)).sort(() => 0.5 - Math.random());
        let offNeeded = TARGET_OFF_COUNT - selected.filter(q => q.id <= CUTOFF).length;
        if (offNeeded > 0) {
            const toAdd = allRemainingOff.slice(0, offNeeded);
            selected.push(...toAdd);
            toAdd.forEach(q => usedIds.add(q.id));
        }

        if (selected.length < EXAM_LIMIT) {
            const allRemaining = allQuestions.filter(q => !usedIds.has(q.id)).sort(() => 0.5 - Math.random());
            selected.push(...allRemaining.slice(0, EXAM_LIMIT - selected.length));
        }

        examQuestions = selected.sort(() => 0.5 - Math.random()).slice(0, EXAM_LIMIT);
        renderQuestion(0);
        startTimer();
    }

    function startTimer() {
        timerInterval = setInterval(() => {
            timeLeft--;
            let mins = Math.floor(timeLeft / 60);
            let secs = timeLeft % 60;
            document.getElementById('timer').innerText = mins + ":" + secs.toString().padStart(2, '0');
            if (timeLeft <= 0) {
                alert("時間到！系統自動交卷。");
                submitExam();
            }
        }, 1000);
    }

    function processContent(content, item) {
        if (!content) return '';
        let html = String(content);
        html = html.replace(/^\d+\.\s*/, '');
        html = html.replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
            const src = item['image' + p1] || item['image0' + p1];
            return src ? `<img src="${src}" style="max-width:100%; border-radius:4px; margin: 10px 0;">` : match;
        });
        return html.replace(/●/g, '<br/>●');
    }

    function renderQuestion(index, scrollTop = true) {
        currentIndex = index;
        const item = examQuestions[index];
        const container = document.getElementById('question-area');
        container.innerHTML = '';
        
        document.getElementById('q-progress').innerText = (index + 1) + " / " + examQuestions.length;
        const sidePrev = document.getElementById('side-btn-prev');
        const sideNext = document.getElementById('side-btn-next');
        
        if (sidePrev) sidePrev.style.display = (index === 0) ? 'none' : 'flex';
        if (sideNext) {
            sideNext.style.display = 'flex';
            sideNext.title = (index === (examQuestions.length - 1)) ? '交卷' : '下一題';
        }

        const card = document.createElement('div');
        card.className = 'card question-card';
        let qText = processContent(item.question, item);
        let html = `
            <div class="question-header">Question ${index + 1} / ${examQuestions.length}</div>
            <div class="question-body">
                <div class="mb-4">${qText}</div>
        `;
        
        if (item.image) {
            html += `<div class="text-center mb-4"><img src="${item.image}" style="max-width:100%; border:1px solid #ddd; border-radius:4px;"></div>`;
        }

        const optionsRaw = item.quiz || item.options || [];
        const options = Array.isArray(optionsRaw) ? optionsRaw : [optionsRaw];
        const savedAns = userAnswers[index] !== undefined ? userAnswers[index] : {};
        
        html += '<div class="mt-3">';
        options.forEach((opt, optIdx) => {
            const optStr = String(opt);
            if (optStr.includes('|')) {
                const subOpts = optStr.split('|');
                html += `<div class="sub-question-label">選項 ${optIdx + 1}</div><div class="d-flex flex-wrap gap-2 mb-3 ms-2">`;
                subOpts.forEach((sub, subIdx) => {
                    const isSel = (savedAns && savedAns[optIdx] === subIdx);
                    html += `<div class="sub-opt-container ${isSel ? 'selected' : ''}" onclick="selectSub(${optIdx}, ${subIdx})">(${subIdx+1}) ${sub}</div>`;
                });
                html += `</div>`;
            } else {
                const isSel = (userAnswers[index] === optIdx);
                html += `<div class="option-item ${isSel ? 'selected' : ''}" onclick="selectOption(${optIdx})">${optIdx + 1}. ${optStr}</div>`;
            }
        });
        
        html += '</div></div>';
        card.innerHTML = html;
        container.appendChild(card);
        if (scrollTop) window.scrollTo(0, 0);
        if (typeof Prism !== 'undefined') Prism.highlightAll();
    }

    function changeQuestion(step) {
        if (currentIndex + step >= 0 && currentIndex + step < examQuestions.length) {
            renderQuestion(currentIndex + step);
        } else if (currentIndex + step >= examQuestions.length) {
            confirmSubmit();
        }
    }

    function selectOption(optIdx) {
        userAnswers[currentIndex] = optIdx;
        renderQuestion(currentIndex, false);
    }

    function selectSub(qIdx, subIdx) {
        if (!userAnswers[currentIndex] || typeof userAnswers[currentIndex] !== 'object') {
            userAnswers[currentIndex] = {};
        }
        userAnswers[currentIndex][qIdx] = subIdx;
        renderQuestion(currentIndex, false);
    }

    function confirmSubmit() {
        if (confirm("確定要交卷嗎？")) {
            submitExam();
        }
    }

    function submitExam() {
        clearInterval(timerInterval);
        document.getElementById('exam-ui').style.display = 'none';
        document.getElementById('result-screen').style.display = 'block';
        
        let correctCount = 0;
        let stats = {};
        let incorrectHTML = '';
        let wrongIds = new Set(JSON.parse(localStorage.getItem(WRONG_KEY) || '[]'));

        examQuestions.forEach((item, idx) => {
            const cat = item.category || '未分類';
            if (!stats[cat]) stats[cat] = { total: 0, correct: 0 };
            stats[cat].total++;

            const userAns = userAnswers[idx];
            let isCorrect = false;

            if (item.type === 'multioption' || (item.quiz || item.options || []).some(o => String(o).includes('|'))) {
                const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
                isCorrect = answers.every((a, i) => userAns && (parseInt(a) - 1) === userAns[i]);
            } else if (item.type === 'multiple') {
                const answers = item.answer.map(a => parseInt(a) - 1);
                isCorrect = Array.isArray(userAns) && userAns.length === answers.length && userAns.every(val => answers.includes(val));
            } else {
                isCorrect = userAns === (parseInt(item.answer) - 1);
            }

            if (isCorrect) {
                correctCount++;
                stats[cat].correct++;
                wrongIds.delete(item.id);
            } else {
                wrongIds.add(item.id);
                let qText = processContent(item.question, item);
                let ansText = Array.isArray(item.answer) ? item.answer.join(', ') : item.answer;
                let optionsHTML = '<hr class="my-2"><div class="fw-bold mb-1">選擇：</div><ul class="list-group list-group-flush mb-3" style="font-size: 0.85rem;">';
                (item.quiz || item.options || []).forEach((opt, oIdx) => {
                    optionsHTML += `<li class="list-group-item p-1" style="background: transparent; border: none;">${oIdx + 1}. ${opt}</li>`;
                });
                optionsHTML += '</ul>';
                let expText = processContent(item.explanation || '暫無解析。', item);
                incorrectHTML += `<div class="review-item"><div class="review-id">題目 ${idx + 1} (原始編號: ${item.id})</div><div class="mb-2">${qText}</div>${optionsHTML}<div class="review-ans">正確答案：${ansText}</div><div class="review-exp"><b>解析：</b><br/>${expText}</div></div>`;
            }
        });

        document.getElementById('final-score').innerText = Math.round((correctCount / examQuestions.length) * 100);
        document.getElementById('correct-count').innerText = correctCount;
        localStorage.setItem(WRONG_KEY, JSON.stringify([...wrongIds]));
        
        let catHTML = '<h5 class="text-center mb-3">各類題數佔比與答對率</h5><div class="table-responsive"><table class="table table-bordered table-striped table-hover align-middle"><thead><tr class="table-light"><th>題目分類</th><th class="text-center" style="width:80px">題數</th><th class="text-center" style="width:80px">佔比</th><th class="text-center" style="width:150px">答對率</th></tr></thead><tbody>';
        const sortedCats = Object.keys(stats).sort();
        for (let cat of sortedCats) {
            let total = stats[cat].total;
            let correct = stats[cat].correct;
            let p = Math.round((correct / total) * 100);
            let share = Math.round((total / examQuestions.length) * 100);
            catHTML += `<tr>
                <td class="fw-bold text-secondary">${cat}</td>
                <td class="text-center fw-bold">${total}</td>
                <td class="text-center">${share}%</td>
                <td class="text-center">
                    <div class="d-flex align-items-center">
                        <span class="me-2 small text-muted" style="width:30px">${p}%</span>
                        <div class="progress flex-grow-1" style="height: 10px;">
                            <div class="progress-bar ${p >= 60 ? 'bg-success' : (p >= 40 ? 'bg-warning' : 'bg-danger')}" role="progressbar" style="width: ${p}%"></div>
                        </div>
                    </div>
                </td>
            </tr>`;
        }
        catHTML += '</tbody></table></div>';
        document.getElementById('category-stats').innerHTML = catHTML;

        if (correctCount < examQuestions.length) {
            document.getElementById('btn-export-pdf').style.display = 'inline-block';
            document.getElementById('review-list').innerHTML = incorrectHTML;
        }
    }

    function clearWrongHistory() {
        if (confirm("確定要清除所有科目的錯題紀錄嗎？")) {
            localStorage.removeItem(WRONG_KEY);
            alert("已清除紀錄。");
            location.reload();
        }
    }

    function exportIncorrectPDF() {
        document.getElementById('review-area').style.display = 'block';
        document.body.classList.add('preview-active');
        if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            setTimeout(() => { window.print(); }, 500);
        } else {
            savedZoomBeforePreview = currentZoom;
            currentZoom = 0.7;
            applyZoom();
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = '⬅️ 結束預覽';
            closeBtn.className = 'btn btn-dark btn-lg fixed-bottom m-3 no-print';
            closeBtn.onclick = () => {
                document.getElementById('review-area').style.display = 'none';
                document.body.classList.remove('preview-active');
                currentZoom = savedZoomBeforePreview;
                applyZoom();
                closeBtn.remove();
            };
            document.body.appendChild(closeBtn);
        }
    }

    let currentZoom = 1.0;
    function applyZoom() { document.body.style.zoom = currentZoom; }
    function adjustZoom(delta) { currentZoom += delta; applyZoom(); }
    window.onload = initExam;
"""

targets = [
    {'path': 'www/AI900/mock_exam.html', 'cutoff': 100, 'limit': 40, 'key': 'ai900_wrong_ids', 'title': 'Microsoft AI-900'},
    {'path': 'www/AZ900/mock_exam.html', 'cutoff': 100, 'limit': 40, 'key': 'az900_wrong_ids', 'title': 'Microsoft AZ-900'},
    {'path': 'www/Generative_AI/mock_exam.html', 'cutoff': 100, 'limit': 40, 'key': 'generative_ai_wrong_ids', 'title': 'Generative AI Foundations'},
    {'path': 'www/ITS_AI/mock_exam.html', 'cutoff': 118, 'limit': 40, 'key': 'its_ai_wrong_ids', 'title': 'ITS Artificial Intelligence'},
    {'path': 'www/ITS_Database/mock_exam.html', 'cutoff': 69, 'limit': 40, 'key': 'its_database_wrong_ids', 'title': 'ITS Database Administration'},
    {'path': 'www/ITS_Python/mock_exam.html', 'cutoff': 69, 'limit': 50, 'key': 'its_python_wrong_ids', 'title': 'ITS Python Programming'},
    {'path': 'www/ITS_softdevelop/mock_exam.html', 'cutoff': 69, 'limit': 50, 'key': 'its_softdevelop_wrong_ids', 'title': 'ITS Software Development'}
]

# 讀取標準 HTML Header (以 commit 過的穩定版為基準)
with open('www/ITS_Python/mock_exam.html', 'r', encoding='utf-8') as f:
    template_content = f.read()
    header_part = template_content.split('<script>')[0]

for t in targets:
    if not os.path.exists(t['path']): continue
    curr_header = header_part.replace('ITS Python Programming', t['title'])
    js_content = get_clean_js(t['cutoff'], t['limit'], t['key'])
    final_output = curr_header + "<script>" + js_content + "</script>
</body>
</html>"
    with open(t['path'], 'w', encoding='utf-8') as f:
        f.write(final_output)
    print("Standardized " + t['path'])
