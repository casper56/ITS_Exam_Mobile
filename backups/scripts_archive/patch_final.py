import os

path = 'final_clean_repair.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 尋找關鍵渲染區塊
target = "else html += `<div class="answer-section" style="display:block;"><div class="fw-bold mb-2 ${isCorrected?'text-warning':'text-success'}">${isCorrected?'🟠 已更正成功！':'✅ 答對了！'}</div><div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div></div>`;"

replacement = """else {
            const ansText = item.answer.join(', ');
            html += `<div class="answer-section" style="display:block;">
                        <div class="fw-bold mb-2 ${isCorrected?'text-warning':'text-success'}">${isCorrected?'🟠 已更正成功！':'✅ 答對了！'}</div>
                        <div class="review-ans" style="margin: 10px 0;">正確答案：${ansText}</div>
                        <div class="explanation">${processContent(item.explanation || '暫無解析。', item)}</div>
                     </div>`;
        }"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Template updated via simple replace.")
else:
    print("ERROR: Target string not found.")
