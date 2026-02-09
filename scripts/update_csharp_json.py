import docx
import json
import re
import sys
import io
import html

# Ensure stdout handles utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_docx_updates(file_path):
    doc = docx.Document(file_path)
    updates = {}
    current_id = None
    current_data = {'explanation': '', 'raw_answer': '', 'question_lines': []}
    state = None
    
    re_q_id = re.compile(r'^第\s*(\d+)\s*題')
    re_q_header = re.compile(r'^題目[：:]')
    re_opt_header = re.compile(r'^選項[：:]')
    re_ans_header = re.compile(r'^(解答|答案|建議答案|正確答案)[：:]')
    re_exp_header = re.compile(r'^(解析|解答說明|說明|閫|憿閫|解釋)[：:]') 
    
    def finalize_current():
        if current_id is not None:
            raw_ans = current_data.get('raw_answer', '').strip()
            explanation = current_data['explanation'].strip()
            
            # Format question
            q_text = "\n".join(current_data['question_lines']).strip()
            # Wrap in code tag as requested. Adding <pre> for better block support.
            formatted_q = f'<pre><code class="language-csharp">{q_text}</code></pre>'

            # Try to extract explanation from raw_answer if explanation is empty
            if not explanation:
                split_patterns = [r'(解析|解答說明|說明|閫|憿閫|解釋)\s*[：:]*']
                for pat in split_patterns:
                    match = re.search(pat, raw_ans)
                    if match:
                        real_ans = raw_ans[:match.start()].strip()
                        extracted_exp = raw_ans[match.end():].strip()
                        if extracted_exp:
                            raw_ans = real_ans
                            explanation = extracted_exp
                            break

            # Parse answer
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
                idx = int(m) if m.isdigit() else ord(m.upper()) - ord('A') + 1
                if 1 <= idx <= 6 and idx not in ans_indices: ans_indices.append(idx)
            
            explanation = explanation.replace('\n', '<br/>')
            
            updates[current_id] = {
                'question': formatted_q,
                'explanation': explanation,
                'answer': sorted(ans_indices),
                'raw_answer': raw_ans 
            }

    lines = [p.text for p in doc.paragraphs]
    for line in lines:
        raw_line = line # Keep original for question content
        line = re.sub(r'//.*', '', line).strip()
        
        match_id = re_q_id.match(line)
        if match_id:
            finalize_current()
            current_id = int(match_id.group(1))
            current_data = {'explanation': '', 'raw_answer': '', 'question_lines': []}
            state = 'QUESTION_ID_FOUND'
            continue
            
        if current_id is None: continue
            
        if re_q_header.match(line):
            state = 'QUESTION'
            content = re_q_header.sub('', raw_line).strip()
            if content: current_data['question_lines'].append(content)
            continue
            
        if re_opt_header.match(line):
            state = 'OPTIONS'
            continue 
            
        if re_ans_header.match(line):
            state = 'ANSWER'
            content = re_ans_header.sub('', line).strip()
            current_data['raw_answer'] += content
            continue
            
        if re_exp_header.match(line):
            state = 'EXPLANATION'
            content = re_exp_header.sub('', line).strip()
            current_data['explanation'] += content + '\n'
            continue
            
        if state == 'QUESTION':
            current_data['question_lines'].append(raw_line)
        elif state == 'ANSWER':
            current_data['raw_answer'] += line + ' '
        elif state == 'EXPLANATION':
            current_data['explanation'] += line + '\n'

    finalize_current()
    return updates

def update_json(json_path, updates):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    updated_count = 0
    for item in data:
        qid = item.get('id')
        
        # Preserve manual changes for ID 3, 7, 8 and 10
        if qid in [3, 7, 8, 10, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109]:
            continue

        if qid in updates:
            upd = updates[qid]
            
            # Update question
            item['question'] = upd['question']
            
            # Update explanation (always, to ensure string format)
            item['explanation'] = upd['explanation']
            
            # Update answer if parsed
            if upd['answer']:
                item['answer'] = upd['answer']
                # Determine type
                if len(upd['answer']) > 1:
                    item['type'] = 'multiple'
                else:
                    item['type'] = 'single'
            
            updated_count += 1
        else:
            # Even if not in updates, convert question list to string if it is a list
            if isinstance(item.get('question'), list):
                item['question'] = "\n".join(item['question'])

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Updated {updated_count} questions in {json_path}")

if __name__ == '__main__':
    docx_path = 'www/ITS_Csharp/ITS_軟體開發-解答說明0827.docx'
    json_path = 'www/ITS_Csharp/questions_ITS_csharp.json'
    
    print("Parsing DOCX...")
    updates = parse_docx_updates(docx_path)
    print(f"Found updates for {len(updates)} questions.")
    
    print("Updating JSON...")
    update_json(json_path, updates)
    update_json(json_path, updates)