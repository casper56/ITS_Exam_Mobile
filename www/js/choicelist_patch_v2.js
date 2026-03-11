/* ChoiceList 全球通用統一補丁 V3.5.14 (精確高度對齊與空格保留) */
(function() {
    let selectedSlotIdx = -1;

    // --- 注入強力 CSS ---
    const style = document.createElement('style');
    style.innerHTML = 
        ':root { --cl-pool-gap: 4px; --cl-gap: 2px; --cl-row-height: 2.6rem; --cl-padding: 0 12px; --cl-header-height: 30px; } ' +
        '.cl-header { font-weight: bold !important; color: #0d6efd !important; height: var(--cl-header-height) !important; line-height: var(--cl-header-height) !important; margin-bottom: 10px !important; border-bottom: 1px solid #ddd !important; width: fit-content !important; font-size: 0.8rem !important; padding-bottom: 2px !important; } ' +
        
        /* 選項區：恢復原始 fit-content 寬度 */
        '.choicelist-pool { display: flex !important; flex-direction: column !important; flex: 0 0 auto !important; width: fit-content !important; max-width: 85% !important; } ' +
        '.cl-items-container.pool-area { display: grid !important; grid-template-columns: 1fr; width: fit-content !important; min-width: 120px; gap: var(--cl-pool-gap) !important; } ' +
        '.grouped-pool-unit { width: fit-content !important; max-width: 100%; border-radius: 8px; transition: all 0.3s; } ' +
        
        /* PC 版預設：絕對不換行 */
        '.choicelist-item, .choicelist-code-line { display: flex !important; align-items: flex-start !important; min-height: var(--cl-row-height) !important; padding: 8px 12px !important; margin: 0 !important; box-sizing: border-box !important; font-family: "Consolas", "Monaco", "Courier New", monospace !important; border-radius: 4px !important; white-space: pre !important; word-break: keep-all !important; overflow: visible !important; text-align: left !important; } ' +
        '.choicelist-item { background: #fff; border: 1px solid #ced4da; cursor: pointer; width: 100% !important; } ' +
        '.choicelist-code-line { border: 1px solid transparent; border-bottom: 1px solid #f0f0f0; } ' +
        
        /* 回答區：恢復原始 fit-content 寬度 */
        '.choicelist-target { display: flex !important; flex-direction: column !important; flex: 0 0 auto !important; min-width: 300px !important; max-width: 100% !important; } ' +
        /* 淺灰色背景：flex: 1 確保高度對齊，維持 padding */
        '.pool-bg, .target-bg { background: #f8f9fa !important; border-radius: 8px; padding: 8px !important; border: 1px solid #ddd !important; flex: 1 1 auto !important; display: flex !important; flex-direction: column !important; gap: var(--cl-pool-gap) !important; } ' +
        
        '.target-slot.inline-slot, .choicelist-item.inline-item { display: inline-flex !important; align-items: center; justify-content: flex-start !important; min-height: 1.8rem !important; height: auto !important; line-height: 1.2 !important; vertical-align: middle !important; padding: 4px 8px !important; margin: 2px 4px !important; border-radius: 4px !important; font-size: 0.95em !important; cursor: pointer !important; position: relative; z-index: 50; box-sizing: border-box !important; white-space: pre-wrap !important; text-align: left !important; word-break: break-all !important; } ' +
        '.choicelist-item.inline-item { background: #e7f1ff !important; border: 2px solid #0d6efd !important; border-left-width: 5px !important; color: #0d6efd !important; width: auto !important; } ' +
        '.locked-slot { background: transparent !important; border: 1px solid transparent !important; color: #198754 !important; font-weight: bold !important; cursor: default !important; } ' +
        '.target-slot.inline-slot { background: #fff !important; border: 2px dashed #adb5bd !important; color: #6c757d !important; justify-content: center !important; } ' +
        '.active-slot { border: 2px solid red !important; background: #fff5f5 !important; box-shadow: 0 0 8px rgba(255,0,0,0.5) !important; color: red !important; } ' +
        '.opt-label { display: inline-block !important; flex: 0 0 auto !important; font-weight: bold; color: #6c757d; margin-right: 10px; border-right: 1px solid #dee2e6; padding-right: 10px; min-width: 1.5rem; text-align: center; line-height: 1.4 !important; vertical-align: middle !important; } ' +
        
        /* 核心佈局：stretch 強制高度同步，gap 控制間距 */
        '.choicelist-wrapper { display: flex !important; flex-direction: row !important; align-items: stretch !important; overflow-x: auto !important; padding-bottom: 15px; gap: 20px !important; width: 100% !important; } ' +
        '.cl-content-text { display: inline-block !important; flex: 0 0 auto !important; white-space: pre !important; word-break: keep-all !important; line-height: 1.4 !important; vertical-align: top !important; } ' +
        
        /* 手機版特規 */
        '@media (max-width: 768px) { ' +
            '.choicelist-item, .choicelist-code-line, .cl-content-text { white-space: pre-wrap !important; word-break: break-all !important; } ' +
            '.choicelist-pool, .choicelist-target { width: 100% !important; max-width: 100% !important; } ' +
            '.choicelist-wrapper { flex-direction: column !important; overflow-x: visible !important; } ' +
        '} ';
    document.head.appendChild(style);

    const stripCodeTags = (str) => {
        if (!str) return "";
        if (Array.isArray(str)) return str.map(stripCodeTags).join(" ");
        return str.replace(/<pre><code.*?>/g, "").replace(/<\/code><\/pre>/g, "").replace(/<code.*?>/g, "").replace(/<\/code>/g, "");
    };

    const highlightHardened = (text) => {
        if (!window.Prism || !text) return text;
        return Prism.highlight(text, Prism.languages.python, "python");
    };

    window.renderChoiceListQuestion = function(index) {
        const isMock = (typeof examQuestions !== "undefined");
        const quizList = isMock ? examQuestions : quizData;
        const containerId = isMock ? "question-area" : "question-container";
        const container = document.getElementById(containerId);
        if (!container) return;

        currentIndex = index; 
        const item = quizList[index];
        const isCorrect = (typeof correctSet !== "undefined") ? correctSet.has(index) : false;
        const isIncorrect = (typeof incorrectSet !== "undefined") ? incorrectSet.has(index) : false;
        const isCorrected = (typeof correctedSet !== "undefined") ? correctedSet.has(index) : false;
        const isReviewMode = !!(document.getElementById("review-list") && document.getElementById("review-list").innerHTML !== "");
        const isLocked = isMock ? isReviewMode : (isCorrect || isCorrected);

        const slotData = item.slots || item.slot;
        const requiredCount = (slotData && Array.isArray(slotData)) ? slotData.join("").split("<slot").length - 1 : 1;
        if (!Array.isArray(userAnswers[index]) || userAnswers[index].length !== requiredCount) {
            userAnswers[index] = new Array(requiredCount).fill(null);
        }
        if (selectedSlotIdx === -1 || selectedSlotIdx >= requiredCount) {
            const firstEmpty = userAnswers[index].indexOf(null);
            selectedSlotIdx = (firstEmpty !== -1) ? firstEmpty : 0;
        }
        if (isLocked) selectedSlotIdx = -1;

        const szStr = item.sz || "0.85rem";
        const customSz = "font-size: " + szStr + " !important; --sz: " + szStr + " !important;";
        const charRatio = item.ratio || 0.6;
        const charBuff = (item.buff !== undefined) ? item.buff : 0;
        const CHAR_W = (parseFloat(szStr) * 16) * charRatio;

        // 選項區渲染 (新增 pool-bg)
        let poolItemsHtml = "<div class=\"cl-header\">選項區</div><div class=\"pool-bg\">";
        const isGrouped = Array.isArray(item.options[0]);
        
        if (isGrouped) {
            item.options.forEach((group, gIdx) => {
                let localMaxLen = 4;
                group.forEach(opt => {
                    const text = stripCodeTags(opt);
                    const lines = text.split('\n');
                    lines.forEach(line => {
                        const processed = line.replace(/\t/g, "    ");
                        if (processed.length > localMaxLen) localMaxLen = processed.length;
                    });
                });
                const localTextW = Math.ceil((localMaxLen + 2 + charBuff) * CHAR_W);
                const localTextStyle = "width: " + localTextW + "px !important;";
                const isActiveGroup = (selectedSlotIdx === gIdx && !isLocked);
                const activeStyle = isActiveGroup ? "border: 2px solid #0d6efd !important; border-radius: 8px; background: #f0f7ff !important; padding: 8px !important;" : "";
                poolItemsHtml += "<div class=\"grouped-pool-unit\" style=\"" + activeStyle + "\">";
                poolItemsHtml += "<div style=\"font-weight:bold; color:#666; margin-bottom:4px; font-size:0.75rem;\">[ 選項 " + (gIdx + 1) + " ]</div>";
                poolItemsHtml += "<div class=\"cl-items-container pool-area\">";
                group.forEach((opt, optIdx) => {
                    const cleanText = stripCodeTags(opt);
                    poolItemsHtml += "<div class=\"choicelist-item " + (isLocked ? "disabled" : "") + "\" style=\"" + customSz + (isLocked ? "cursor: default !important;" : "") + "\" onclick=\"" + (isLocked ? "" : "window.moveToTarget(" + optIdx + ", " + gIdx + ")") + "\"><span class=\"opt-label\">" + String.fromCharCode(65 + optIdx) + "</span><span class=\"cl-content-text\" style=\"" + localTextStyle + "\">" + highlightHardened(cleanText) + "</span></div>";
                });
                poolItemsHtml += "</div></div>";
            });
        } else {
            let localMaxLen = 4;
            item.options.forEach(opt => {
                const text = stripCodeTags(opt);
                const lines = text.split('\n');
                lines.forEach(line => {
                    const processed = line.replace(/\t/g, "    ");
                    if (processed.length > localMaxLen) localMaxLen = processed.length;
                });
            });
            const localTextW = Math.ceil((localMaxLen + 2 + charBuff) * CHAR_W);
            const localTextStyle = "width: " + localTextW + "px !important;";
            poolItemsHtml += "<div class=\"cl-items-container pool-area\">";
            item.options.forEach((opt, idx) => {
                const cleanText = stripCodeTags(opt);
                poolItemsHtml += "<div class=\"choicelist-item " + (isLocked ? "disabled" : "") + "\" style=\"" + customSz + (isLocked ? "cursor: default !important;" : "") + "\" onclick=\"" + (isLocked ? "" : "window.moveToTarget(" + idx + ")") + "\"><span class=\"opt-label\">" + String.fromCharCode(65 + idx) + "</span><span class=\"cl-content-text\" style=\"" + localTextStyle + "\">" + highlightHardened(cleanText) + "</span></div>";
            });
            poolItemsHtml += "</div>";
        }
        poolItemsHtml += "</div>"; // close pool-bg

        // 回答區渲染
        let targetItemsHtml = "<div class=\"cl-header\">回答區</div><div class=\"target-bg\">";
        if (slotData) {
            let sIdxCounter = 0;
            slotData.forEach(line => {
                const rawLine = stripCodeTags(line);
                const segments = rawLine.split(/<slot\d*>/);
                let lineFinalHtml = "";
                segments.forEach((seg, i) => {
                    // 包裹文字以保留空格縮排
                    lineFinalHtml += "<span class=\"cl-content-text\">" + highlightHardened(seg) + "</span>";
                    if (i < segments.length - 1) {
                        const sIdx = sIdxCounter++;
                        const optIdx = userAnswers[index][sIdx], isActive = (selectedSlotIdx === sIdx && !isLocked);
                        const clickHandler = isLocked ? "" : "onclick=\"event.stopPropagation(); window.selectSlot(" + sIdx + ")\"";
                        if (optIdx !== null && optIdx !== undefined) {
                            const cls = isLocked ? "locked-slot" : "choicelist-item inline-item";
                            const filledText = stripCodeTags(isGrouped ? item.options[sIdx][optIdx] : item.options[optIdx]);
                            lineFinalHtml += "<span class=\"" + cls + (isActive ? " active-slot" : "") + "\" " + clickHandler + "><span class=\"cl-content-text\">" + highlightHardened(filledText) + "</span></span>";
                        } else {
                            lineFinalHtml += "<span class=\"target-slot inline-slot" + (isActive ? " active-slot" : "") + "\" " + clickHandler + ">[ 選項 " + (sIdx + 1) + " ]</span>";
                        }
                    }
                });
                targetItemsHtml += "<div class=\"choicelist-code-line\" style=\"" + customSz + "\">" + lineFinalHtml + "</div>";
            });
        }
        targetItemsHtml += "</div>";

        const poolContainer = "<div class=\"choicelist-pool\">" + poolItemsHtml + "</div>";
        const targetContainer = "<div class=\"choicelist-target\">" + targetItemsHtml + "</div>";
        
        let statusTextHtml = '';
        let cardClass = 'card question-card';
        if (isCorrect) { statusTextHtml = '<div class="alert alert-success py-1 px-2 mb-2 fw-bold">答對了 ✅</div>'; cardClass += ' correct'; }
        else if (isCorrected) { statusTextHtml = '<div class="alert alert-warning py-1 px-2 mb-2 fw-bold text-dark">已修正 ⚠️</div>'; cardClass += ' corrected'; }
        else if (isIncorrect) { statusTextHtml = '<div class="alert alert-danger py-1 px-2 mb-2 fw-bold">答錯了 ❌</div>'; cardClass += ' incorrect'; }

        const headerHtml = isMock 
            ? `題目 ${index + 1} / ${quizList.length} <span class="badge bg-secondary small ms-2">${item.category || ''}</span>`
            : `<div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizList.length}</span><span class="badge bg-info">填空題 (ChoiceList)</span></div><div class="category-tag">${item.category || '一般'}</div>`;

        container.innerHTML = `<div class="${cardClass}">
            <div class="question-header">${headerHtml}</div>
            <div class="question-body" style="padding-bottom:0;"><div class="choicelist-q-text">${processContent(item.question, item)}</div></div>
            <div class="px-3 pb-3">
                <div class="choicelist-wrapper">${poolContainer}${targetContainer}</div>
                ${(!isLocked && !isMock) ? `<div class="text-center mt-4 pt-3 border-top"><button class="btn btn-primary px-5" id="choicelist-submit-btn" onclick="window.submitChoiceList()">確認提交</button></div>` : ''}
                <div class="answer-section" id="choicelist-ans-section" style="${isLocked || isIncorrect ? 'display:block' : 'display:none'}">
                    ${statusTextHtml}
                    <h6 class="fw-bold mb-3">正確順序如下：</h6>
                    <div class="mb-3">${(Array.isArray(item.answer) ? item.answer : [item.answer]).map((val, ansIdx) => {
                        const idx = parseAnswerToIndex(val);
                        const optText = isGrouped ? item.options[ansIdx][idx] : item.options[idx];
                        const cleanText = stripCodeTags(optText);
                        return `<div class="mt-2 border-start border-success border-4 bg-light p-2 font-monospace" style="display:flex; align-items:flex-start;"><span class="badge bg-secondary me-2" style="flex:0 0 auto; margin-top:2px;">${String.fromCharCode(65 + idx)}</span><span class="cl-content-text" style="flex:1 1 auto;">${highlightHardened(cleanText) || val}</span></div>`;
                    }).join('')}</div>
                    <div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div>
                </div>
            </div>
        </div>`;

        // 恢復導航按鈕功能
        const sp = document.getElementById('side-btn-prev');
        const sn = document.getElementById('side-btn-next');
        if (sp) sp.style.display = (index === 0) ? 'none' : 'flex';
        if (sn) sn.style.display = 'flex';

        if(typeof updateUI === "function") updateUI();
    };

    window.selectSlot = function(idx) {
        if (typeof userAnswers[currentIndex] === 'undefined') return;
        userAnswers[currentIndex][idx] = null;
        selectedSlotIdx = idx;
        if (typeof saveState === 'function') saveState();
        window.renderChoiceListQuestion(currentIndex);
    };

    window.moveToTarget = function(optIdx, groupIdx) {
        if (!userAnswers[currentIndex]) return;
        let targetIdx = (groupIdx !== undefined && groupIdx !== null) ? groupIdx : selectedSlotIdx;
        if (targetIdx === -1 || (groupIdx === undefined && userAnswers[currentIndex][targetIdx] !== null)) {
            targetIdx = userAnswers[currentIndex].indexOf(null);
        }
        if (targetIdx !== -1) {
            userAnswers[currentIndex][targetIdx] = optIdx;
            if (groupIdx === undefined || selectedSlotIdx === groupIdx) {
                selectedSlotIdx = userAnswers[currentIndex].indexOf(null);
            }
            if (typeof saveState === "function") saveState();
            window.renderChoiceListQuestion(currentIndex);
        }
    };

    window.submitChoiceList = function() {
        if (typeof incorrectSet === 'undefined') return;
        const item = (typeof quizData !== 'undefined') ? quizData[currentIndex] : examQuestions[currentIndex];
        const userIdxs = userAnswers[currentIndex] || [], correctAns = Array.isArray(item.answer) ? item.answer : [item.answer];
        let isCorrect = (userIdxs.length === correctAns.length && !userIdxs.includes(null));
        if (isCorrect) { 
            for (let i = 0; i < correctAns.length; i++) { if (userIdxs[i] !== parseAnswerToIndex(correctAns[i])) { isCorrect = false; break; } } 
        }
        if (isCorrect) { 
            if (incorrectSet.has(currentIndex)) { incorrectSet.delete(currentIndex); correctedSet.add(currentIndex); } 
            else { correctSet.add(currentIndex); } 
        }
        else { incorrectSet.add(currentIndex); }
        if (typeof saveState === 'function') saveState();
        window.renderChoiceListQuestion(currentIndex);
    };
})();
