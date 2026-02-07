import json
import re
import os

def classify_by_content(question_obj):
    text = (question_obj.get('question', '') + " " + question_obj.get('explanation', '')).lower()
    
    features = {
        'Domain 1: 資料型別與運算子': [
            'type(', 'datatype', 'string', 'bool', 'boolean', 'float', 'integer', 'list', 'slice', 
            '索引', '切片', '運算子', '優先順序', 'precedence', '==', '>=', '+=', '//', '**', ' % ', ' is ', ' in '
        ],
        'Domain 2: 流程控制': [
            'if ', 'elif', 'else:', '分支', 'while', 'for ', '迴圈', 'iteration', 'break', 'continue', 'range(', 'nested loop'
        ],
        'Domain 3: 輸入與輸出': [
            'input(', 'print(', '格式化', 'format(', 'f-string', '檔案', '讀取', '寫入', 'open(', 'close(', '.read(', '.write(', 'with open', 'argv['
        ],
        'Domain 4: 程式碼文件與結構': [
            '註解', 'comment', 'docstring', '文件', '函式', 'function', 'def ', 'return', '引數', '參數', 'argument', 'signature'
        ],
        'Domain 5: 錯誤處理與測試': [
            '除錯', 'debug', 'error', 'exception', 'try:', 'except', 'finally', 'raise', '測試', 'unittest', 'assert', '斷言'
        ],
        'Domain 6: 模組與工具': [
            'import ', '模組', 'module', 'math.', 'random.', 'datetime.', 'os.', 'sys.', 'randint', 'strftime', 'floor(', 'ceil('
        ]
    }

    scores = {domain: 0 for domain in features.keys()}
    for domain, keywords in features.items():
        for kw in keywords:
            if kw in text:
                scores[domain] += 1
                
    best_domain = max(scores, key=scores.get)
    if scores[best_domain] == 0:
        return "Unclassified (未分類)"
    return best_domain

def analyze_content():
    json_path = 'questions_ITS_python.json'
    output_path = 'ITS_Python_Content_Analysis.md'

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    content_stats = {}
    for q in questions:
        q_id = q.get('id')
        predicted_domain = classify_by_content(q)
        if predicted_domain not in content_stats:
            content_stats[predicted_domain] = []
        content_stats[predicted_domain].append(q_id)

    report = []
    report.append("# ITS Python 題目內容特徵分析報告")
    report.append("\n> 本報告捨棄原始章節標籤，純粹依據題目程式碼與文字內容進行特徵分類。")
    report.append(f"\n- **分析總題數**: {len(questions)}")
    report.append("\n## 內容分類統計\n")
    report.append("| 領域 (依據特徵判定) | 題數 | 佔比 |")
    report.append("| :--- | :---: | :---: |")
    
    sorted_domains = sorted(content_stats.keys())
    for domain in sorted_domains:
        count = len(content_stats[domain])
        perc = (count / len(questions)) * 100
        report.append(f"| {domain} | {count} | {perc:.1f}% |")

    report.append("\n## 領域詳細題號清單\n")
    for domain in sorted_domains:
        ids = content_stats[domain]
        report.append(f"### {domain}")
        chunk_size = 15
        for i in range(0, len(ids), chunk_size):
            chunk = ids[i:i+chunk_size]
            report.append("> " + ", ".join(map(str, chunk)))
        report.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print(f"Content analysis complete. Report saved to {output_path}")

if __name__ == "__main__":
    analyze_content()