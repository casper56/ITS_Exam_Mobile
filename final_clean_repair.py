import json
import os
import re
import glob
import time

def clean_repair_all():
    subject_dirs = [d for d in os.listdir('www') if os.path.isdir(os.path.join('www', d)) and d != 'assets']
    title_map = { "AI900": "Microsoft AI-900", "AZ900": "Microsoft AZ-900", "Generative_AI": "Generative AI Foundations", "ITS_AI": "ITS Artificial Intelligence", "ITS_Database": "ITS Database Administration", "ITS_Python": "ITS Python Programming", "ITS_softdevelop": "ITS Software Development" }

    html_template = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{DISPLAY_TITLE}} 模擬測驗</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-solarized-light.min.css" rel="stylesheet" />
    <style>
        body { background-color: #f8f9fa; font-family: "Microsoft JhengHei", "Segoe UI", sans-serif; }
        .main-wrapper { display: flex; min-height: 100vh; }
        .sidebar { width: 280px; background: #fff; border-right: 1px solid #dee2e6; display: flex; flex-direction: column; position: fixed; top: 0; bottom: 0; left: 0; z-index: 1000; transition: transform 0.3s ease; }
        .sidebar-header { background: #212529; color: #fff; padding: 15px; border-bottom: 1px solid #dee2e6; }
        .sidebar-header h5 { font-size: 1.25rem; font-weight: bold; color: #fff; margin-bottom: 0; }
        #progress-stats { font-size: 1.2rem; font-weight: bold; color: #fff; }
        .sidebar-content { flex: 1; overflow-y: auto; padding: 15px; }
        .sidebar-footer { padding: 15px; border-top: 1px solid #dee2e6; background: #f8f9fa; }
        .content-area { flex: 1; margin-left: 280px; padding: 20px; transition: margin-left 0.3s ease; }
        code { color: inherit !important; background-color: transparent !important; }
        pre { background-color: transparent !important; border: none !important; }
        .form-check-input { border-radius: 50% !important; width: 1.2rem; height: 1.2rem; background-image: none !important; cursor: pointer; }
        .form-check-input:checked { background-color: #0d6efd !important; border-color: #0d6efd !important; }
        .option-item { border: 1px solid #e9ecef; border-radius: 6px; padding: 10px; margin-bottom: 8px; cursor: pointer; transition: 0.2s; }
        .option-item.correct, .sub-opt-container.correct { background-color: #d1e7dd !important; border-color: #badbcc !important; color: #0f5132 !important; }
        .option-item.incorrect, .sub-opt-container.incorrect { background-color: #f8d7da !important; border-color: #f5c2c7 !important; color: #842029 !important; }
        .sub-opt-container.selected { background-color: #e7f1ff !important; border-color: #9ec5fe !important; }
        .q-node { aspect-ratio: 1; display: flex; align-items: center; justify-content: center; border: 1px solid #dee2e6; border-radius: 6px; background-color: #fff; cursor: pointer; font-size: 0.85rem; }
        .q-node.correct { background-color: #d1e7dd; color: #0f5132; }
        .q-node.incorrect { background-color: #f8d7da; color: #842029; }
        .q-node.corrected { background-color: #fd7e14; color: #fff; }
        .q-node.active { background-color: #0d6efd; color: white; transform: scale(1.1); z-index: 1; }
        .progress-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }
        .category-tag { font-size: 0.8rem; color: #6c757d; background-color: #f8f9fa; padding: 2px 8px; border-radius: 12px; border: 1px solid #dee2e6; margin-top: 5px; display: inline-block; }
        .type-badge { font-size: 0.75rem; vertical-align: middle; }
        .question-card { border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: #fff; border-radius: 8px; }
        .question-header { border-bottom: 2px solid #0d6efd; padding: 15px 20px; font-weight: bold; color: #0d6efd; display: flex; justify-content: space-between; align-items: center; }
        .question-body { padding: 20px; font-size: 1.05rem; }
        .answer-section { display: none; margin-top: 20px; padding: 20px; background: #fff; border: 2px solid #0d6efd; border-radius: 8px; }
        .q-img { max-width: 100%; height: auto; border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); margin: 5px auto; display: block; }
        #review-area { display: none; text-align: left; padding: 20px; background: white; }
        .review-item { margin-bottom: 40px; padding: 0; border: none; background: white; page-break-inside: auto; border-bottom: 1px solid #eee; padding-bottom: 20px; }
        .review-q-text { font-size: 1.1rem; line-height: 1.6; margin-bottom: 15px; color: #333; }
        .review-ans { color: #198754; font-weight: bold; padding: 10px 15px; margin: 20px 0; border-left: 5px solid #198754; background: white; font-size: 1.1rem; }
        .review-exp-box { background: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #eeeeee; line-height: 1.8; color: #333; }
        @media print { 
            @page { size: auto; margin: 8mm; }
            body { background: white !important; font-size: 13px; line-height: 1.4 !important; } 
            .main-wrapper, .mobile-toggle, .side-nav-btn { display: none !important; } 
            #review-area { display: block !important; } 
            .review-item { margin-bottom: 20px !important; padding-bottom: 15px !important; border-bottom: 1px solid #eee !important; }
            .review-q-text { font-size: 1rem !important; margin-bottom: 8px !important; }
            .review-ans { font-size: 0.95rem !important; margin: 10px 0 !important; padding: 5px 10px !important; border-left-width: 4px !important; }
            .review-exp-box { font-size: 0.9rem !important; padding: 12px !important; border-radius: 6px !important; background: #fafafa !important; }
            .review-opt-line { margin-bottom: 2px !important; }
            .q-img { max-width: 300px !important; margin: 10px 0 !important; }
            h1 { font-size: 1.5rem !important; margin-bottom: 20px !important; }
        }
        .side-nav-btn { position: fixed; top: 50%; left: 280px; transform: translateY(-50%); width: 40px; height: 80px; background: rgba(13, 110, 253, 0.8); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 1100; border-radius: 0 40px 40px 0; transition: left 0.3s ease; }
        .side-nav-next { left: auto; right: 0; border-radius: 40px 0 0 40px; }
        @media (max-width: 992px) { 
            .sidebar { transform: translateX(-100%); } 
            .sidebar.active { transform: translateX(0); } 
            .content-area { margin-left: 0; } 
            .mobile-toggle { display: block !important; } 
            .side-nav-btn#side-btn-prev { left: 0; }
            .sidebar.active ~ .side-nav-btn#side-btn-prev { left: 280px; }
        }
        .mobile-toggle { display: none; position: fixed; bottom: 20px; right: 20px; z-index: 1100; width: 50px; height: 50px; border-radius: 50%; background: #212529; color: white; border: none; }
    </style>
</head>
<body>
<div class="main-wrapper">
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="d-flex align-items-center justify-content-between mb-2">
                <div class="d-flex align-items-center"><a href="../index.html" class="text-decoration-none text-white me-2">🏠</a><h5 class="m-0">題目列表</h5></div>
                <button type="button" onclick="prepareAndPrint()" class="btn btn-outline-light btn-sm py-0 px-2" style="font-size: 0.75rem;">📄 列印預覽</button>
            </div>
            <div id="progress-stats">✅0 ❌0 🟠0 / {{TOTAL}}</div>
        </div>
        <div class="sidebar-content">
            <div class="d-flex justify-content-between small mb-3 text-muted">
                <span><span style="display:inline-block;width:10px;height:10px;background:#fff;border:1px solid #ccc"></span> 未讀</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#d1e7dd"></span> 答對</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#f8d7da"></span> 答錯</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#fd7e14"></span> 訂正</span>
            </div>
            <div class="progress-grid" id="progress-grid"></div>
        </div>
        <div class="sidebar-footer"><button class="btn btn-outline-danger btn-sm w-100" onclick="resetProgress()">🗑️ 重置進度</button></div>
    </nav>
    <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>
    <div class="side-nav-btn" id="side-btn-prev" onclick="prevQuestion()">&#10094;</div>
    <div class="side-nav-btn side-nav-next" id="side-btn-next" onclick="nextQuestion()">&#10095;</div>
    <main class="content-area"><div class="container-fluid" style="max-width: 900px;"><div id="question-container"></div></div></main>
</div>
<div id="review-area"></div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-csharp.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
<script>
    const quizData = {{QUIZ_DATA}};
    let currentIndex = 0;
    let correctSet = new Set(), incorrectSet = new Set(), correctedSet = new Set(), userAnswers = {}; 
    const CORR_KEY = '{{CORR_KEY}}', INCORR_KEY = '{{INCORR_KEY}}', CORR_EDIT_KEY = '{{CORR_EDIT_KEY}}', INDEX_KEY = '{{INDEX_KEY}}', ANSWERS_KEY = '{{ANSWERS_KEY}}';

    function loadState() {
        const sCorr = localStorage.getItem(CORR_KEY), sIncorr = localStorage.getItem(INCORR_KEY), sEdit = localStorage.getItem(CORR_EDIT_KEY), sIdx = localStorage.getItem(INDEX_KEY), sAns = localStorage.getItem(ANSWERS_KEY);
        if (sCorr) correctSet = new Set(JSON.parse(sCorr));
        if (sIncorr) incorrectSet = new Set(JSON.parse(sIncorr));
        if (sEdit) correctedSet = new Set(JSON.parse(sEdit));
        if (sIdx) currentIndex = parseInt(sIdx) || 0;
        if (sAns) userAnswers = JSON.parse(sAns);
    }
    function saveState() {
        localStorage.setItem(CORR_KEY, JSON.stringify([...correctSet]));
        localStorage.setItem(INCORR_KEY, JSON.stringify([...incorrectSet]));
        localStorage.setItem(CORR_EDIT_KEY, JSON.stringify([...correctedSet]));
        localStorage.setItem(INDEX_KEY, currentIndex.toString());
        localStorage.setItem(ANSWERS_KEY, JSON.stringify(userAnswers));
    }
    function resetProgress() { if(confirm('確定清除紀錄嗎？')) { localStorage.clear(); location.reload(); } }
    function toggleSidebar() { document.getElementById('sidebar').classList.toggle('active'); }

    function processContent(content, item) {
        if (!content) return '';
        const lines = Array.isArray(content) ? content : [String(content)];
        return lines.map(line => {
            let html = String(line);
            html = html.replace(/\[\[image(\d+)\]\]/g, (match, p1) => {
                const src = item['image' + p1];
                return src ? `<img src="${src}" class="q-img">` : match;
            });
            if (html.includes('●')) {
                const parts = html.split('●').map(p => p.trim()).filter(p => p);
                return parts.map(p => `<div class="mb-1">● ${p}</div>`).join('');
            }
            return `<div>${html}</div>`;
        }).join('');
    }

    function toggleExplanation(forceShow = null) {
        const el = document.getElementById('ans-section'), btn = document.getElementById('toggle-exp-btn');
        if (!el || !btn) return;
        const isShow = (forceShow !== null) ? forceShow : (el.style.display !== 'block');
        el.style.display = isShow ? 'block' : 'none';
    }

    function checkAnswer(element, qIdx, optIdx, event) {
        const item = quizData[qIdx], isMultiple = item.type === 'multiple';
        let answers = item.answer; if (!Array.isArray(answers)) answers = [answers];
        const correctIndices = answers.map(a => parseInt(a) - 1);
        const input = element.querySelector('input');
        if (event && event.target !== input) { if (isMultiple) input.checked = !input.checked; else input.checked = true; }
        
        if (isMultiple) {
            const inputs = document.querySelectorAll(`input[name="q${qIdx}"]`);
            let selected = []; inputs.forEach((inp, idx) => { if (inp.checked) selected.push(idx); });
            userAnswers[qIdx] = selected;
            element.classList.toggle('correct', input.checked && correctIndices.includes(optIdx));
            element.classList.toggle('incorrect', input.checked && !correctIndices.includes(optIdx));
            const isPerfect = selected.length === correctIndices.length && selected.every(v => correctIndices.includes(v));
            const anyWrong = selected.some(v => !correctIndices.includes(v));
            if (isPerfect) {
                if (incorrectSet.has(qIdx)) { incorrectSet.delete(qIdx); correctedSet.add(qIdx); }
                else if (!correctedSet.has(qIdx)) { correctSet.add(qIdx); }
                inputs.forEach(i => i.disabled = true);
                toggleExplanation(true);
            } else if (anyWrong || selected.length > correctIndices.length) {
                incorrectSet.add(qIdx); correctSet.delete(qIdx); correctedSet.delete(qIdx);
            }
        } else {
            if (correctSet.has(qIdx) || correctedSet.has(qIdx)) return;
            userAnswers[qIdx] = optIdx;
            if (correctIndices.includes(optIdx)) {
                element.classList.add('correct');
                if (incorrectSet.has(qIdx)) { incorrectSet.delete(qIdx); correctedSet.add(qIdx); }
                else { correctSet.add(qIdx); }
                document.querySelectorAll(`input[name="q${qIdx}"]`).forEach(i => i.disabled = true);
            } else {
                element.classList.add('incorrect'); incorrectSet.add(qIdx);
                const ci = document.getElementById(`o${correctIndices[0]}`); if (ci) ci.closest('.option-item').classList.add('correct');
            }
            toggleExplanation(true);
        }
        saveState(); updateUI();
    }

    function checkSubAnswer(element, qIdx, optIdx, subIdx, event) {
        const item = quizData[qIdx];
        let answers = item.answer; if (!Array.isArray(answers)) answers = [answers];
        const correctSubIdx = parseInt(answers[optIdx]) - 1, input = element.querySelector('input');
        if (event && event.target !== input) input.checked = true;
        if (!userAnswers[qIdx]) userAnswers[qIdx] = {};
        userAnswers[qIdx][optIdx] = subIdx;
        
        // 移除同題組其他選項的選中樣式
        element.parentElement.querySelectorAll('.sub-opt-container').forEach(el => el.classList.remove('selected'));
        element.classList.add('selected');

        if (subIdx === correctSubIdx) {
            element.classList.add('correct');
            const totalSub = (item.quiz || item.options || []).length;
            const curCorrect = document.querySelectorAll('.sub-opt-container.correct').length;
            if (curCorrect === totalSub) {
                if (incorrectSet.has(qIdx)) { incorrectSet.delete(qIdx); correctedSet.add(qIdx); }
                else if (!correctedSet.has(qIdx)) { correctSet.add(qIdx); }
                toggleExplanation(true);
            }
            document.querySelectorAll(`input[name="q${qIdx}_opt${optIdx}"]`).forEach(i => i.disabled = true);
        } else {
            element.classList.add('incorrect'); incorrectSet.add(qIdx);
            const ci = document.getElementById(`o${optIdx}_s${correctSubIdx}`); if (ci) ci.parentElement.classList.add('correct');
            toggleExplanation(true);
        }
        saveState(); updateUI();
    }

    function evaluateCurrentQuestion() {
        const item = quizData[currentIndex], qIdx = currentIndex;
        if (correctSet.has(qIdx) || correctedSet.has(qIdx) || incorrectSet.has(qIdx)) return;
        const saved = userAnswers[qIdx]; if (!saved) return; 
        let answers = item.answer; if (!Array.isArray(answers)) answers = [answers];
        const correctIndices = answers.map(a => parseInt(a) - 1);
        if (item.type === 'multiple') {
            const selected = Array.isArray(saved) ? saved : []; if (selected.length === 0) return;
            const isPerfect = selected.length === correctIndices.length && selected.every(v => correctIndices.includes(v));
            if (isPerfect) correctSet.add(qIdx); else incorrectSet.add(qIdx);
        } else if (String(item.quiz || item.options || "").includes('|')) {
            const savedKeys = typeof saved === 'object' ? Object.keys(saved) : []; if (savedKeys.length === 0) return;
            const totalSub = (item.quiz || item.options || []).length;
            let allCorrect = (savedKeys.length === totalSub);
            if (allCorrect) { for(let i=0; i<totalSub; i++) if ((parseInt(saved[i]) + 1) != parseInt(answers[i])) { allCorrect = false; break; } }
            if (allCorrect) correctSet.add(qIdx); else incorrectSet.add(qIdx);
        }
        saveState(); updateUI();
    }

    function nextQuestion() { evaluateCurrentQuestion(); if (currentIndex < quizData.length-1) renderQuestion(currentIndex+1); }
    function prevQuestion() { evaluateCurrentQuestion(); if (currentIndex > 0) renderQuestion(currentIndex-1); }
    function jumpTo(idx) { evaluateCurrentQuestion(); renderQuestion(idx); }

    function prepareAndPrint() {
        const area = document.getElementById('review-area');
        area.innerHTML = `<h1 class="text-center mb-4" style="color:#212529">{{DISPLAY_TITLE}} 完整解析講義</h1>`;
        quizData.forEach((item, idx) => {
            const div = document.createElement('div'); div.className = 'review-item';
            const opts = item.quiz || item.options || [];
            let optHtml = opts.map((o, i) => `<div class="review-opt-line">${i+1}. ${o}</div>`).join('');
            
            const cleanQ = String(item.question).replace(/^\d+\.\s*/, '');
            let imgHtml = item.image ? `<div class="text-center my-2"><img src="${item.image}" class="q-img"></div>` : '';
            
            div.innerHTML = `
                <div class="review-q-text"><b>${idx+1}.</b> ${processContent(cleanQ, item)}</div>
                ${imgHtml}
                <div class="review-opts" style="margin-left:20px">${optHtml}</div>
                <div class="review-ans">正確答案：${item.answer}</div>
                <div class="review-exp-box"><b>解析：</b><br>${processContent(item.explanation || '暫無解析。', item)}</div>
            `;
            area.appendChild(div);
        });
        const originalTitle = document.title; document.title = "{{DISPLAY_TITLE}}"; window.print(); document.title = originalTitle;
    }

    function renderQuestion(index) {
        window.scrollTo(0, 0);
        currentIndex = index; const item = quizData[index];
        const container = document.getElementById('question-container');
        const opts = item.quiz || item.options || [];
        
        // UI 按鈕顯示邏輯
        const pBtn = document.getElementById('side-btn-prev');
        if (pBtn) pBtn.style.display = (index === 0) ? 'none' : 'flex';

        // Determine Type Label
        let typeLabel = "單選";
        if (opts.some(o => String(o).includes('|'))) typeLabel = "題組";
        else if (item.type === 'multiple') typeLabel = "複選";
        
        container.innerHTML = `
            <div class="card question-card">
                <div class="question-header">
                    <div>
                        <span class="badge bg-primary me-2">題目 ${index + 1} / ${quizData.length}</span>
                        <span class="badge bg-info type-badge">${typeLabel}</span>
                    </div>
                    <div class="category-tag">${item.category || '一般'}</div>
                </div>
                <div class="question-body">
                    <div class="mb-3">${processContent(item.question, item)}</div>
                    ${item.image ? `<img src="${item.image}" class="q-img">` : ''}
                    <div class="options-area mt-3"></div>
                    <div class="text-center mt-4 pt-3 border-top"><button class="btn btn-outline-primary px-4" id="toggle-exp-btn" onclick="toggleExplanation()">👁️ 顯示答案 / 解析</button></div>
                    <div class="answer-section" id="ans-section">
                        <h6 class="fw-bold mb-3">正確答案: <span class="text-blue">${item.answer}</span></h6>
                        <div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div>
                    </div>
                </div>
            </div>
        `;
        const optionsArea = container.querySelector('.options-area');
        opts.forEach((opt, oIdx) => {
            if (String(opt).includes('|')) {
                let sHtml = `<div class="mb-3"><div class="fw-bold mb-1 small">題目 ${oIdx+1}</div><div class="d-flex flex-wrap gap-2">`;
                opt.split('|').forEach((s, subIdx) => {
                    sHtml += `<div class="sub-opt-container p-2 border rounded bg-light" onclick="checkSubAnswer(this, ${index}, ${oIdx}, ${subIdx}, event)" style="cursor:pointer; font-size:0.9rem"><input class="form-check-input" type="radio" name="q${index}_opt${oIdx}" id="o${oIdx}_s${subIdx}"> ${s}</div>`;
                });
                optionsArea.innerHTML += sHtml + '</div></div>';
            } else {
                optionsArea.innerHTML += `<div class="option-item" onclick="checkAnswer(this, ${index}, ${oIdx}, event)"><input class="form-check-input" type="${item.type==='multiple'?'checkbox':'radio'}" name="q${index}" id="o${oIdx}"> ${oIdx+1}. ${opt}</div>`;
            }
        });
        const saved = userAnswers[index], completed = correctSet.has(index) || incorrectSet.has(index) || correctedSet.has(index);
        let answers = item.answer; if (!Array.isArray(answers)) answers = [answers];
        let cIdxs = answers.map(a => parseInt(a) - 1);

        // --- 題組 (multioption) 顯示邏輯強化 ---
        if (opts.some(o => String(o).includes('|'))) {
            opts.forEach((opt, r) => {
                const correctSubIdx = parseInt(answers[r]) - 1;
                const savedSubIdx = (saved && typeof saved === 'object') ? saved[r] : undefined;
                
                opt.split('|').forEach((_, subIdx) => {
                    const inp = document.getElementById(`o${r}_s${subIdx}`);
                    if (!inp) return;
                    const container = inp.parentElement;
                    
                    // 1. 恢復曾經填寫的答案
                    if (savedSubIdx !== undefined && parseInt(savedSubIdx) === subIdx) {
                        inp.checked = true;
                        container.classList.add('selected');
                    }
                    
                    // 2. 如果已完成，顯示正確(綠)/錯誤(紅)顏色
                    if (completed) {
                        if (subIdx === correctSubIdx) {
                            container.classList.add('correct');
                        } else if (savedSubIdx !== undefined && parseInt(savedSubIdx) === subIdx) {
                            container.classList.add('incorrect');
                        }
                    }
                });
            });
        } 
        // --- 單選/複選 顯示邏輯 ---
        else if (saved !== undefined) {
            if (Array.isArray(saved)) {
                saved.forEach(idx => { const inp = document.getElementById(`o${idx}`); if (inp) { inp.checked = true; if(completed) inp.closest('.option-item').classList.add(cIdxs.includes(idx) ? 'correct' : 'incorrect'); } });
                if(completed) cIdxs.forEach(ci => { const inp = document.getElementById(`o${ci}`); if (inp) { inp.closest('.option-item').classList.add('correct'); } });
            } else {
                const inp = document.getElementById(`o${saved}`); if (inp) { inp.checked = true; if(completed) inp.closest('.option-item').classList.add(cIdxs.includes(saved) ? 'correct' : 'incorrect'); }
                if(completed && !cIdxs.includes(saved)) { const ci = document.getElementById(`o${cIdxs[0]}`); if(ci) ci.closest('.option-item').classList.add('correct'); }
            }
        }
        
        if (completed) { toggleExplanation(true); document.querySelectorAll(`input[name^="q${index}"]`).forEach(i => i.disabled = true); }
        updateUI(); Prism.highlightAll(); saveState();
    }
    function updateUI() {
        const stats = document.getElementById('progress-stats'); if (stats) stats.innerHTML = `✅${correctSet.size} ❌${incorrectSet.size} 🟠${correctedSet.size} <span class="ms-1 small" style="opacity:0.7">/ ${quizData.length}</span>`;
        const grid = document.getElementById('progress-grid'); grid.innerHTML = '';
        quizData.forEach((_, i) => {
            const n = document.createElement('div'); n.className = 'q-node'; if (i === currentIndex) n.classList.add('active');
            if (incorrectSet.has(i)) n.classList.add('incorrect'); else if (correctedSet.has(i)) n.classList.add('corrected'); else if (correctSet.has(i)) n.classList.add('correct');
            n.innerText = i + 1; n.onclick = () => jumpTo(i); grid.appendChild(n);
        });
    }
    loadState(); renderQuestion(currentIndex);
</script>
</body>
</html>"""

    for subject_dir in subject_dirs:
        dir_path = os.path.join('www', subject_dir)
        json_files = glob.glob(os.path.join(dir_path, 'questions_*.json'))
        if not json_files: continue
        with open(json_files[0], 'r', encoding='utf-8') as f: quiz_data = json.load(f)
        display_title = title_map.get(subject_dir, subject_dir.replace('_', ' '))
        res = html_template.replace('{{DISPLAY_TITLE}}', display_title).replace('{{QUIZ_DATA}}', json.dumps(quiz_data, ensure_ascii=False)).replace('{{CORR_KEY}}', f"{subject_dir.lower()}_correct_v1").replace('{{INCORR_KEY}}', f"{subject_dir.lower()}_incorrect_v1").replace('{{CORR_EDIT_KEY}}', f"{subject_dir.lower()}_corrected_v1").replace('{{INDEX_KEY}}', f"{subject_dir.lower()}_index_v1").replace('{{ANSWERS_KEY}}', f"{subject_dir.lower()}_answers_v1").replace('{{TOTAL}}', str(len(quiz_data))).replace('{{PDF_FILENAME}}', display_title)
        with open(os.path.join(dir_path, subject_dir + ".html"), 'w', encoding='utf-8') as f: f.write(res)
        alt_name = os.path.basename(json_files[0]).replace('questions_', '').replace('.json', '.html')
        if alt_name != subject_dir + ".html":
            with open(os.path.join(dir_path, alt_name), 'w', encoding='utf-8') as f: f.write(res)
        print(f"Refreshed: {display_title}")

if __name__ == "__main__":
    clean_repair_all()
