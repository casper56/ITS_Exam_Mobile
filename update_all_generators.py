import os
import re

def update_json_to_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # CSS styles
    content = re.sub(r'min-height: \d+px;', 'min-height: 400px;', content)
    content = re.sub(r'\.question-body \{\{ padding: [^;]+; font-size: [^;]+; \}\}', 
                     '.question-body {{ padding: 15px 25px 10px 25px; font-size: 1rem; }}', content)
    
    content = re.sub(r'\.option-item \{\{\s*list-style: none; margin-bottom: \d+px; padding: [^;]+; border: 1px solid #e9ecef;',
                     '.option-item {{ list-style: none; margin-bottom: 5px; padding: 5px 12px; border: 1px solid #e9ecef;', content)
    content = re.sub(r'border-radius: \d+px;', 'border-radius: 6px;', content)
    
    # Tighten answer-section CSS
    content = re.sub(r'\.answer-section \{\{\s*display: none; margin-top: \d+px; padding: [^;]+; background-color: #f0f7ff;',
                     '.answer-section {{ display: none; margin-top: 12px; padding: 10px 15px 5px 15px; background-color: #f0f7ff;', content)
    
    # Tighten nav-btn-group
    content = re.sub(r'\.nav-btn-group \{\{ display: flex; gap: \d+px; margin-top: \d+px;',
                     '.nav-btn-group {{ display: flex; gap: 15px; margin-top: 15px;', content)

    # Explanation font size (Increase to 1rem)
    content = re.sub(r'\.explanation \{\{ font-size: [^;]+; margin: 0; \}\}',
                     '.explanation {{ font-size: 1rem; margin: 0; }}', content)

    # Dynamic HTML Spacing
    content = content.replace('let qText = (item.question || \'\').replace(/●/g, \'<br/>●\');',
                              'let qText = (item.question || \'\').replace(/●/g, \'<br/>●\').replace(/^<br\\/>/, \'\');')
    
    content = content.replace('<h6 class="mb-1 fw-bold">正確答案:</h6>', '<h6 class="mb-0 fw-bold">正確答案:</h6>')
    content = re.sub(r'<div class="alert alert-success fs-6 fw-bold mb-2 p-2">', 
                     '<div class="alert alert-success fs-6 fw-bold mb-1 p-1">', content)
    content = content.replace('<h6 class="mb-1 mt-2 fw-bold">解析:</h6>', '<h6 class="mb-0 mt-1 fw-bold">解析:</h6>')
    
    content = content.replace('<div class="explanation">${{(item.explanation || \'暫無解析。\').replace(/●/g, \'<br/>●\')}}</div>',
                              '<div class="explanation">${{(item.explanation || \'暫無解析。\').replace(/●/g, \'<br/>●\').replace(/^<br\\/>/, \'\')}}</div>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Find all files
for root, dirs, files in os.walk('www'):
    for file in files:
        file_path = os.path.join(root, file)
        if file == 'json_to_html.py':
            print(f"Updating {file_path}")
            update_json_to_html(file_path)

print("Batch update complete.")