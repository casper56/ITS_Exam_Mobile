const fs = require('fs');
const path = 'final_clean_repair.py';
let content = fs.readFileSync(path, 'utf-8');

const oldBlock = "else html += `<div class="answer-section" style="display:block;"><div class="fw-bold mb-2 ${isCorrected?'text-warning':'text-success'}">${isCorrected?'🟠 已更正成功！':'✅ 答對了！'}</div><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div>`;";

const newBlock = "else { const ansText = item.answer.join(', '); html += `<div class="answer-section" style="display:block;"><div class="fw-bold mb-2 ${isCorrected?'text-warning':'text-success'}">${isCorrected?'🟠 已更正成功！':'✅ 答對了！'}</div><div class="review-ans" style="margin: 10px 0;">正確答案：${ansText}</div><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div>`; }";

if (content.includes(oldBlock)) {
    content = content.replace(oldBlock, newBlock);
    fs.writeFileSync(path, content, 'utf-8');
    console.log('SUCCESS: Template updated with answer list.');
} else {
    console.log('ERROR: Marker not found.');
}
