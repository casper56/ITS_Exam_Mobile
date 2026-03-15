import os
import json

def rebuild():
    # 1. 讀取備份並重建
    with open('backups/final_clean_repair.py.bak3', 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 強化 CSS
    css_to_add = r"""
        /* ChoiceListStr 終極穩定樣式 */
        .choicelist-container-flex { display: flex !important; flex-direction: row !important; gap: 15px; margin: 15px 0; align-items: flex-start; }
        .choicelist-pool { flex: 0 0 220px !important; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px; background: #fdfdfd; min-height: 400px; }
        .choicelist-target-text { flex: 1 !important; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; background: #fff; min-height: 400px; min-width: 0; }
        .choicelist-header { font-weight: bold; color: #0d6efd; border-bottom: 1px solid #eee; margin-bottom: 15px; padding: 8px; border-left: 4px solid #0d6efd; font-size: 0.9rem; background: #fff; border-radius: 4px; }
        .choicelist-q-text { white-space: pre !important; font-family: 'Cascadia Code', Consolas, Monaco, monospace !important; font-size: 0.95rem; line-height: 2.0 !important; color: #333; overflow-x: auto; }
        .choicelist-item { background: #fff; border: 1px solid #ced4da; border-radius: 6px; padding: 4px 10px; margin-bottom: 4px; cursor: pointer; font-size: 0.82rem !important; transition: all 0.2s; position: relative; user-select: none; white-space: pre !important; font-family: Consolas, monospace !important; line-height: 1.1 !important; display: block; }
        .choicelist-item:hover { border-color: #0d6efd; background: #f0f7ff; }
        .choicelist-item.disabled { opacity: 0.3 !important; cursor: not-allowed; background: #e9ecef !important; }
        .target-slot.inline-slot { display: inline-flex !important; min-width: 120px !important; height: 30px !important; margin: 0 5px !important; vertical-align: middle !important; border: 1px solid #ced4da !important; background-color: #f8f9fa !important; color: #adb5bd !important; font-size: 0.8rem !important; border-radius: 4px !important; cursor: pointer !important; justify-content: center !important; align-items: center !important; }
        .choicelist-item.in-slot { margin: 0 5px !important; padding: 0 10px !important; border: 1px solid #9ec5fe !important; background-color: #e7f1ff !important; display: inline-flex !important; width: auto !important; height: 30px !important; font-size: 0.95rem !important; cursor: pointer !important; border-radius: 4px !important; align-items: center !important; justify-content: center !important; color: #084298 !important; font-weight: bold !important; vertical-align: middle !important; }
        .choicelist-item.in-slot:hover { background-color: #fff0f0 !important; border-color: #dc3545 !important; color: #dc3545 !important; }
        .choicelist-item.in-slot::after { content: " ×"; font-size: 1.0rem; }
    """

    # 3. 核心 JS 邏輯 (支援 2D options)
    js_logic = r"""
    window.renderChoiceListStrQuestion = function(index) {
        currentIndex = index; const item = (typeof quizData !== 'undefined') ? quizData[index] : examQuestions[index];
        const container = (typeof quizData !== 'undefined') ? document.getElementById('question-container') : document.getElementById('question-area');
        
        // --- 核心相容性處理：自動識別 2D options ---
        let allOptions = [], displayGroups = [];
        if (item.options && Array.isArray(item.options[0])) {
            displayGroups = item.options;
            allOptions = item.options.flat();
        } else {
            allOptions = item.options || [];
            displayGroups = item.options_grouped || [allOptions];
        }

        const req = item.answer.length;
        if (!Array.isArray(userAnswers[index]) || userAnswers[index].length !== req) { userAnswers[index] = new Array(req).fill(null); }
        const currentAns = userAnswers[index];
        const isPractice = (typeof quizData !== 'undefined'), isLocked = isPractice && (correctSet.has(index) || correctedSet.has(index)), isWrong = isPractice && incorrectSet.has(index);

        const qLines = Array.isArray(item.question) ? item.question : [item.question];
        let topParts = [], codeLines = [], reachedCode = false;
        qLines.forEach((line) => {
            if (line.includes('[[slot')) reachedCode = true;
            if (reachedCode) { codeLines.push(line.replace(/<\/?[^>]+(>|$)/g, "")); } else { topParts.push(line); }
        });
        
        let codeContent = codeLines.join('\n');
        for (let i = 0; i < req; i++) {
            const optIdx = currentAns[i];
            let slotHtml = (optIdx !== null) ? `<span class="choicelist-item in-slot" onclick="${isLocked ? '' : `removeFromStrTarget(${i})`}">${String(allOptions[optIdx]).replace(/</g, '&lt;').replace(/>/g, '&gt;')}</span>` : `<span class="target-slot inline-slot">位置 ${i + 1}</span>`;
            codeContent = codeContent.replace(/\[\[slot\d*\]\]/, slotHtml);
        }

        let poolHtml = '', flatCounter = 0;
        displayGroups.forEach((group, gIdx) => {
            poolHtml += `<div class="mb-2"><div style="font-size: 0.75rem; font-weight: bold; color: #666; background: #eee; padding: 1px 8px; border-radius: 4px; margin-bottom: 3px;">群組 ${gIdx + 1}</div><div class="d-flex flex-column gap-0">`;
            group.forEach(opt => {
                const idx = flatCounter++;
                poolHtml += `<div class="choicelist-item ${currentAns.includes(idx) || isLocked ? 'disabled' : ''}" onclick="${currentAns.includes(idx) || isLocked ? '' : `moveToStrTarget(${idx})`}">${String(opt).replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>`;
            });
            poolHtml += `</div></div>`;
        });

        const displayAnsHtml = isPractice ? (Array.isArray(item.answer) ? item.answer : [item.answer]).map((val, i) => {
            const optIdx = parseAnswerToIndex(val);
            return `<div class="mt-2 border-start border-success border-4 bg-light" style="padding: 10px 12px; font-family:monospace; font-size:0.95rem;">(${i+1}) ${allOptions[optIdx] || val}</div>`;
        }).join('') : '';

        container.innerHTML = `<div class="card question-card">
            <div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1}</span><span class="badge bg-info">填空題</span></div><div class="category-tag">${item.category || ''}</div></div>
            <div class="question-body">
                <div class="choicelist-top-stimulus mb-4">${processContent(topParts, item)}</div>
                <div class="choicelist-container-flex">
                    <div class="choicelist-pool"><div class="choicelist-header">選項區 (點擊填入)</div>${poolHtml}</div>
                    <div class="choicelist-target-text"><div class="choicelist-header">答題區</div><div class="choicelist-q-text">${codeContent}</div></div>
                </div>
                ${isPractice && !isLocked ? `<div class="text-center mt-4 pt-3 border-top"><button class="btn btn-primary px-5" onclick="submitChoiceListStr()">確認提交</button></div>` : ''}
                ${isPractice && (isWrong || isLocked) ? `<div class="answer-section" style="display:block; margin-top: 20px;"><h6 class="fw-bold mb-3">${isWrong ? '❌ 答錯了' : '✅ 答對認證'}！正確答案：</h6><div class="mb-3">${displayAnsHtml}</div><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div>` : ''}
            </div>
        </div>`;
        if(typeof updateUI === 'function') updateUI();
    };

    window.moveToStrTarget = function(optIdx) {
        const item = (typeof quizData !== 'undefined') ? quizData[currentIndex] : examQuestions[currentIndex];
        if (!userAnswers[currentIndex]) userAnswers[currentIndex] = new Array(item.answer.length).fill(null);
        const empty = userAnswers[currentIndex].indexOf(null);
        if (empty !== -1) { userAnswers[currentIndex][empty] = optIdx; renderChoiceListStrQuestion(currentIndex); }
    };

    window.removeFromStrTarget = function(ansIdx) {
        if (userAnswers[currentIndex]) { userAnswers[currentIndex][ansIdx] = null; renderChoiceListStrQuestion(currentIndex); }
    };

    window.submitChoiceListStr = function() {
        const item = quizData[currentIndex];
        const userIdxs = userAnswers[currentIndex] || [];
        const correctAns = Array.isArray(item.answer) ? item.answer : [item.answer];
        let isCorrect = (userIdxs.length === correctAns.length);
        if (isCorrect) {
            // 這裡自動攤平 options 以進行答案比對
            const allOpts = Array.isArray(item.options[0]) ? item.options.flat() : item.options;
            isCorrect = correctAns.every((a, i) => userIdxs[i] === parseAnswerToIndex(a));
        }
        if (isCorrect) { if (incorrectSet.has(currentIndex)) { incorrectSet.delete(currentIndex); correctedSet.add(currentIndex); } else { correctSet.add(currentIndex); } } else { incorrectSet.add(currentIndex); }
        saveState(); renderChoiceListStrQuestion(currentIndex);
    };
    """

    # --- 取代邏輯 ---
    content = content.replace('    </style>', css_to_add + '\n    </style>')
    content = content.replace('    function renderQuestion(index, scrollTop = true)', js_logic + '\n    function renderQuestion(index, scrollTop = true)')
    content = content.replace('    function renderQuestion(index) {', js_logic + '\n    function renderQuestion(index) {')
    content = content.replace("currentIndex = index; const item = examQuestions[index]; ", "currentIndex = index; const item = examQuestions[index]; if (item.type === 'choiceliststr') { renderChoiceListStrQuestion(index); return; }")
    content = content.replace("currentIndex = index; const item = quizData[index];", "currentIndex = index; const item = quizData[index]; if (item.type === 'choiceliststr') { renderChoiceListStrQuestion(index); return; }")
    
    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    rebuild()
    print("DONE_WITH_2D_OPTIONS_SUPPORT")
