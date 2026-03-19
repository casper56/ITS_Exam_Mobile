import os
import re

mock_files = [
    'www/AI900/mock_v34.html',
    'www/AZ900/mock_v34.html',
    'www/Generative_AI/mock_v34.html',
    'www/ITS_AI/mock_v34.html',
    'www/ITS_Database/mock_v34.html',
    'www/ITS_softdevelop/mock_v34.html',
    'www/ITS_Python/mock_v34.html',
    'www/ITS_JAVA/mock_v34.html'
]

def generate_clean_init(cutoff_val):
    return f"""    function initExam() {{
        if (typeof allQuestions === 'undefined' || allQuestions.length === 0) {{
            console.error("題庫資料載入失敗！"); return;
        }}
        const CUTOFF = {cutoff_val};
        const EXAM_LIMIT = 60;
        const TARGET_OFF_COUNT = 59; 
        const TARGET_SUPP_COUNT = 1;
        
        let historySet = new Set();
        try {{
            const savedHistory = localStorage.getItem(HISTORY_KEY);
            if (savedHistory) historySet = new Set(JSON.parse(savedHistory));
        }} catch(e) {{}}

        // 1. 池子拆分
        const offPool = allQuestions.filter(q => q.id <= CUTOFF).sort(() => 0.5 - Math.random());
        const suppPool = allQuestions.filter(q => q.id > CUTOFF).sort(() => 0.5 - Math.random());

        const offUnseen = offPool.filter(q => !historySet.has(q.id));
        const offSeen = offPool.filter(q => historySet.has(q.id));
        const finalOffOrder = [...offUnseen, ...offSeen];

        const suppUnseen = suppPool.filter(q => !historySet.has(q.id));
        const suppSeen = suppPool.filter(q => historySet.has(q.id));
        const finalSuppOrder = [...suppUnseen, ...suppSeen];

        // 2. 59 題官方 + 1 題補充
        let selected = finalOffOrder.slice(0, TARGET_OFF_COUNT);
        const suppSelected = finalSuppOrder.slice(0, TARGET_SUPP_COUNT);
        selected = [...selected, ...suppSelected];

        // 3. 兜底 (若總數不足 60)
        if (selected.length < EXAM_LIMIT) {{
            const usedIds = new Set(selected.map(q => q.id));
            const remainingPool = allQuestions.filter(q => !usedIds.has(q.id)).sort(() => 0.5 - Math.random());
            while (selected.length < EXAM_LIMIT && remainingPool.length > 0) {{
                selected.push(remainingPool.shift());
            }}
        }}

        // 4. 更新歷史
        selected.forEach(q => historySet.add(q.id));
        if (historySet.size > (allQuestions.length * 0.9)) historySet.clear();
        localStorage.setItem(HISTORY_KEY, JSON.stringify([...historySet]));

        // 5. 隨機打散並截取 60 題
        examQuestions = selected.sort(() => 0.5 - Math.random()).slice(0, EXAM_LIMIT);"""

for file_path in mock_files:
    if not os.path.exists(file_path): continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine Cutoff
    m = re.search(r'const CUTOFF = (\d+);', content)
    cutoff_val = m.group(1) if m else "98"
    if "ITS_softdevelop" in file_path: cutoff_val = "101"

    # 暴力替換：將 function initExam() { ... 到 ... examQuestions = ...; } 的所有可能重複區塊全部取代
    # 我們使用非貪婪匹配，並循環替換直到沒得換為止，以防檔案中有重複的定義
    new_init_body = generate_clean_init(cutoff_val)
    
    # 匹配模式：從 function initExam() { 到最近的 examQuestions = ...;
    pattern = r'function initExam\(\) \{[\s\S]*?examQuestions = selected\.sort\(\(\) => 0\.5 - Math\.random\(\)\)(?:\.slice\(0, EXAM_LIMIT\))?;'
    
    # 進行循環替換以清除所有潛在的舊定義
    while re.search(pattern, content):
        content = re.sub(pattern, new_init_body, content)

    # 同步更新結果畫面的判定邏輯
    content = re.sub(r'obj\.id > \d+ \? `\(\$\{obj\.id\}\)` : obj\.id', f'obj.id > {cutoff_val} ? `(${{obj.id}})` : obj.id', content)
    content = re.sub(r'代表 1-\d+ 題以外的補充題', f'代表 1-{cutoff_val} 題以外的補充題', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Brute-force updated {file_path} to 59+1 (CUTOFF={cutoff_val})")

print("Cleanup and reconstruction completed.")
