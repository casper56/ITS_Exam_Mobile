import json
import os

def get_domain(text):
    text = text.lower()
    rules = {
        'D1_資料型別與運算子': ['type(', 'str', 'float', 'int', 'bool', 'list', 'slice', '索引', '切片', '優先順序', '**', '//', ' % ', ' is ', ' in ', 'ord(', 'chr('],
        'D2_流程控制': ['if ', 'elif', 'else', 'while', 'for ', 'break', 'continue', 'range', '迴圈', 'nested'],
        'D3_輸入與輸出': ['input', 'print', 'format', 'f-string', 'open(', 'read', 'write', 'file', '檔案'],
        'D4_程式碼文件與結構': ['def ', 'return', 'class', 'docstring', '註解', 'argument', '參數', 'pass'],
        'D5_錯誤處理與測試': ['try', 'except', 'raise', 'error', 'test', 'assert', 'unittest', '除錯'],
        'D6_模組與工具': ['import', 'math', 'random', 'datetime', 'os.', 'sys.', 'time.'],
        'D7_進階題(APCS/演算法)': ['演算法', 'apcs', 'stack', 'queue', '堆疊', '佇列', '遞迴']
    }
    for domain, keywords in rules.items():
        for kw in keywords:
            if kw in text: return domain
    return 'D1_資料型別與運算子'

def check_distribution():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'www', 'ITS_Python', 'questions_ITS_python.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    core_stats = {}
    supp_stats = {}
    
    for q in questions:
        content = (q.get('question', '') + str(q.get('explanation', ''))).lower()
        cat = get_domain(content)
        
        if q['id'] < 89:
            core_stats[cat] = core_stats.get(cat, 0) + 1
        else:
            supp_stats[cat] = supp_stats.get(cat, 0) + 1

    print("=== 核心題庫 (ID 1-88) 分佈 ===")
    for k, v in core_stats.items():
        print(f"{k}: {v}")
        
    print("\n=== 補充題庫 (ID 89+) 分佈 ===")
    for k, v in supp_stats.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    check_distribution()