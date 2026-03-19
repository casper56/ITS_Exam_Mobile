import re

with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
    content = f.read()

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

old_str3 = """<div class="review-ans">正確答案：${ansText}</div>"""
new_str3 = """<div class="review-ans">正確答案：${ansText} &nbsp;&nbsp;|&nbsp;&nbsp; 您的回答：${userAnsText}</div>"""

if old_str2 in content:
    content = content.replace(old_str2, new_str2)
    print("Replaced logic block")

if old_str3 in content:
    content = content.replace(old_str3, new_str3)
    print("Replaced HTML block")

with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
    f.write(content)
