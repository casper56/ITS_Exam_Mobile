/* ChoiceList 終極補丁 V3.5.24 (精確字元 & sz 響應版) */
(function() {
    let selectedSlotIdx = -1;

    window.renderChoiceListQuestion = function(index) {
        const isMock = (typeof examQuestions !== 'undefined');
        const quizList = isMock ? examQuestions : quizData;
        const containerId = isMock ? 'question-area' : 'question-container';
        
        currentIndex = index; 
        const item = quizList[index];
        const container = document.getElementById(containerId);
        if (!container) return;

        if (!Array.isArray(userAnswers[index])) userAnswers[index] = [];
        const currentAns = userAnswers[index];
        const isReviewMode = !!(document.getElementById('review-list') && document.getElementById('review-list').innerHTML);
        const isPractice = !isMock;
        const isLocked = isMock ? isReviewMode : (correctSet.has(index) || correctedSet.has(index));
        const isWrong = isPractice ? incorrectSet.has(index) : false;

        // --- V3.5.24 精確字元量測核心 ---
        const szStr = item.sz || "0.85rem";
        // 動態計算 CHAR_W：以 16px 為基準 rem 換算，Consolas 比例約 0.62
        const baseFontSize = parseFloat(szStr) * 16;
        const CHAR_W = baseFontSize * 0.62; 
        
        const slotData = item.slots || item.slot;
        let maxSlotChars = 0;
        if (slotData && Array.isArray(slotData)) {
            slotData.forEach(line => {
                // 1. 強力移除特定 Python 37字標籤 (物理級扣除)
                let p = line.replace('<pre><code class=\\"language-python\\">', '');
                p = p.replace('<pre><code class=\"language-python\">', '');
                p = p.replace('</code></pre>', '');
                // 2. 移除所有剩餘 HTML 標籤、斜線、Slot標記
                p = p.replace(/<[^>]*>/g, "").replace(/\\/g, "").replace(/<slot\d*>/g, "").trimEnd();
                
                // 目標：31 (對應程式碼內容)
                if (p.length > maxSlotChars) maxSlotChars = p.length;
            });
        }

        let maxOptChars = 0;
        item.options.forEach(opt => {
            const p = opt.replace(/<[^>]*>/g, "").replace(/\\/g, "").trim();
            if (p.length > maxOptChars) maxOptChars = p.length;
        });

        // 選項區寬度 = slots 最大字元 (31) * 字寬
        const finalOptW = Math.ceil(maxSlotChars * CHAR_W) + 15;
        const optStyle = `min-width:${finalOptW}px; width:${finalOptW}px;`;

        // 答案區總寬度 = (選項最大字元 + slots 最大字元) * 字寬
        const totalTargetW = Math.ceil((maxOptChars + maxSlotChars) * CHAR_W) + 40;
        const targetInnerStyle = `min-width:${totalTargetW}px; width:${totalTargetW}px;`;
        // ----------------------------------------------

        const requiredCount = (slotData && Array.isArray(slotData)) ? 
            slotData.join('').split('<slot').length - 1 : 
            item.answer.length;

        if (userAnswers[index].length !== requiredCount) userAnswers[index] = new Array(requiredCount).fill(null);
        if (selectedSlotIdx === -1 || selectedSlotIdx >= requiredCount) {
            const firstEmpty = userAnswers[index].indexOf(null);
            selectedSlotIdx = (firstEmpty !== -1) ? firstEmpty : 0;
        }

        const customSz = `font-size: ${szStr} !important; --sz: ${szStr} !important;`;

        let poolHtml = '';
        item.options.forEach((opt, idx) => {
            const isUsed = currentAns.includes(idx);
            poolHtml += `<div class="choicelist-item ${isUsed || isLocked ? 'disabled' : ''}" style="${customSz} ${optStyle}" onclick="${isUsed || isLocked ? '' : `moveToTarget(${idx})`}">${opt}</div>`;
        });

        let targetHtml = '';
        if (slotData && Array.isArray(slotData)) {
            let sIdxCounter = 0;
            slotData.forEach(line => {
                const lineHtml = line.replace(/<slot\d*>/g, () => {
                    const sIdx = sIdxCounter++;
                    const optIdx = currentAns[sIdx], isActive = (selectedSlotIdx === sIdx && !isLocked);
                    if (optIdx !== null) return `<span class="choicelist-item inline-item ${isActive ? 'active-slot' : ''}" style="${customSz} ${optStyle}" onclick="${isLocked ? '' : `selectSlot(${sIdx})`}">${item.options[optIdx]}</span>`;
                    return `<span class="target-slot inline-slot ${isActive ? 'active-slot' : ''}" style="${optStyle}" onclick="${isLocked ? '' : `selectSlot(${sIdx})`}">[Slot ${sIdx + 1}]</span>`;
                });
                targetHtml += `<div class="choicelist-code-line" style="${customSz}">${lineHtml}</div>`;
            });
        }

        const displayAnsHtml = (Array.isArray(item.answer) ? item.answer : [item.answer]).map(val => {
            const optIdx = parseAnswerToIndex(val);
            return `<div class="mt-2 border-start border-success border-4 bg-light p-2 font-monospace" style="${customSz}">${item.options[optIdx] || val}</div>`;
        }).join('');

        container.innerHTML = `<div class="card question-card">
            <div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizList.length}</span><span class="badge bg-info">排序題</span></div><div class="category-tag">${item.category || '一般'}</div></div>
            <div class="question-body" style="padding-bottom:0;"><div class="choicelist-q-text">${processContent(item.question, item)}</div></div>
            <div class="px-3 pb-3">
                <div class="choicelist-wrapper" style="width: fit-content; margin-left: 0;">
                    <div class="choicelist-pool" style="width: auto;"><h6>選項區</h6>${poolHtml}</div>
                    <div class="choicelist-target" style="width: auto; min-width: auto;">
                        <h6>答案區</h6>
                        <div style="background:#f8f9fa; padding:15px; border-radius:8px; overflow-x:auto;">
                            <div style="${targetInnerStyle}">${targetHtml}</div>
                        </div>
                    </div>
                </div>
                ${isPractice && !isLocked ? `<div class="text-center mt-4 pt-3 border-top"><button class="btn btn-primary px-5" onclick="submitChoiceList()">確認提交</button></div>` : ''}
                <div class="answer-section" style="${(isPractice && (isWrong || isLocked)) || (isMock && isReviewMode) ? 'display:block' : 'display:none'}">
                    <h6>正確順序如下：</h6>
                    <div class="mb-3">${displayAnsHtml}</div>
                    <div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div>
                </div>
            </div>
        </div>`;
        if(window.Prism) Prism.highlightAll();
        if(typeof updateUI === 'function') updateUI();
    };

    window.selectSlot = function(idx) {
        userAnswers[currentIndex][idx] = null;
        selectedSlotIdx = idx;
        if (typeof saveState === 'function') saveState();
        window.renderChoiceListQuestion(currentIndex);
    };

    window.moveToTarget = function(optIdx) {
        if (!userAnswers[currentIndex]) return;
        if (selectedSlotIdx === -1 || userAnswers[currentIndex][selectedSlotIdx] !== null) {
            const empty = userAnswers[currentIndex].indexOf(null);
            if (empty !== -1) selectedSlotIdx = empty;
        }
        if (selectedSlotIdx !== -1) {
            userAnswers[currentIndex][selectedSlotIdx] = optIdx;
            const nextEmpty = userAnswers[currentIndex].indexOf(null);
            if (nextEmpty !== -1) selectedSlotIdx = nextEmpty;
            if (typeof saveState === 'function') saveState();
            window.renderChoiceListQuestion(currentIndex);
        }
    };

    window.removeFromTarget = function(ansIdx) { window.selectSlot(ansIdx); };
    
    window.submitChoiceList = function() {
        const item = (typeof quizData !== 'undefined') ? quizData[currentIndex] : examQuestions[currentIndex];
        const userIdxs = userAnswers[currentIndex] || [], correctAns = Array.isArray(item.answer) ? item.answer : [item.answer];
        let isCorrect = (userIdxs.length === correctAns.length && !userIdxs.includes(null));
        if (isCorrect) { for (let i = 0; i < correctAns.length; i++) { if (userIdxs[i] !== parseAnswerToIndex(correctAns[i])) { isCorrect = false; break; } } }
        if (isCorrect) { if (incorrectSet.has(currentIndex)) { incorrectSet.delete(currentIndex); correctedSet.add(currentIndex); } else { correctSet.add(currentIndex); } }
        else { incorrectSet.add(currentIndex); }
        if (typeof saveState === 'function') saveState();
        window.renderChoiceListQuestion(currentIndex);
    };
})();
