import re

def apply_mock_only_fix():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 識別並還原 練習區 (prac_bottom_tmpl 內部) 的所有繪圖點為 0 補償
    # 練習區特徵：位於 prepareAndPrint 函數內，且引用 quizData
    # 我們尋找 L1300 之後的練習區繪圖邏輯
    prac_pattern = r'(quizData\[qIdx\].*?const x2 = rR\.left - wRect\.left \+ rR\.width/2).*?;'
    # 強行將練習區的所有補償歸零
    content = re.sub(prac_pattern, r'\1;', content)

    # 2. 確保 模擬考 (Mock) 維持分離補償
    # 網頁成績單 (L745 附近) -> 保持 +120
    # PDF 列印 (L249 附近) -> 保持 -20
    # 答題中 (drawLines) -> 保持 0 (已在之前還原)

    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Mock-only rule applied. Practice area restored to 0 offset.")

if __name__ == "__main__":
    apply_mock_only_fix()
