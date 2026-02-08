import json
import re

def emergency_restore():
    path = 'www/ITS_Python/mock_exam.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修正 ID 27 標籤 (再次確保)
    content = content.replace('<code class=\\"language-python>', '<code class=\\"language-python\\">')
    
    # 2. 找到 allQuestions 的結束位置
    # 搜尋 "];" 且前面有大量的 JSON 資料
    match = re.search(r'const allQuestions = \[.*?\];', content, re.DOTALL)
    if not match:
        print("Could not find allQuestions array.")
        return
    
    questions_end = match.end()
    
    # 3. 定義乾淨的後續腳本
    clean_script = """
    const categories = ["D1_資料型別與運算子", "D2_控制流程", "D3_輸入與輸出", "D4_程式碼除錯與維護", "D5_演算法與資料結構", "D6_標準函式庫", "D7_進階練習(APCS/考古題)"];

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

        // 1. 按類別分桶並隨機排序
        categories.forEach(cat => {
            buckets[cat] = allQuestions.filter(q => q.category === cat)
                                       .sort(() => 0.5 - Math.random());
        });

        // 2. 優先抽取 D7 類別 (APCS) 3 題
        const d7Name = "D7_進階練習(APCS/考古題)";
        if (buckets[d7Name]) {
            let take = Math.min(buckets[d7Name].length, 3);
            selectedQuestions.push(...buckets[d7Name].splice(0, take));
        }

        // 3. 輪流從其餘類別中抽題，直到滿 50 題
        let otherCats = categories.filter(c => c !== d7Name);
        let hasMore = true;
        while (selectedQuestions.length < 50 && hasMore) {
            hasMore = false;
            for (let cat of otherCats) {
                if (selectedQuestions.length >= 50) break;
                if (buckets[cat] && buckets[cat].length > 0) {
                    selectedQuestions.push(buckets[cat].shift());
                    hasMore = true;
                }
            }
        }

        // 4. 初始化考試狀態
        examQuestions = selectedQuestions.sort(() => 0.5 - Math.random());
        currentIndex = 0;
        userAnswers = {};
        timeLeft = 50 * 60;
        
        document.getElementById('start-screen').style.display = 'none';
        document.getElementById('exam-ui').style.display = 'block';
        
        renderQuestion(0);
        startTimer();
        console.log("出題完成。總數:", examQuestions.length);
    }

    function startTimer() {
        if (timerInterval) clearInterval(timerInterval);
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
        window.scrollTo(0,0);
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

            if (isCorrect) { 
                correctCount++; 
                catStats[cat].correct++; 
            } else {
                let qClean = item.question.replace(/<pre[^>]*>([\\s\\S]*?)<\\/pre>/gi, '<div style="font-family:monospace; font-size:10pt; white-space: pre-wrap; background:#f4f4f4; border:1px solid #000; padding:8px; margin:10px 0; color:#000 !important;">$1</div>').replace(/<br[^>]*>/gi, " ");
                qClean = qClean.replace(/<code[^>]*>([\\s\\S]*?)<\\/code>/gi, '<code style="color:#000 !important; font-weight:bold;">$1</code>');
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
        
        if (score >= 70) {
            confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
        }
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

    function showReviewReport() {
        document.getElementById('result-screen').style.display = 'none';
        document.getElementById('report-time').innerText = new Date().toLocaleString();
        document.getElementById('review-content').innerHTML = globalIncorrectHTML;
        document.getElementById('review-container').style.display = 'block';
        window.scrollTo(0, 0);
    }

    async function downloadPDF() {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF('p', 'pt', 'a4');
        const container = document.getElementById('review-content');
        const blocks = container.getElementsByClassName('review-block');
        
        let yOffset = 40;
        doc.setFontSize(16);
        doc.text("ITS Python 模擬考檢討報告", 40, yOffset);
        yOffset += 30;
        doc.setFontSize(10);
        doc.text(`產出時間：${new Date().toLocaleString()}`, 40, yOffset);
        yOffset += 20;

        for (let i = 0; i < blocks.length; i++) {
            const canvas = await html2canvas(blocks[i], { scale: 2 });
            const imgData = canvas.toDataURL('image/jpeg', 0.8);
            const imgProps = doc.getImageProperties(imgData);
            const pdfWidth = doc.internal.pageSize.getWidth() - 80;
            const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

            if (yOffset + pdfHeight > doc.internal.pageSize.getHeight() - 40) {
                doc.addPage();
                yOffset = 40;
            }

            doc.addImage(imgData, 'JPEG', 40, yOffset, pdfWidth, pdfHeight);
            yOffset += pdfHeight + 20;
        }
        doc.save(`ITS_Python_Review_${new Date().getTime()}.pdf`);
    }
    </script>
    </body>
    </html>
    """
    
    # 移除從 allQuestions 結束到最後的所有內容
    new_content = content[:questions_end] + clean_script
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Emergency restore completed successfully.")

emergency_restore()