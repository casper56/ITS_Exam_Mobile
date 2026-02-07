import json
import re

def auto_classify_report():
    json_path = 'questions_ITS_python.json'
    
    # 分類特徵定義 (可根據需要自行增加)
    rules = {
        'Domain 1 (資料型別)': r'type\(|list|str|float|int|bool|索引|切片|slice|precedence|優先順序|\*\*|//| % | is | in ',
        'Domain 2 (流程控制)': r'if |elif|else:|while|for |break|continue|range|迴圈|iteration',
        'Domain 3 (輸出入)': r'input\(|print\(|format\(|f-string|檔案|read\(|write\(|with open',
        'Domain 4 (函式結構)': r'def |return|引數|參數|argument|function|docstring|註解',
        'Domain 5 (錯誤測試)': r'try:|except|finally|raise|error|unittest|assert|斷言',
        'Domain 6 (模組工具)': r'import |math\.|random\.|datetime\.|os\.|sys\.|randint'
    }

    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    print(f"正在分析 {len(questions)} 題...")
    
    results = {name: [] for name in rules.keys()}
    results['Unclassified'] = []

    for q in questions:
        text = (q.get('question', '') + " " + q.get('explanation', '')).lower()
        matched = False
        for name, pattern in rules.items():
            if re.search(pattern, text):
                results[name].append(q['id'])
                matched = True
                break # 每一題只歸類到第一個匹配到的領域
        if not matched:
            results['Unclassified'].append(q['id'])

    # 輸出成小巧的參考檔
    with open('Classification_Guide.txt', 'w', encoding='utf-8') as f:
        f.write("=== ITS Python 自動分類參考清單 ===

")
        for name, ids in results.items():
            f.write(f"[{name}] 共 {len(ids)} 題
")
            f.write(f"題號: {', '.join(map(str, ids))}

")
    
    print("分類參考檔 'Classification_Guide.txt' 已產生。")

if __name__ == "__main__":
    auto_classify_report()
