# -*- coding: utf-8 -*-
import json
import os

# 配置路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'questions_ITS_python.json')
JS_MOCK_PATH = os.path.join(BASE_DIR, 'questions_data.js')
JS_PRACTICE_PATH = os.path.join(BASE_DIR, 'questions_practice.js')

def update_all():
    print("Starting data synchronization...")
    
    if not os.path.exists(JSON_PATH):
        print(f"Error: Cannot find {JSON_PATH}")
        return

    # 1. 讀取 JSON
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 2. 生成 JS 檔案
    with open(JS_MOCK_PATH, 'w', encoding='utf-8') as f:
        f.write(f"const allQuestions = {json.dumps(questions, ensure_ascii=False)};")
    
    with open(JS_PRACTICE_PATH, 'w', encoding='utf-8') as f:
        f.write(f"const quizData = {json.dumps(questions, ensure_ascii=False)};")
    
    print("✓ JS data files synchronized with latest JSON.")

if __name__ == "__main__":
    update_all()
