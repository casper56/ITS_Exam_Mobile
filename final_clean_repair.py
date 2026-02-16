import json
import os
import re
import glob

def clean_repair_all():
    subject_dirs = [d for d in os.listdir('www') if os.path.isdir(os.path.join('www', d)) and d != 'assets']
    
    # V3.4 穩定升級版：支援字母答案與 parseAnswerToIndex
    logic_code = r"""
    function parseAnswerToIndex(val) {
        if (typeof val === 'number') return val - 1;
        if (typeof val === 'string') {
            const code = val.toUpperCase().charCodeAt(0);
            if (code >= 65 && code <= 90) return code - 65;
            return parseInt(val) - 1;
        }
        return -1;
    }

    function initExam() {
        if (!allQuestions || allQuestions.length === 0) { console.error("題庫資料載入失敗！"); return; }
        
        const isITS_AI = window.location.href.includes('ITS_AI');
        const is900Series = window.location.href.includes('AZ900') || window.location.href.includes('AI900');
        const isPython = window.location.href.includes('ITS_Python');
        
        const CUTOFF = isITS_AI ? 118 : (is900Series ? 100 : 69);
        const TARGET_OFF_COUNT = Math.floor(EXAM_LIMIT * 0.92); 
        const MIN_PER_CAT_PCT = 0.05; 
        const MAX_PER_CAT_PCT = 0.40; 
        
        const categories = {};
        const catNameMap = {}; 
        
        allQuestions.forEach(q => {
            let fullCat = q.category || '一般';
            let m = fullCat.match(/^(D\d+)/);
            let prefix = (m ? m[1] : fullCat);
            if (!catNameMap[prefix] || fullCat.length > catNameMap[prefix].length) catNameMap[prefix] = fullCat;
        });

        allQuestions.forEach(q => {
            let m = (q.category ? q.category.match(/^(D\d+)/) : null);
            let prefix = (m ? m[1] : q.category || '一般');
            let cat = catNameMap[prefix];
            if (!categories[cat]) categories[cat] = [];
            categories[cat].push(q);
        });

        let selected = [], usedIds = new Set();
        const catNames = Object.keys(categories).sort();
        const MIN_PER_CAT = Math.max(1, Math.floor(EXAM_LIMIT * MIN_PER_CAT_PCT));
        const MAX_PER_CAT = Math.floor(EXAM_LIMIT * MAX_PER_CAT_PCT);

        catNames.forEach(cat => {
            const catOff = categories[cat].filter(q => q.id <= CUTOFF).sort(() => 0.5 - Math.random());
            const catSupp = categories[cat].filter(q => q.id > CUTOFF).sort(() => 0.5 - Math.random());
            for (let i = 0; i < MIN_PER_CAT; i++) {
                if (catOff.length > 0) { const q = catOff.shift(); selected.push(q); usedIds.add(q.id); }
                else if (catSupp.length > 0) { const q = catSupp.shift(); selected.push(q); usedIds.add(q.id); }
            }
        });

        let offPool = allQuestions.filter(q => q.id <= CUTOFF && !usedIds.has(q.id)).sort(() => 0.5 - Math.random());
        for (let q of offPool) {
            if (selected.length >= TARGET_OFF_COUNT) break;
            let qCat = catNames.find(c => categories[c].some(cq => cq.id === q.id));
            let currentInCat = selected.filter(sq => categories[qCat].some(cq => cq.id === sq.id)).length;
            if (currentInCat < MAX_PER_CAT) { selected.push(q); usedIds.add(q.id); }
        }

        let finalPool = allQuestions.filter(q => !usedIds.has(q.id)).sort((a, b) => (b.id <= CUTOFF ? 1 : 0) - (a.id <= CUTOFF ? 1 : 0) || (0.5 - Math.random()));
        while (selected.length < EXAM_LIMIT && finalPool.length > 0) { const q = finalPool.shift(); selected.push(q); usedIds.add(q.id); }

        examQuestions = selected.sort(() => 0.5 - Math.random()).slice(0, EXAM_LIMIT);
        renderQuestion(0); startTimer();
    }"""

    for subject_dir in subject_dirs:
        dir_path = os.path.join('www', subject_dir)
        mock_path = os.path.join(dir_path, 'mock_exam.html')
        if not os.path.exists(mock_path): continue
        
        json_files = glob.glob(os.path.join(dir_path, 'questions_*.json'))
        if json_files:
            with open(json_files[0], 'r', encoding='utf-8') as f: quiz_data = json.load(f)
            json_str = json.dumps(quiz_data, ensure_ascii=False, indent=2)
            
            with open(mock_path, 'r', encoding='utf-8') as f: content = f.read()
            
            # 1. 替換 initExam 邏輯
            start_marker = 'function initExam() {'
            end_marker = '    function startTimer'
            if start_marker in content and end_marker in content:
                parts = content.split(start_marker)
                rest = parts[1].split(end_marker, 1)
                content = parts[0] + logic_code + "\n\n" + end_marker + rest[1]
            
            # 2. 同步 JSON 資料
            if 'const allQuestions =' in content:
                head = content.split('const allQuestions =')[0]
                rest = content.split('let examQuestions = [];')[1]
                content = head + 'const allQuestions = ' + json_str + ';\n    let examQuestions = [];' + rest
            
            # 3. 強化 submitExam 中的答案比對 (確保 parseAnswerToIndex 被使用)
            # 針對可能存在的舊版比對邏輯進行正則修正
            content = content.replace('(parseInt(a) - 1)', 'parseAnswerToIndex(a)')
            content = content.replace('(parseInt(item.answer) - 1)', 'parseAnswerToIndex(item.answer)')
            content = content.replace('item.answer.map(a => parseInt(a) - 1)', 'item.answer.map(a => parseAnswerToIndex(a))')

            with open(mock_path, 'w', encoding='utf-8') as f: f.write(content)
        print(f"V3.4 Refreshed (Letter Answer Support): {subject_dir}")

if __name__ == "__main__":
    clean_repair_all()
