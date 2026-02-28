const fs = require('fs');
const path = 'final_clean_repair.py';
let content = fs.readFileSync(path, 'utf-8');

const marker = "else html += `<div class="answer-section" style="display:block;"><div class="fw-bold mb-2 ${isCorrected?'text-warning':'text-success'}">${isCorrected?'";
// 使用 IndexOf 找穩定標記
const idx = content.indexOf(marker);

if (idx !== -1) {
    // 找到這一整行
    const lineStart = content.lastIndexOf('
', idx) + 1;
    const lineEnd = content.indexOf('
', idx);
    
    const newBlock = `        else {
            const ansText = item.answer.join(', ');
            html += `<div class="answer-section" style="display:block;">
                        <div class="fw-bold mb-2 \${isCorrected?'text-warning':'text-success'}">\${isCorrected?'🟠 已更正成功！':'✅ 答對了！'}</div>
                        <div class="review-ans" style="margin: 10px 0;">正確答案：\${ansText}</div>
                        <div class="explanation">\${processContent(item.explanation || '暫無解析。', item)}</div>
                     </div>`;
        }`;
    
    const newContent = content.substring(0, lineStart) + newBlock + content.substring(lineEnd);
    fs.writeFileSync(path, newContent, 'utf-8');
    console.log('SUCCESS: RESTORED VIA NODEJS BUFFER');
} else {
    console.log('NOT FOUND');
}
