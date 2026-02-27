import re

with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_prepare_print = r"""    function prepareAndPrint(onlyMistakes = false) {
        const area = document.getElementById('review-area');
        if (!area) return;
        area.style.display = 'block'; 
        const CUTOFF = REPLACE_CUTOFF;
        let title = "REPLACE_TITLE 認證完整解析";
        let targetItems = quizData.map((item, idx) => ({ item, idx }));
        if (onlyMistakes) {
            targetItems = targetItems.filter(({ idx }) => incorrectSet.has(idx) || correctedSet.has(idx));
            if (targetItems.length === 0) { alert('目前沒有錯題或訂正紀錄可供列印！'); return; }
            title = "REPLACE_TITLE 訂正解析講義";
        }

        // 1. 物理排序: Category -> ID
        targetItems.sort((a, b) => {
            const catA = String(a.item.category || "");
            const catB = String(b.item.category || "");
            const comp = catA.localeCompare(catB, undefined, {numeric: true});
            if (comp !== 0) return comp;
            return a.item.id - b.item.id;
        });

        area.innerHTML = `<h1 class="text-center mb-4" style="color:#212529">${title}</h1>`;
        targetItems.forEach(({ item, idx }, displayIdx) => {
            const displayId = item.id > CUTOFF ? `(${item.id})` : item.id;
            const div = document.createElement('div'); div.className = 'review-item';
            const optsRaw = item.quiz || item.options || [];
            const opts = Array.isArray(optsRaw) ? optsRaw : [optsRaw];
            const isNum = (item.labelType === 'num');
            const numStyle = (item.labelType === 'none' || item.hideLabel) ? 'style="display:none"' : '';
            
            let optHtml = "";
            if (item.type === 'matching') {
                optHtml += `<div class="matching-wrapper print-matching" id="print-match-${idx}" data-idx="${idx}" style="margin: 20px 0; position:relative; width:100%; display:block; -webkit-print-color-adjust:exact; print-color-adjust:exact;">
                    <div class="match-header-row" style="display:flex; justify-content:flex-start; gap:60px; margin:0 !important; margin-bottom:10px !important; border-bottom:1px solid #eee; padding:0 !important; padding-bottom:5px !important; padding-left:10px !important;">
                        <div class="match-header-title" style="font-weight:bold; color:#666; font-size:1.1rem; width:150px;">程式碼片段</div>
                        <div class="match-header-title" style="font-weight:bold; color:#666; font-size:1.1rem;">回答區</div>
                    </div>
                    <svg class="print-svg" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:1; overflow:visible; display:block;"></svg>
                    <div class="matching-columns" style="display:flex; justify-content:flex-start; gap:60px; position:relative; z-index:2; padding-left:10px;">
                        <div class="match-col left-col" style="display:flex; flex-direction:column; gap:25px; min-width:150px;">`;
                item.left.forEach((l, li) => {
                    optHtml += `<div class="match-item match-item-left" style="display:flex; align-items:center; min-height:45px; justify-content:flex-end; text-align:right;"><div style="font-family:Consolas,monospace;">${l}</div><div class="match-dot" id="pdl-${idx}-${li}" style="width:22px; height:22px; border:1.5px solid #333; border-radius:50%; margin:0 15px; display:flex; align-items:center; justify-content:center; background:#fff; position:relative; flex-shrink:0;"><div style="width:10px; height:10px; background:#333; border-radius:50%;"></div></div></div>`;
                });
                optHtml += `</div><div class="match-col right-col" style="display:flex; flex-direction:column; gap:25px; min-width:150px;">`;
                item.right.forEach((r, ri) => {
                    optHtml += `<div class="match-item match-item-right" style="display:flex; align-items:center; min-height:45px; justify-content:flex-start; text-align:left;"><div class="match-dot" id="pdr-${idx}-${ri}" style="width:22px; height:22px; border:1.5px solid #333; border-radius:50%; margin:0 15px; display:flex; align-items:center; justify-content:center; background:#fff; position:relative; flex-shrink:0;"><div style="width:10px; height:10px; background:#333; border-radius:50%;"></div></div><div style="font-family:Consolas,monospace;">${r}</div></div>`;
                });
                optHtml += `</div></div></div>`;
            } else {
                optHtml = opts.map((o, i) => {
                    if (String(o).includes('|')) {
                        const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                        const displayLabel = item["question" + alphabet[i]] || `選項 ${i + 1}`;
                        const subLabels = o.split('|').map((s, si) => `<span class="opt-num" ${numStyle}>(${isNum?(si+1):String.fromCharCode(65+si)})</span>${s}`).join(' ');
                        return `<div class="review-opt-line" style="margin-bottom:2px;"><span class="fw-bold">${displayLabel}</span> ${subLabels}</div>`;
                    } else {
                        return `<div class="review-opt-line" style="margin-bottom:2px;"><span class="opt-num" ${numStyle}>${isNum?(i+1)+'.':'('+String.fromCharCode(65+i)+')'} </span>${o}</div>`;
                    }
                }).join('');
            }

            let cleanQ = Array.isArray(item.question) ? [...item.question] : [String(item.question)];
            if (cleanQ.length > 0) cleanQ[0] = cleanQ[0].replace(/^((?:<[^>]+>)*)\d+\.\s*/, '    ');
            const ansText = (Array.isArray(item.answer)?item.answer:[item.answer]).map(a => {
                const indexValue = parseAnswerToIndex(a); return (indexValue < 0 || String(a).match(/[YN]/i)) ? a : (isNum ? (indexValue+1) : String.fromCharCode(65+indexValue));
            }).join(', ');
            // 使用排序後的 displayIdx 作為題號
            div.innerHTML = `<div class="review-q-text"><b>題目 ${displayIdx + 1} (物理編號: ${displayId})</b> <div class="q-content">${processContent(cleanQ, item)}</div></div>${item.image?`<div class="text-center my-2"><img src="${item.image}" class="q-img"></div>`:''}<div class="review-opts">${optHtml}</div><div class="review-ans">正確答案：${ansText}</div><div class="review-exp">${processContent(item.explanation || '暫無解析。', item)}</div>`;
            area.appendChild(div);
        });

        // 畫藍色連線
        setTimeout(() => {
            window.scrollTo(0, 0);
            document.querySelectorAll('.print-matching').forEach(wrapper => {
                const qIdx = parseInt(wrapper.getAttribute('data-idx'));
                const item = quizData[qIdx];
                const svg = wrapper.querySelector('.print-svg');
                
                const wRect = wrapper.getBoundingClientRect();
                if (wRect.width === 0) return;
                svg.setAttribute('width', wRect.width);
                svg.setAttribute('height', wRect.height);
                svg.style.width = wRect.width + 'px';
                svg.style.height = wRect.height + 'px';
                svg.innerHTML = ''; 
                
                const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
                answers.forEach((ansVal, lIdx) => {
                    const rIdx = parseAnswerToIndex(ansVal);
                    const dotL = document.getElementById(`pdl-${qIdx}-${lIdx}`);
                    const dotR = document.getElementById(`pdr-${qIdx}-${rIdx}`);
                    if (dotL && dotR) {
                        const recL = dotL.getBoundingClientRect(), recR = dotR.getBoundingClientRect();
                        const x1 = recL.left - wRect.left + recL.width/2;
                        const y1 = recL.top - wRect.top + recL.height/2;
                        const x2 = recR.left - wRect.left + recR.width/2;
                        const y2 = recR.top - wRect.top + recR.height/2;
                        
                        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                        line.setAttribute('x1', x1.toFixed(2)); line.setAttribute('y1', y1.toFixed(2)); 
                        line.setAttribute('x2', x2.toFixed(2)); line.setAttribute('y2', y2.toFixed(2));
                        line.setAttribute('stroke', "#0d6efd"); line.setAttribute('stroke-width', "2.5"); 
                        line.setAttribute('stroke-linecap', "round"); 
                        line.setAttribute('style', "stroke-opacity:1 !important;");
                        svg.appendChild(line);
                    }
                });
                const html = svg.innerHTML; svg.innerHTML = ''; svg.innerHTML = html;
            });
            if(window.Prism) Prism.highlightAll(); 
            setTimeout(() => { window.print(); }, 1000);
        }, 2000);
    }
"""

start_idx = content.find("    function prepareAndPrint(onlyMistakes = false) {")
end_idx = content.find("    function renderQuestion(index) {")

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_prepare_print + "\n" + content[end_idx:]

with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("PATCH 2 COMPLETE")
