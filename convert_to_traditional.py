import json
import os
from opencc import OpenCC

# 初始化 OpenCC (s2twp: 簡體到台灣正體並修正常用詞)
cc = OpenCC('s2twp')

def convert_content(data):
    if isinstance(data, str):
        return cc.convert(data)
    elif isinstance(data, list):
        return [convert_content(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_content(value) for key, value in data.items()}
    else:
        return data

# 需要處理的術語手動微調 (s2twp 有時不夠完美)
manual_fixes = {
    "列表": "串列",
    "清单": "清單",
    "元组": "元組",
    "变量": "變數",
    "程序": "程式",
    "函数": "函式",
    "布尔": "布林",
    "字典": "字典",
    "集合": "集合"
}

def final_polish(text):
    if not isinstance(text, str):
        return text
    for key, val in manual_fixes.items():
        text = text.replace(key, val)
    return text

# 遍歷 www 目錄
for root, dirs, files in os.walk('www'):
    for file in files:
        if file.startswith('questions_') and file.endswith('.json'):
            file_path = os.path.join(root, file)
            print(f"Converting {file_path} to Traditional Chinese...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 轉換
            converted_data = convert_content(data)
            
            # 寫回
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(converted_data, f, ensure_ascii=False, indent=4)

print("Conversion complete.")
