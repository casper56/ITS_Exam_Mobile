import os
import glob
import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Repl 1: newline in array
    old_str1 = "let processedRow = Array.isArray(o) ? o.join('\\n') : String(o);"
    new_str1 = "let processedRow = Array.isArray(o) ? o.join('<br>') : String(o);"
    if old_str1 in content:
        content = content.replace(old_str1, new_str1)
    
    # Repl 2: userAnsText logic
    old_str2 = """            let ansText = answers.map(a => {
                if (String(a).toUpperCase() === 'Y' || String(a).toUpperCase() === 'N') return a;
                const idx = parseAnswerToIndex(a);
                if (idx < 0) return a;
                return isNum ? (idx + 1) : String.fromCharCode(65 + idx);
            }).join(', ');

            if (isCorrect) { correctCount++; stats[cat].correct++; }"""
    
    new_str2 = """            let ansText = answers.map(a => {
                if (String(a).toUpperCase() === 'Y' || String(a).toUpperCase() === 'N') return a;
                const idx = parseAnswerToIndex(a);
                if (idx < 0) return a;
                return isNum ? (idx + 1) : String.fromCharCode(65 + idx);
            }).join(', ');

            let userAnsText = '未作答';
            if (userAns !== undefined && userAns !== null) {
                let parseU = (u) => {
                    if (u === null || u === undefined || u === -1) return '未作答';
                    return isNum ? (u + 1) : String.fromCharCode(65 + u);
                };
                if (Array.isArray(userAns)) {
                    userAnsText = userAns.map(parseU).join(', ');
                } else if (typeof userAns === 'object') {
                    let uArr = [];
                    for(let i=0; i<answers.length; i++) {
                        uArr.push(parseU(userAns[i]));
                    }
                    userAnsText = uArr.join(', ');
                } else {
                    userAnsText = parseU(userAns);
                }
            }

            if (isCorrect) { correctCount++; stats[cat].correct++; }"""
            
    if old_str2 in content:
        content = content.replace(old_str2, new_str2)
    else:
        # Fallback regex in case of slight indentation differences
        pattern2 = re.compile(r"(let ansText = answers\.map\(a => \{.*?\}\)\.join\(', '\);\s*)(if \(isCorrect\) \{ correctCount\+\+; stats\[cat\]\.correct\+\+; \})", re.DOTALL)
        content = pattern2.sub(r"\1" + """
            let userAnsText = '未作答';
            if (userAns !== undefined && userAns !== null) {
                let parseU = (u) => {
                    if (u === null || u === undefined || u === -1) return '未作答';
                    return isNum ? (u + 1) : String.fromCharCode(65 + u);
                };
                if (Array.isArray(userAns)) {
                    userAnsText = userAns.map(parseU).join(', ');
                } else if (typeof userAns === 'object') {
                    let uArr = [];
                    for(let i=0; i<answers.length; i++) {
                        uArr.push(parseU(userAns[i]));
                    }
                    userAnsText = uArr.join(', ');
                } else {
                    userAnsText = parseU(userAns);
                }
            }

            \2""", content)

    # Repl 3: Render userAnsText in HTML
    old_str3 = """<div class="review-ans">正確答案：${ansText}</div>"""
    new_str3 = """<div class="review-ans">正確答案：${ansText} &nbsp;&nbsp;|&nbsp;&nbsp; 您的回答：${userAnsText}</div>"""
    if old_str3 in content:
        content = content.replace(old_str3, new_str3)
    else:
        # Fallback for exact match
        pattern3 = re.compile(r'<div class="review-ans">正確答案：\$\{ansText\}</div>')
        content = pattern3.sub(r'<div class="review-ans">正確答案：${ansText} &nbsp;&nbsp;|&nbsp;&nbsp; 您的回答：${userAnsText}</div>', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched: {filepath}")

for f in glob.glob('www/**/*mock_v34.html', recursive=True):
    patch_file(f)
