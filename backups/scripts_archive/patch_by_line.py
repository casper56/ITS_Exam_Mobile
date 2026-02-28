import os

path = 'final_clean_repair.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
found = False
for line in lines:
    if "item.explanation || '暫無解析。'" in line and "renderMatchingQuestion" in "".join(lines[max(0, lines.index(line)-50):lines.index(line)]):
        # 找到配對題的解析顯示行
        indent = line[:line.find("html")]
        new_lines.append(f"{indent}else {{
")
        new_lines.append(f"{indent}    const ansText = item.answer.join(', ');
")
        new_lines.append(f"{indent}    html += `<div class="answer-section" style="display:block;">
")
        new_lines.append(f"{indent}                <div class="fw-bold mb-2 ${{isCorrected?'text-warning':'text-success'}}">${{isCorrected?'🟠 已更正成功！':'✅ 答對了！'}}</div>
")
        new_lines.append(f"{indent}                <div class="review-ans" style="margin: 10px 0;">正確答案：${{ansText}}</div>
")
        new_lines.append(f"{indent}                <div class="explanation">${{processContent(item.explanation || '暫無解析。', item)}}</div>
")
        new_lines.append(f"{indent}             </div>`;
")
        new_lines.append(f"{indent}}}
")
        found = True
    else:
        new_lines.append(line)

if found:
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("SUCCESS: Line replaced via searching logic.")
else:
    print("ERROR: Could not locate target line.")
