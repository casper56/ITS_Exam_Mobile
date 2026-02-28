const fs = require('fs');
const path = 'final_clean_repair.py';
let content = fs.readFileSync(path, 'utf-8');

const goldenUI = `    function updateUI() {
        const stats = document.getElementById('progress-stats'); if (stats) stats.innerHTML = '✅' + correctSet.size + ' ❌' + incorrectSet.size + ' 🟠' + correctedSet.size + ' / ' + quizData.length;
        const grid = document.getElementById('progress-grid'); if(!grid) return;
        grid.innerHTML = '';
        quizData.forEach((_, i) => {
            const n = document.createElement('div'); n.className = 'q-node';
            if(i === currentIndex) n.classList.add('active');
            if(correctSet.has(i)) n.classList.add('correct');
            else if(correctedSet.has(i)) n.classList.add('corrected');
            else if(incorrectSet.has(i)) n.classList.add('incorrect');
            n.innerText = i + 1; n.onclick = () => jumpTo(i);
            grid.appendChild(n);
        });
    }`;

// 尋找舊的、簡化版的 updateUI 並替換
content = content.replace(/function updateUI\(\) \{[\s\S]*?\}/, goldenUI);

fs.writeFileSync(path, content, 'utf-8');
console.log('SUCCESS: Sidebar UI logic restored to original professional version.');
