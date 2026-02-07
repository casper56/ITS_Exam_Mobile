import os
import re

def update_json_to_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS styles
    content = re.sub(r'min-height: 500px;', 'min-height: 400px;', content)
    content = re.sub(r'\.question-body \{\{ padding: 40px; font-size: 1.1rem; \}\}', 
                     '.question-body {{ padding: 15px 25px; font-size: 1rem; }}', content)
    
    content = re.sub(r'\.option-item \{\{\s*list-style: none; margin-bottom: 12px; padding: 15px; border: 1px solid #e9ecef;',
                     '.option-item {{ list-style: none; margin-bottom: 5px; padding: 5px 12px; border: 1px solid #e9ecef;', content)
    content = re.sub(r'border-radius: 8px;', 'border-radius: 6px;', content)
    
    content = re.sub(r'\.sub-question-label \{\{ font-weight: bold; margin-top: 20px; margin-bottom: 10px;',
                     '.sub-question-label {{ font-weight: bold; margin-top: 15px; margin-bottom: 8px;', content)
    
    content = re.sub(r'\.answer-section \{\{\s*display: none; margin-top: 30px; padding: 25px;',
                     '.answer-section {{ display: none; margin-top: 20px; padding: 15px 20px;', content)
    
    content = re.sub(r'\.nav-btn-group \{\{ display: flex; gap: 15px; margin-top: 30px;',
                     '.nav-btn-group {{ display: flex; gap: 15px; margin-top: 20px;', content)

    if '.explanation {{ font-size: 1rem; }}' not in content:
        content = content.replace('code {{ font-family: Consolas, Monaco, monospace; color: #d63384; background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; }}',
                                  'code {{ font-family: Consolas, Monaco, monospace; color: #d63384; background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; }}\n        .explanation {{ font-size: 1rem; }}')

    # 2. Update renderQuestion dynamic HTML
    content = content.replace('body.innerHTML += `<div class="mb-4">${{qText}}</div>`;', 
                              'body.innerHTML += `<div class="mb-3">${{qText}}</div>`;')
    content = content.replace('body.innerHTML += `<div class="text-center mb-4"><img src="${{item.image}}" class="question-image" alt="Question Image"></div>`;',
                              'body.innerHTML += `<div class="text-center mb-3"><img src="${{item.image}}" class="question-image" alt="Question Image"></div>`;')
    content = content.replace('let optionsHtml = \'<div class="mt-4">\';', 
                              'let optionsHtml = \'<div class="mt-3">\';')
    content = content.replace('p-2 border rounded bg-light sub-opt-container', 
                              'p-1 border rounded bg-light sub-opt-container')
    content = content.replace('style="transform: scale(1.2); margin-top: 0.3rem;"', 
                              'style="transform: scale(1.1); margin-top: 0.2rem;"')
    content = content.replace('footer.className = \'mt-5 pt-4 border-top text-center\';', 
                              'footer.className = \'mt-4 pt-3 border-top text-center\';')
    
    content = content.replace('<h5 class="mb-3">正確答案:</h5>', '<h6 class="mb-1 fw-bold">正確答案:</h6>')
    content = content.replace('<div class="alert alert-success fs-5 fw-bold">${{ansDisplay}}</div>', 
                              '<div class="alert alert-success fs-6 fw-bold mb-2 p-2">${{ansDisplay}}</div>')
    content = content.replace('<h5 class="mb-3 mt-4">解析:</h5>', '<h6 class="mb-1 mt-2 fw-bold">解析:</h6>')
    content = content.replace('<div class="explanation">${{(item.explanation || \'暫無解析。\').replace(/●/g, \'<br/>●\')}}</div>',
                              '<div class="explanation">${{(item.explanation || \'暫無解析。\').replace(/●/g, \'<br/>●\')}}</div>')
    content = content.replace('<div class="explanation small">', '<div class="explanation">')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_json_to_pdf(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r"name='Question', parent=styles\['Heading2'\], fontName=font_name, fontSize=11, spaceAfter=10, leading=16",
                     "name='Question', parent=styles['Heading2'], fontName=font_name, fontSize=11, spaceAfter=6, leading=14", content)
    content = re.sub(r"name='Option', parent=styles\['Normal'\], fontName=font_name, fontSize=10, leftIndent=20, spaceAfter=2, leading=14",
                     "name='Option', parent=styles['Normal'], fontName=font_name, fontSize=10, leftIndent=20, spaceAfter=1, leading=12", content)
    content = re.sub(r"name='Answer', parent=styles\['Normal'\], fontName=font_name, fontSize=10, textColor=colors.blue, spaceBefore=5, spaceAfter=5",
                     "name='Answer', parent=styles['Normal'], fontName=font_name, fontSize=10, textColor=colors.blue, spaceBefore=3, spaceAfter=3", content)
    content = re.sub(r"name='Explanation', parent=styles\['Normal'\], fontName=font_name, fontSize=10, textColor=colors.darkgreen\)\)",
                     "name='Explanation', parent=styles['Normal'], fontName=font_name, fontSize=10, textColor=colors.darkgreen, spaceAfter=2))", content)

    content = content.replace('story.append(img)\n                    story.append(Spacer(1, 10))',
                              'story.append(img)\n                    story.append(Spacer(1, 5))')
    content = content.replace('story.append(Spacer(1, 15))\n        story.append(Paragraph("<hr color=\'silver\' width=\'100%\'/>", styles[\'Normal\']))\n        story.append(Spacer(1, 15))',
                              'story.append(Spacer(1, 10))\n        story.append(Paragraph("<hr color=\'silver\' width=\'100%\'/>", styles[\'Normal\']))\n        story.append(Spacer(1, 10))')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('www'):
    for file in files:
        file_path = os.path.join(root, file)
        if file == 'json_to_html.py':
            print(f"Updating {file_path}")
            update_json_to_html(file_path)
        elif file == 'json_to_pdf.py':
            print(f"Updating {file_path}")
            update_json_to_pdf(file_path)

print("Batch update complete.")