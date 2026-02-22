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
                
                html += `<div class="sub-question-label">${customLabel || ('選項 ' + (optIdx + 1))}</div>`;
                
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