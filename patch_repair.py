import os

path = 'final_clean_repair.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修正 prac_top_tmpl 中的 explanation 換行與列印佈局
old_prac_style = """        .question-body { padding: 20px; font-size: 1.0rem; word-wrap: break-word; word-break: normal; overflow-x: hidden; line-height: 1.8; }
        .answer-section { display: none; margin-top: 20px; padding: 20px; background: #fff; border: 2px solid #0d6efd; border-radius: 8px; }
        .q-img { max-width: 100%; height: auto; border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); margin: 5px auto; display: block; }"""

new_prac_style = """        .question-body { padding: 20px; font-size: 1.0rem; word-wrap: break-word; word-break: normal; overflow-x: hidden; line-height: 1.8; }
        .answer-section { display: none; margin-top: 20px; padding: 20px; background: #fff; border: 2px solid #0d6efd; border-radius: 8px; }
        .explanation, .explanation pre, .explanation code, .review-exp-box pre, .review-exp-box code, pre[class*="language-"], code[class*="language-"] { white-space: pre-wrap !important; word-wrap: break-word !important; word-break: break-all !important; overflow-wrap: anywhere !important; }
        .review-item { margin-bottom: 10px; padding: 0; border: none; background: white; page-break-inside: auto; border-bottom: 1px solid #eee; padding-bottom: 10px; }
        .review-q-text { display: flex; align-items: flex-start; font-size: 1.0rem; line-height: 1.8; margin-bottom: 5px; color: #333; }
        .review-q-text b { margin-right: 8px; white-space: nowrap; }
        .review-q-text .q-content { flex: 1; }
        .review-q-text .q-content pre, .review-q-text .q-content code { margin-top: 0 !important; padding-top: 0 !important; }
        .q-img { max-width: 100%; height: auto; border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); margin: 5px auto; display: block; }"""

# 2. 修正 prepareAndPrint 中的題號結構
old_prac_html = """div.innerHTML = `<div class="review-q-text"><b>${idx+1}.</b> ${processContent(cleanQ, item)}</div>${imgHtml}<div class="review-opts" style="margin-left:0">${optHtml}</div><div class="review-ans">正確答案：${ansText}</div><div class="review-exp">${processContent(item.explanation || '暫無解析。', item)}</div>`;"""
new_prac_html = """div.innerHTML = `<div class="review-q-text"><b>${idx+1}.</b> <div class="q-content">${processContent(cleanQ, item)}</div></div>${imgHtml}<div class="review-opts" style="margin-left:0">${optHtml}</div><div class="review-ans">正確答案：${ansText}</div><div class="review-exp">${processContent(item.explanation || '暫無解析。', item)}</div>`;"""

# 3. 修正 mock_top_tmpl 的列印樣式 (解決空行問題)
old_mock_print = """            #result-screen { display: block !important; padding: 0 !important; width: 100% !important; margin: 0 !important; }
            #review-area { display: block !important; border: none !important; width: 100% !important; padding: 0 !important; }"""

new_mock_print = """            #result-screen { display: block !important; padding: 0 !important; width: 100% !important; margin: 0 !important; }
            #result-screen h2.text-center { margin-top: 0 !important; padding-top: 0 !important; }
            #review-area { display: block !important; border: none !important; width: 100% !important; padding: 0 !important; margin: 0 !important; }
            .review-item { border: 1px solid #eee !important; width: 100% !important; page-break-inside: auto; margin-bottom: 5px !important; padding: 0 !important; }
            .review-id { margin: 0 !important; padding: 5px 10px !important; border-radius: 0 !important; }
            .review-q-text { display: flex !important; align-items: flex-start !important; padding: 10px 15px !important; font-size: 1.0rem !important; white-space: pre-wrap !important; word-break: break-all !important; width: calc(100% - 2px) !important; }
            .review-q-text b { margin-right: 8px !important; white-space: nowrap !important; }
            .review-q-text .q-content { flex: 1 !important; }
            .review-q-text .q-content pre, .review-q-text .q-content code { margin-top: 0 !important; padding-top: 0 !important; }"""

# 4. 修正 MOCK 題目回顧結構
old_mock_html = """incorrectHTML += `<div class="review-item"><div class="review-id">題目 ${idx + 1} (編號: ${item.id})</div><div class="mb-2">${processContent(item.question, item)}</div>${optionsHTML}<div class="review-ans">正確答案：${ansText}</div><div class="review-exp"><b>解析：</b><br/>${processContent(item.explanation || '暫無解析。', item)}</div></div>`;"""
new_mock_html = """incorrectHTML += `<div class="review-item"><div class="review-id">題目 ${idx + 1} (編號: ${item.id})</div><div class="review-q-text"><div class="q-content">${processContent(item.question, item)}</div></div>${optionsHTML}<div class="review-ans">正確答案：${ansText}</div><div class="review-exp"><b>解析：</b><br/>${processContent(item.explanation || '暫無解析。', item)}</div></div>`;"""

content = content.replace(old_prac_style, new_prac_style)
content = content.replace(old_prac_html, new_prac_html)
content = content.replace(old_mock_print, new_mock_print)
content = content.replace(old_mock_html, new_mock_html)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("final_clean_repair.py 修補完成，編碼已受保護。")
