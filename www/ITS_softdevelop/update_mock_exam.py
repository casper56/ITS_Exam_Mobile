import json
import os
import re

def get_domain(question_data):
    text = (question_data.get('question', '') + str(question_data.get('explanation', ''))).lower()
    rules = {
        'D5_資料庫': ['sql', 'database', '資料表', 'delete', 'select', 'update', 'insert', 'transaction', '正規化', '1nf', '2nf', '3nf', 'erd', 'nosql', 'linq', '預存程序', 'procedure'],
        'D4_網頁應用程式': ['html', 'css', 'javascript', 'xhr', 'http', 'api', 'mvc', 'mvvm', 'iis', '伺服器', 'json', 'xml', 'oauth', '網頁', '樣式表'],
        'D3_物件導向程式設計': ['class', 'interface', '介面', '抽象', 'abstract', '繼承', 'inheritance', '多型', 'polymorphism', '封裝', 'encapsulation', 'protected', 'private', 'public', 'override', 'virtual', '建構函式', 'constructor', '衍生'],
        'D2_軟體開發原則': ['git', 'github', 'commit', 'push', 'pull', 'branch', 'merge', 'sdlc', '生命週期', 'stack', 'queue', '堆疊', '佇列', '連結清單', 'linked list', '排序', '搜尋', '加密', '雜湊', '簽章', 'csrf'],
        'D1_核心程式設計概念': ['int', 'double', 'float', 'string', 'bool', 'byte', 'decimal', 'if ', 'else', 'while', 'for ', 'switch', 'try', 'catch', 'finally', 'delegate', 'event', '委派', '事件', '例外', '資料型別']
    }
    for domain, keywords in rules.items():
        for kw in keywords:
            if kw.lower() in text: return domain
    return 'D1_核心程式設計概念'

def update_mock_exam():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'questions_ITS_csharp.json')
    template_path = os.path.join(os.path.dirname(base_dir), 'ITS_Python', 'mock_exam.html')
    output_path = os.path.join(base_dir, 'mock_exam.html')

    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    for q in questions:
        q['category'] = get_domain(q)

    # 這裡我們使用 ensure_ascii=True 來確保所有非 ASCII 字元都變成長像 \uXXXX 的形式
    # 這能 100% 避免編碼產生的 JavaScript Token 錯誤
    json_str = json.dumps(questions, ensure_ascii=True)

    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace('ITS Python 模擬考試', 'ITS Software Development 模擬考試')
    html = html.replace('prism-python.min.js', 'prism-csharp.min.js')
    html = html.replace('language-python', 'language-csharp')
    html = html.replace('its_python_wrong_ids', 'its_softdevelop_wrong_ids')
    
    new_categories = "[ 'D1_核心程式設計概念', 'D2_軟體開發原則', 'D3_物件導向程式設計', 'D4_網頁應用程式', 'D5_資料庫' ]"
    html = re.sub(r'const categories = \[.*?\];', f'const categories = {new_categories};', html, flags=re.DOTALL)

    # 使用穩定搜尋取代
    marker_start = 'const allQuestions = ['
    start_pos = html.find(marker_start)
    if start_pos != -1:
        # 尋找 let examQuestions 作為區塊結束點，徹底清除中間所有殘留
        end_marker = 'let examQuestions = [];'
        end_pos = html.find(end_marker, start_pos)
        if end_pos != -1:
            html = html[:start_pos] + f'const allQuestions = {json_str};\n    ' + html[end_pos:]

    html = html.replace('if (d1Count < 17)', 'if (d1Count < 12)')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed with ASCII escape: {output_path}")

if __name__ == "__main__":
    update_mock_exam()
