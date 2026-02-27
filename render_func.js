    let currentSelection = { side: null, index: null };
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || (window.innerWidth <= 768);

    function parseAnswerToIndex(val) {
        if (typeof val === 'number') return val - 1;
        if (typeof val === 'string') {
            const v = val.toUpperCase();
            if (v === 'Y') return 0; if (v === 'N') return 1;
            const code = v.charCodeAt(0);
            if (code >= 65 && code <= 90) return code - 65;
            return parseInt(val) - 1;
        }
        return -1;
    }

    function renderMatchingQuestion(item, index, savedAns) {
        const container = document.getElementById('question-area');
        let qText = item.question.replace(/^\d+\.\s*/, '');
        
        // 初始化答案
        if (!userAnswers[index]) userAnswers[index] = new Array(item.left.length).fill(null);
        const currentAns = userAnswers[index];

        let html = `<div class="card question-card">
            <div class="question-header">Question ${index + 1} / 50 <span class="badge bg-light text-dark float-end">${item.category || ''}</span></div>
            <div class="question-body" style="color:#000;">
                <div class="mb-4" style="font-weight:500; font-size:1.1rem; line-height:1.6; white-space: pre-wrap;">${qText}</div>`;
        
        if (item.image) html += `<div class="text-center mb-4"><img src="${item.image}" style="max-width:100%; border:1px solid #ddd;"></div>`;
        
        html += `<div class="mt-4 pt-3" style="border-top: 1px dashed #ccc;"><h6 class="fw-bold text-dark mb-3">📍 拖拉/點選配對區 (${isMobile ? '手機模式: 請依序點選左側與右側' : '電腦模式: 支援拖拉或點選'})</h6>`;
        
        html += `<div class="matching-container d-flex flex-column gap-3">`;
        
        item.left.forEach((leftText, lIdx) => {
            const matchedRightIdx = currentAns[lIdx];
            const rightText = matchedRightIdx !== null ? item.right[matchedRightIdx] : "請點選右側選項或拖曳至此";
            const isMatchSelected = (currentSelection.side === 'left' && currentSelection.index === lIdx);

            html += `
            <div class="match-row d-flex align-items-stretch gap-2" style="min-height: 60px;">
                <div class="match-left flex-fill p-2 border rounded ${isMatchSelected ? 'bg-primary text-white border-primary' : 'bg-light'}" 
                     onclick="selectMatch('left', ${lIdx})" 
                     ondrop="dropMatch(event, ${lIdx})" ondragover="allowDrop(event)"
                     style="cursor:pointer; display:flex; align-items:center;">
                    ${leftText}
                </div>
                <div class="match-connector d-flex align-items-center">
                    <i class="bi bi-arrow-right-short fs-4"></i>
                </div>
                <div class="match-right flex-fill p-2 border rounded ${matchedRightIdx !== null ? 'border-success bg-white' : 'border-dashed text-muted'}" 
                     style="display:flex; align-items:center; min-width: 150px; position:relative;">
                    ${rightText}
                    ${matchedRightIdx !== null ? `<span class="badge bg-danger position-absolute top-0 end-0 m-1" onclick="clearMatch(${lIdx}); event.stopPropagation();" style="cursor:pointer;">&times;</span>` : ''}
                </div>
            </div>`;
        });

        html += `</div>`;
        
        // 右側候選清單
        html += `<div class="mt-4 mb-2"><small class="text-secondary fw-bold">可選項目：</small></div>
                 <div class="d-flex flex-wrap gap-2">`;
        
        item.right.forEach((rightText, rIdx) => {
            const isUsed = currentAns.includes(rIdx);
            const isMatchSelected = (currentSelection.side === 'right' && currentSelection.index === rIdx);
            
            html += `
            <div class="option-pill p-2 border rounded ${isUsed ? 'opacity-50' : 'bg-white shadow-sm'} ${isMatchSelected ? 'border-primary ring' : ''}" 
                 draggable="${!isUsed}" ondragstart="dragStart(event, ${rIdx})"
                 onclick="${isUsed ? '' : `selectMatch('right', ${rIdx})`}"
                 style="cursor:${isUsed ? 'not-allowed' : 'pointer'}; font-size: 0.9rem;">
                ${rightText}
            </div>`;
        });
        
        html += `</div></div></div></div>`;
        container.innerHTML = html;
        Prism.highlightAll();
    }

    window.selectMatch = function(side, idx) {
        if (currentSelection.side === side) {
            currentSelection = { side, index: idx }; // 切換同側選取
        } else if (currentSelection.side === null) {
            currentSelection = { side, index: idx };
        } else {
            // 不同側，執行連線
            const leftIdx = side === 'left' ? idx : currentSelection.index;
            const rightIdx = side === 'right' ? idx : currentSelection.index;
            
            userAnswers[currentIndex][leftIdx] = rightIdx;
            currentSelection = { side: null, index: null };
            renderQuestion(currentIndex);
        }
        renderQuestion(currentIndex);
    };

    window.clearMatch = function(lIdx) {
        userAnswers[currentIndex][lIdx] = null;
        renderQuestion(currentIndex);
    };

    window.allowDrop = (e) => e.preventDefault();
    window.dragStart = (e, rIdx) => e.dataTransfer.setData("text", rIdx);
    window.dropMatch = (e, lIdx) => {
        e.preventDefault();
        const rIdx = parseInt(e.dataTransfer.getData("text"));
        userAnswers[currentIndex][lIdx] = rIdx;
        renderQuestion(currentIndex);
    };

    function renderQuestion(index) {
        currentIndex = index;
        const item = examQuestions[index];
        const container = document.getElementById('question-area');
        container.innerHTML = '';
        document.getElementById('q-progress').innerText = `題目 ${index + 1} / 50`;
        
        // 更新固定按鈕狀態
        const prevBtn = document.getElementById('btn-prev');
        const nextBtn = document.getElementById('btn-next');
        if (index === 0) prevBtn.classList.add('disabled'); else prevBtn.classList.remove('disabled');
        
        nextBtn.innerHTML = '❯';
        if (index === 49) {
            nextBtn.classList.add('btn-success', 'text-white');
            nextBtn.title = "完成答題並交卷";
        } else {
            nextBtn.classList.remove('btn-success', 'text-white');
            nextBtn.title = "下一題";
        }

        // 分流：配對題
        if (item.type === 'matching') {
            renderMatchingQuestion(item, index, userAnswers[index]);
            return;
        }

        // 常規處理：僅移除數字編號，交給 CSS (pre-wrap) 處理換行
        let qText = item.question.replace(/^\d+\.\s*/, '');
            
        let html = `<div class="card question-card">
            <div class="question-header">Question ${index + 1} / 50 <span class="badge bg-light text-dark float-end">${item.category || ''}</span></div>
            <div class="question-body" style="color:#000; white-space: pre-wrap;">
                <div class="mb-4" style="font-weight:500; font-size:1.1rem; line-height:1.6;">${qText}</div>`;
        
        if (item.image) html += `<div class="text-center mb-4"><img src="${item.image}" style="max-width:100%; border:1px solid #ddd;"></div>`;
        
        const options = item.quiz || item.options || [];
        const savedAns = userAnswers[index];
        
        // 確保答題區與題目區有物理間隔
        html += '<div class="mt-4 pt-3" style="border-top: 1px dashed #ccc;"><h6 class="fw-bold text-dark mb-3">📍 答題區</h6>';
        
        options.forEach((opt, optIdx) => {
            const optStr = String(opt);
            
            // 預設為 Alpha (A), 只有明確設為 'num' 才用 1.
            let labelText = `(${String.fromCharCode(65 + optIdx)}) `;
            if (item.labelType === 'num') {
                labelText = `${optIdx + 1}. `;
            }
            const numStyle = (item.labelType === 'none' || item.hideLabel) ? 'style="display:none"' : '';

            if (optStr.includes('|')) {
                const parts = optStr.split('|');
                
                // 優先使用 questionA, questionB... 作為標籤
                const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                const customLabelField = "question" + alphabet[optIdx];
                let customLabel = "";
                if (item[customLabelField]) {
                    customLabel = Array.isArray(item[customLabelField]) ? item[customLabelField].join('<br>') : item[customLabelField];
                }
                
                html += `<div class="mt-2 mb-1"><code>${customLabel || ('選項 ' + (optIdx + 1))}</code></div>`;
                
                let sIdx = 0;
                // 智慧標題：如果超過 3 個字且不是單一字母/數字/YesNo 才是標題
                const isShort = parts[0].trim().length <= 3 || /^[A-G]$|^\d+$|^Yes$|^No$|^True$|^False/i.test(parts[0].trim());
                if (!isShort) {
                    html += `<div class="mb-2 ms-2" style="font-size:1.05rem; border-left:4px solid #0d6efd; padding-left:12px; background:#f0f7ff; padding:5px 12px; border-radius:4px;">${parts[0]}</div>`;
                    sIdx = 1;
                }

                html += '<div class="d-flex flex-wrap gap-2 mb-3 ms-2">';
                for (let i = sIdx; i < parts.length; i++) {
                    const btnIdx = i - sIdx;
                    const isSel = (savedAns && savedAns[optIdx] === btnIdx);
                    // 子選項也同步預設 Alpha
                    let subLabel = `(${String.fromCharCode(65 + btnIdx)}) `;
                    if (item.labelType === 'num') subLabel = `(${btnIdx+1}) `;
                    
                    html += `<div class="sub-opt-container ${isSel ? 'selected' : ''}" onclick="selectSub(${optIdx}, ${btnIdx})"><span class="opt-num" ${numStyle}>${subLabel}</span>${parts[i]}</div>`;
                }
                html += '</div>';
            } else {
                const isSel = Array.isArray(savedAns) ? savedAns.includes(optIdx) : savedAns === optIdx;
                html += `<div class="option-item ${isSel ? 'selected' : ''}" onclick="selectOption(${optIdx})"><span class="opt-num" ${numStyle}>${labelText}</span>${optStr}</div>`;
            }
        });
        html += '</div></div></div>';
        container.innerHTML = html;
        Prism.highlightAll();
    }