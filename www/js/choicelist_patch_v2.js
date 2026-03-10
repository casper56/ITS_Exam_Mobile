/* ChoiceList 全球通用統一補丁 V3.5.4 (答對隱藏框版) */
(function() {
    let selectedSlotIdx = -1;

    // --- 注入強力 CSS ---
    const style = document.createElement('style');
    style.innerHTML = `
        :root {
            --cl-pool-gap: 2px;
            --cl-gap: 2px;
            --cl-row-height: 2.6rem;
            --cl-padding: 0 12px;
            --cl-header-height: 30px;
        }
        .cl-header {
            font-weight: bold !important; color: #0d6efd !important;
            height: var(--cl-header-height) !important; line-height: var(--cl-header-height) !important;
            margin-bottom: 10px !important; border-bottom: 1px solid #ddd !important;
            width: fit-content !important; font-size: 0.8rem !important; padding-bottom: 2px !important;
        }
        .cl-items-container { display: flex !important; flex-direction: column !important; margin: 0 !important; padding: 0 !important; }
        .pool-area { gap: var(--cl-pool-gap) !important; }
        .target-area { gap: var(--cl-gap) !important; }

        .choicelist-item, .choicelist-code-line {
            display: block !important; 
            min-height: var(--cl-row-height) !important;
            padding: 8px 12px !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
            border-radius: 4px !important;
            white-space: pre-wrap !important; 
            word-break: break-all !important;
            overflow: visible !important;
            text-align: left !important;
        }
        .choicelist-item { background: #fff; border: 1px solid #ced4da; cursor: pointer; }
        .choicelist-code-line { border: 1px solid transparent; border-bottom: 1px solid #f0f0f0; }

        .choicelist-target { flex: none !important; width: fit-content !important; max-width: 75% !important; margin-left: 0 !important; }
        .target-bg { background: #f8f9fa !important; border-radius: 8px; padding: 4px !important; border: 1px solid #ddd !important; }
        .choicelist-pool { flex: none !important; width: fit-content !important; margin-right: 4px !important; }

        .target-slot.inline-slot, .choicelist-item.inline-item { 
            display: inline-flex !important; 
            align-items: center; 
            justify-content: flex-start !important; 
            height: 1.8rem !important; 
            line-height: 1 !important;
            vertical-align: middle !important; 
            padding: 0 8px !important; 
            margin: 0 4px !important;
            border-radius: 4px !important; 
            font-size: 0.95em !important;
            cursor: pointer !important; 
            position: relative; 
            z-index: 50;
            box-sizing: border-box !important;
            white-space: pre !important;
            text-align: left !important;
        }
        /* 已填入藍色框樣式 */
        .choicelist-item.inline-item { 
            background: #e7f1ff !important; 
            border: 2px solid #0d6efd !important; 
            border-left-width: 5px !important; 
            color: #0d6efd !important; 
        }
        /* 答對後隱藏框樣式 */
        .locked-slot {
            background: transparent !important;
            border: 1px solid transparent !important;
            color: #198754 !important; /* 綠色代表正確 */
            font-weight: bold !important;
            cursor: default !important;
        }
        
        .target-slot.inline-slot { background: #fff !important; border: 2px dashed #adb5bd !important; color: #6c757d !important; justify-content: center !important; }
        .active-slot { border: 2px solid red !important; background: #fff5f5 !important; box-shadow: 0 0 8px rgba(255,0,0,0.5) !important; color: red !important; }
        
        .opt-label { 
            display: inline-block !important; 
            font-weight: bold; 
            color: #6c757d; 
            margin-right: 10px; 
            border-right: 1px solid #dee2e6; 
            padding-right: 10px; 
            min-width: 1.5rem; 
            text-align: center; 
            line-height: 1.4 !important;
            vertical-align: middle !important;
        }

        .choicelist-wrapper { 
            display: flex !important; 
            flex-direction: row !important; 
            align-items: flex-start !important; 
            overflow-x: auto !important; 
            padding-bottom: 10px; 
            gap: 12px !important; 
        }
        /* 僅在寬度窄且為直立模式時，才切換為上下堆疊 */
        @media (max-width: 768px) and (orientation: portrait) {
            .choicelist-wrapper {
                flex-direction: column !important;
                overflow-x: visible !important;
            }
            .choicelist-pool, .choicelist-target {
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 0 15px 0 !important;
            }
        }
        .token { background: transparent !important; display: inline !important; white-space: pre !important; }
    `;
    document.head.appendChild(style);

    const stripCodeTags = (str) => {
        if (!str) return "";
        if (Array.isArray(str)) return str.map(stripCodeTags).join(" ");
        return str.replace(/<pre><code.*?>/g, '').replace(/<\/code><\/pre>/g, '').replace(/<code.*?>/g, '').replace(/<\/code>/g, '');
    };

    const highlightHardened = (text) => {
        if (!window.Prism || !text) return text;
        const hardened = text.replace(/ /g, '\u00a0');
        return Prism.highlight(hardened, Prism.languages.python, 'python');
    };

    const processContentLocal = (content, item) => {
        if (!content) return "";
        let html = content;
        // 1. 處理 [[image01]] 格式
        html = html.replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
            const num = parseInt(p1);
            const src = item['image' + num] || item['image' + p1] || item['image'] || `images/${p1}.png`;
            // 如果 src 不含路徑，補上 ./images/
            const finalSrc = (src.includes('/') || src.includes('\\')) ? src : `./images/${src}`;
            return `<img src="${finalSrc}" class="q-img" style="max-width:100%; height:auto; display:block; margin:10px 0;">`;
        });
        // 2. 處理 <code> 標籤
        html = html.replace(/<code>(.*?)<\/code>/g, '<code class="language-python">$1</code>');
        return html;
    };

    window.renderChoiceListQuestion = function(index) {
        const isMock = (typeof examQuestions !== 'undefined');
        const quizList = isMock ? examQuestions : quizData;
        const containerId = isMock ? 'question-area' : 'question-container';
        
        currentIndex = index; 
        const item = quizList[index];
        const container = document.getElementById(containerId);
        if (!container) return;

        const isCorrect = (typeof correctSet !== 'undefined') ? correctSet.has(index) : false;
        const isIncorrect = (typeof incorrectSet !== 'undefined') ? incorrectSet.has(index) : false;
        const isCorrected = (typeof correctedSet !== 'undefined') ? correctedSet.has(index) : false;
        const isReviewMode = !!(document.getElementById('review-list') && document.getElementById('review-list').innerHTML !== "");
        const isLocked = isMock ? isReviewMode : (isCorrect || isCorrected);

        const slotData = item.slots || item.slot;
        const requiredCount = (slotData && Array.isArray(slotData)) ? 
            slotData.join('').split('<slot').length - 1 : 1;

        if (!Array.isArray(userAnswers[index]) || userAnswers[index].length !== requiredCount) {
            userAnswers[index] = new Array(requiredCount).fill(null);
        }
        const currentAns = userAnswers[index];
        
        if (selectedSlotIdx === -1 || selectedSlotIdx >= requiredCount) {
            const firstEmpty = userAnswers[index].indexOf(null);
            selectedSlotIdx = (firstEmpty !== -1) ? firstEmpty : 0;
        }
        if (isLocked) selectedSlotIdx = -1;

        const szStr = item.sz || "0.85rem";
        const baseFontSize = parseFloat(szStr) * 16;
        const CHAR_W = baseFontSize * 0.62;
        const customSz = `font-size: ${szStr} !important; --sz: ${szStr} !important;`;

        // 1. 先找出所有選項中，最長一行的字元數 (考慮 \n 與 \t)
        // 支援分組選項：將 options 扁平化處理
        let globalMaxLen = 4;
        const flatOptions = item.options.flat(Infinity);
        flatOptions.forEach(opt => {
            const text = stripCodeTags(opt);
            const lines = text.split('\n');
            lines.forEach(line => {
                const processed = line.replace(/\t/g, '    ');
                if (processed.length > globalMaxLen) globalMaxLen = processed.length;
            });
        });

        // 2. 根據全域最長行計算統一的寬度 (V3.5.4 強化版)
        const unifiedW = Math.ceil((globalMaxLen + 4) * CHAR_W) + 20;
        const unifiedBoxStyle = `width: ${unifiedW}px !important; min-width: ${unifiedW}px !important;`;

        // 選項區渲染 (支援同時顯示多組分組選項)
        let poolHtml = `<div class="cl-header" style="width: 100%; border-bottom: 2px solid #0d6efd; margin-bottom: 10px; color: #0d6efd; font-weight: bold; padding-bottom: 5px;">選項區</div>`;
        const isGrouped = Array.isArray(item.options[0]);
        
        if (isGrouped) {
            item.options.forEach((group, gIdx) => {
                const isActiveGroup = (selectedSlotIdx === gIdx && !isLocked);
                const activeStyle = isActiveGroup ? 'border: 2px solid #0d6efd !important; border-radius: 8px; background: #f0f7ff !important; padding: 8px !important; margin-bottom: 15px !important;' : 'margin-bottom: 15px !important;';
                
                poolHtml += `<div class="grouped-pool-unit" style="${activeStyle}">`;
                poolHtml += `<div style="font-weight:bold; color:#666; margin-bottom:8px; font-size:0.85rem;">[ 選項 ${gIdx + 1} ]</div>`;
                poolHtml += `<div class="cl-items-container pool-area">`;
                group.forEach((opt, optIdx) => {
                    const label = String.fromCharCode(65 + optIdx);
                    const cleanText = stripCodeTags(opt);
                    poolHtml += `<div class="choicelist-item ${isLocked ? 'disabled' : ''}" style="${customSz} ${unifiedBoxStyle} ${isLocked ? 'cursor: default !important;' : ''}" onclick="${isLocked ? '' : `window.moveToTarget(${optIdx}, ${gIdx})`}"><span class="opt-label">${label}</span><span style="white-space:pre !important;">${highlightHardened(cleanText)}</span></div>`;
                });
                poolHtml += `</div></div>`;
            });
        } else {
            poolHtml += `<div class="cl-items-container pool-area">`;
            item.options.forEach((opt, idx) => {
                const label = String.fromCharCode(65 + idx);
                const cleanText = stripCodeTags(opt);
                poolHtml += `<div class="choicelist-item ${isLocked ? 'disabled' : ''}" style="${customSz} ${unifiedBoxStyle} ${isLocked ? 'cursor: default !important;' : ''}" onclick="${isLocked ? '' : `window.moveToTarget(${idx})`}"><span class="opt-label">${label}</span><span style="white-space:pre !important;">${highlightHardened(cleanText)}</span></div>`;
            });
            poolHtml += `</div>`;
        }

        // 回答區渲染 (V3.5.4 標準：嵌入式標題)
        let targetHtml = `<div class="cl-header" style="width: 100%; border-bottom: 2px solid #0d6efd; margin-bottom: 10px; color: #0d6efd; font-weight: bold; padding-bottom: 5px;">回答區</div><div class="target-bg" style="background:#f8f9fa; border-radius:8px; padding:10px; border:1px solid #ddd;">`;
        if (slotData) {
            let sIdxCounter = 0;
            slotData.forEach(line => {
                const rawLine = stripCodeTags(line);
                const segments = rawLine.split(/<slot\d*>/);
                let lineFinalHtml = '';
                segments.forEach((seg, i) => {
                    lineFinalHtml += highlightHardened(seg);
                    if (i < segments.length - 1) {
                        const sIdx = sIdxCounter++;
                        const optIdx = currentAns[sIdx], isActive = (selectedSlotIdx === sIdx && !isLocked);
                        const clickHandler = isLocked ? '' : `onclick="event.stopPropagation(); window.selectSlot(${sIdx})"`;
                        
                        if (optIdx !== null && optIdx !== undefined) {
                            const cls = isLocked ? 'locked-slot' : 'choicelist-item inline-item';
                            const filledOpt = isGrouped ? item.options[sIdx][optIdx] : item.options[optIdx];
                            const filledText = stripCodeTags(filledOpt);
                            lineFinalHtml += `<span class="${cls} ${isActive ? 'active-slot' : ''}" style="${unifiedBoxStyle}" ${clickHandler}>${highlightHardened(filledText)}</span>`;
                        } else {
                            lineFinalHtml += `<span class="target-slot inline-slot ${isActive ? 'active-slot' : ''}" style="${unifiedBoxStyle}" ${clickHandler}>[ 選項 ${sIdx + 1} ]</span>`;
                        }
                    }
                });
                targetHtml += `<div class="choicelist-code-line" style="${customSz}">${lineFinalHtml}</div>`;
            });
        }
        targetHtml += `</div>`;

        let statusTextHtml = '';
        let cardClass = 'card question-card';
        if (isCorrect) { statusTextHtml = '<div class="alert alert-success py-1 px-2 mb-2 fw-bold">答對了 ✅</div>'; cardClass += ' correct'; }
        else if (isCorrected) { statusTextHtml = '<div class="alert alert-warning py-1 px-2 mb-2 fw-bold text-dark">已修正 ⚠️</div>'; cardClass += ' corrected'; }
        else if (isIncorrect) { statusTextHtml = '<div class="alert alert-danger py-1 px-2 mb-2 fw-bold">答錯了 ❌</div>'; cardClass += ' incorrect'; }

        container.innerHTML = `<div class="${cardClass}">
            <div class="question-header"><div><span class="badge bg-primary me-2">題目 ${index + 1} / ${quizList.length}</span><span class="badge bg-info">填空題 (ChoiceList)</span></div><div class="category-tag">${item.category || '一般'}</div></div>
            <div class="question-body" style="padding-bottom:0;"><div class="choicelist-q-text">${processContent(item.question, item)}</div></div>
            <div class="px-3 pb-3">
                <div class="choicelist-wrapper" style="display:flex; gap:25px; align-items:flex-start;">
                    <div class="choicelist-pool" style="flex:0 0 auto;">
                        ${poolHtml}
                    </div>
                    <div class="choicelist-target" style="flex:1 1 auto; min-width:0;">
                        ${targetHtml}
                    </div>
                </div>
                ${(!isLocked && !isMock) ? `<div class="text-center mt-4 pt-3 border-top"><button class="btn btn-primary px-5" id="choicelist-submit-btn" onclick="window.submitChoiceList()">確認提交</button></div>` : ''}
                <div class="answer-section" id="choicelist-ans-section" style="${isLocked || isIncorrect ? 'display:block' : 'display:none'}">
                    ${statusTextHtml}
                    <h6 class="fw-bold mb-3">正確順序如下：</h6>
                    <div class="mb-3">${(Array.isArray(item.answer) ? item.answer : [item.answer]).map((val, ansIdx) => {
                        const idx = parseAnswerToIndex(val);
                        const optText = isGrouped ? item.options[ansIdx][idx] : item.options[idx];
                        return `<div class="mt-2 border-start border-success border-4 bg-light p-2 font-monospace"><span class="badge bg-secondary me-2">${String.fromCharCode(65 + idx)}</span>${stripCodeTags(optText) || val}</div>`;
                    }).join('')}</div>
                    <div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div>
                </div>
            </div>
        </div>`;

        // --- 強制控制導覽按鈕顯示 ---
        const sidePrev = document.getElementById('side-btn-prev');
        const sideNext = document.getElementById('side-btn-next');
        if (sidePrev) sidePrev.style.display = (index === 0) ? 'none' : 'flex';
        if (sideNext) sideNext.style.display = 'flex';
        
        if(typeof updateUI === 'function') updateUI();
    };

    window.selectSlot = function(idx) {
        if (typeof userAnswers[currentIndex] === 'undefined') return;
        userAnswers[currentIndex][idx] = null;
        selectedSlotIdx = idx;
        console.log(`[ChoiceList Debug] 選項位置 ${idx} 已清空。目前 Q${currentIndex} 答題紀錄:`, userAnswers[currentIndex]);
        if (typeof saveState === 'function') saveState();
        window.renderChoiceListQuestion(currentIndex);
    };

    window.moveToTarget = function(optIdx, groupIdx = null) {
        if (!userAnswers[currentIndex]) return;
        
        // 如果傳入了 groupIdx，則優先填入該選項位置；否則使用全域選中的 selectedSlotIdx
        let targetIdx = (groupIdx !== null) ? groupIdx : selectedSlotIdx;
        
        // 如果 targetIdx 已經有值，或者尚未選中任何選項位置，則找第一個空的
        if (targetIdx === -1 || (groupIdx === null && userAnswers[currentIndex][targetIdx] !== null)) {
            targetIdx = userAnswers[currentIndex].indexOf(null);
        }
        
        if (targetIdx !== -1) {
            userAnswers[currentIndex][targetIdx] = optIdx;
            
            // 自動跳轉到下一個空格
            if (groupIdx === null || selectedSlotIdx === groupIdx) {
                selectedSlotIdx = userAnswers[currentIndex].indexOf(null);
            }
            
            console.log(`[ChoiceList Debug] 選項 ${String.fromCharCode(65 + optIdx)} 已填入位置 ${targetIdx}。目前 Q${currentIndex} 答題紀錄:`, userAnswers[currentIndex]);
            if (typeof saveState === 'function') saveState();
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
