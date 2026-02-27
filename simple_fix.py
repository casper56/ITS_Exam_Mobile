import os

with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修正判定 logic: 改為檢查 document.title
new_init_exam = """    function initExam() {
        if (typeof allQuestions === 'undefined' || allQuestions.length === 0) return;
        const CUTOFF = REPLACE_CUTOFF;
        // 修正判定：直接檢查網頁標題是否含有 Python
        const isPython = document.title.includes("Python");
        
        let historySet = new Set();
        try {
            const savedHistory = localStorage.getItem(HISTORY_KEY);
            if (savedHistory) historySet = new Set(JSON.parse(savedHistory));
        } catch(e) {}

        let selected = [], usedIds = new Set();

        // --- 鐵腕 D0 鎖定：針對 Python，我們先手動抽 2 題 D0 ---
        if (isPython) {
            const d0Pool = allQuestions.filter(q => q.category && q.category.includes("D0")).sort(() => 0.5 - Math.random());
            const d0ToDraw = Math.min(2, d0Pool.length);
            for (let i = 0; i < d0ToDraw; i++) {
                selected.push(d0Pool[i]); usedIds.add(d0Pool[i].id);
            }
        }

        // --- 剩餘題目抽樣 (排除已選的 D0，且如果已經是 Python 也不准再抽 D0) ---
        const remainingPool = allQuestions.filter(q => !usedIds.has(q.id) && !(isPython && q.category && q.category.includes("D0")));
        const offPool = remainingPool.filter(q => q.id <= CUTOFF).sort(() => 0.5 - Math.random());
        const suppPool = remainingPool.filter(q => q.id > CUTOFF).sort(() => 0.5 - Math.random());

        // 抽官方題直到 57 題 (包含之前的 D0)
        for (let q of offPool) {
            if (selected.filter(s => s.id <= CUTOFF).length >= 57) break;
            selected.push(q); usedIds.add(q.id);
        }
        // 抽補充題直到 60 題
        for (let q of suppPool) {
            if (selected.length >= 60) break;
            selected.push(q); usedIds.add(q.id);
        }
        // 萬一不夠 (兜底，且依然排除 D0)
        const finalPool = allQuestions.filter(q => !usedIds.has(q.id) && !(isPython && q.category && q.category.includes("D0"))).sort(() => 0.5 - Math.random());
        while (selected.length < 60 && finalPool.length > 0) {
            const q = finalPool.shift(); selected.push(q); usedIds.add(q.id);
        }

        selected.forEach(q => historySet.add(q.id));
        if (historySet.size > (allQuestions.length * 0.9)) historySet.clear();
        localStorage.setItem(HISTORY_KEY, JSON.stringify([...historySet]));

        examQuestions = selected.sort(() => 0.5 - Math.random());
        renderQuestion(0); startTimer();
    }
"""

start_marker = "    function initExam() {"
end_marker = "    function renderQuestion(index, scrollTop = true) {"

s_idx = content.find(start_marker)
e_idx = content.find(end_marker)

if s_idx != -1 and e_idx != -1:
    new_content = content[:s_idx] + new_init_exam + "\n" + content[e_idx:]
    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: initExam fixed to use document.title and hard-locked D0 limit.")
else:
    print("ERROR: Could not find markers.")
