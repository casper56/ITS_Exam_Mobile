import re

def fix_separation():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 先把練習區（Practice）整塊救回來
    # 練習區特徵：程式碼中有 quizData[qIdx] 且位於 prepareAndPrint 內
    # 找到那行被誤加 +120 的代碼並歸零
    content = content.replace('const x2 = rR.left - wRect.left + rR.width/2 + 120;', 'const x2 = rR.left - wRect.left + rR.width/2;')
    
    # 2. 重新『精確』替換模擬考網頁版（Mock Web）
    # 模擬考特徵：程式碼中有 examQuestions[qIdx] 且位於 submitExam 內
    # 我們搜尋 L745 附近的區塊（剛才被歸零了，現在精確加回去）
    mock_web_marker = 'const item = examQuestions[qIdx];'
    # 我們找 mock_web_marker 之後的第一個 x2 計算並改為 +120
    # 這裡使用 split 分段處理，確保只改到模擬考網頁部分
    parts = content.split('function submitExam() {')
    if len(parts) > 1:
        # 在 submitExam 的內容中尋找
        parts[1] = parts[1].replace('const x2 = rR.left - wRect.left + rR.width/2;', 'const x2 = rR.left - wRect.left + rR.width/2 + 120;')
        content = 'function submitExam() {'.join(parts)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed: Practice restored to 0, Mock Web restored to +120.")

if __name__ == "__main__":
    fix_separation()
