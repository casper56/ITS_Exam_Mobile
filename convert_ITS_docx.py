import docx
import json
import re
import sys
import io
import html

# Ensure stdout handles utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_docx(file_path):
    doc = docx.Document(file_path)
    questions = []
    current_q = None
    state = None
    
    re_q_id = re.compile(r'^第\s*(\d+)\s*題')
    re_q_header = re.compile(r'^題目[：:]')
    re_opt_header = re.compile(r'^選項[：:]')
    re_ans_header = re.compile(r'^(解答|答案|建議答案|正確答案)[：:]')
    re_exp_header = re.compile(r'^(解析|解答說明|說明|閫|憿閫)[：:]') 
    
    def parse_options_line(line_text):
        pattern = r'(?:^|\s+)([A-Da-d1-4])[\.、\)]\s*'
        matches = list(re.finditer(pattern, line_text))
        
        if matches:
            for i in range(len(matches)):
                start = matches[i].end()
                end = matches[i+1].start() if i+1 < len(matches) else len(line_text)
                content = line_text[start:end].strip()
                current_q['options'].append(content)
        else:
            if current_q['options']:
                current_q['options'][-1] += ' ' + line_text

    def format_question(text):
        lines = text.strip().split('\n')
        formatted_lines = []
        in_code = False
        code_block = []
        
        code_keywords = {'int', 'string', 'bool', 'if', 'else', 'for', 'while', 'public', 'private', 'var', 'void', 'delegate'}
        
        for line in lines:
            stripped = line.strip()
            is_code_line = (
                stripped.endswith(';') or 
                stripped.endswith('{') or 
                stripped.endswith('}') or 
                any(stripped.startswith(k + ' ') for k in code_keywords) or
                (stripped.startswith('if') and '(' in stripped) or
                stripped.startswith('//')
            )
            
            if is_code_line:
                in_code = True
                code_block.append(line)
            else:
                if in_code:
                    code_html = html.escape('\n'.join(code_block))
                    formatted_lines.append(f'<pre><code class="language-csharp">{code_html}</code></pre>')
                    code_block = []
                    in_code = False
                if stripped:
                    formatted_lines.append(html.escape(stripped))
        
        if in_code:
            code_html = html.escape('\n'.join(code_block))
            formatted_lines.append(f'<pre><code class="language-csharp">{code_html}</code></pre>')
            
        return '<br/>'.join(formatted_lines)

    def save_current():
        if current_q:
            raw_ans = current_q.get('raw_answer', '').strip()
            clean_ans_str = re.sub(r'[^\w\s]', ' ', raw_ans)
            tokens = clean_ans_str.split()
            valid_tokens = []
            mode = None
            for t in tokens:
                t = t.strip()
                if not t: continue
                is_letter = re.match(r'^[A-Da-d]$', t)
                is_number = re.match(r'^[1-4]$', t)
                if mode is None:
                    if is_letter: mode = 'LETTER'; valid_tokens.append(t)
                    elif is_number: mode = 'NUMBER'; valid_tokens.append(t)
                    else: break
                else:
                    if (mode == 'LETTER' and is_letter) or (mode == 'NUMBER' and is_number): valid_tokens.append(t)
                    else: break
            
            ans_indices = []
            for m in valid_tokens:
                idx = int(m) - 1 if m.isdigit() else ord(m.upper()) - ord('A')
                if 0 <= idx < 4 and idx not in ans_indices: ans_indices.append(idx)
            
            current_q['answer'] = sorted(ans_indices)
            current_q['type'] = 'multiple' if len(ans_indices) > 1 else 'single'
            
            current_q['question'] = format_question(current_q['question'])
            current_q['explanation'] = current_q['explanation'].replace('\n', '<br/>').strip()
            
            if 'raw_answer' in current_q: del current_q['raw_answer']
            current_q['options'] = [o.strip() for o in current_q['options']]
            
            questions.append(current_q)

    lines = [p.text for p in doc.paragraphs]
    for line in lines:
        line = re.sub(r'//.*', '', line).strip()
        if not line: continue
            
        match_id = re_q_id.match(line)
        if match_id:
            save_current()
            current_q = {'id': int(match_id.group(1)), 'question': '', 'options': [], 'answer': [], 'explanation': '', 'weight': 1, 'image': None, 'raw_answer': ''}
            state = 'QUESTION_ID_FOUND'
            continue
            
        if current_q is None: continue
            
        if re_q_header.match(line):
            state = 'QUESTION'
            content = re_q_header.sub('', line).strip()
            if content: current_q['question'] += content + '\n'
            continue
            
        if re_opt_header.match(line):
            state = 'OPTIONS'
            content = re_opt_header.sub('', line).strip()
            if content: parse_options_line(content)
            continue 
            
        if re_ans_header.match(line):
            state = 'ANSWER'
            content = re_ans_header.sub('', line).strip()
            current_q['raw_answer'] += content
            continue
            
        if re_exp_header.match(line):
            state = 'EXPLANATION'
            content = re_exp_header.sub('', line).strip()
            current_q['explanation'] += content + '\n'
            continue
            
        if state == 'QUESTION' or state == 'QUESTION_ID_FOUND':
            current_q['question'] += line + '\n'
        elif state == 'OPTIONS':
            parse_options_line(line)
        elif state == 'ANSWER':
            current_q['raw_answer'] += line + ' '
        elif state == 'EXPLANATION':
            current_q['explanation'] += line + '\n'

    save_current()
    return questions

questions = parse_docx('www/ITS_Csharp/ITS_軟體開發-解答說明0827.docx')
with open('www/ITS_Csharp/questions_ITS_csharp.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=4, ensure_ascii=False)

print(f"Successfully processed {len(questions)} questions.")