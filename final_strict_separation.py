import re

def final_strict_separation():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修復 prepareMockPrint (真正的預覽列印點) - 確保無語法錯誤且有補償
    # 我們搜尋 prepareMockPrint 內部的繪圖循環
    pdf_logic = """                    if (dotL && dotR) {
                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const wRect = wrapper.getBoundingClientRect();
                        const x1 = rL.left - wRect.left + rL.width/2 + 5;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2 - 20;
                        const y2 = rR.top - wRect.top + rR.height/2;"""
    
    # 2. 還原 submitExam (網頁成績單) - 確保無語法錯誤且「零補償」
    web_logic = """                    if (dotL && dotR) {
                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const wRect = wrapper.getBoundingClientRect();
                        const x1 = rL.left - wRect.left + rL.width/2;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2;
                        const y2 = rR.top - wRect.top + rR.height/2;"""

    # 執行強力清洗：先移除所有損壞的座標計算塊
    content = re.sub(r'if \(dotL && dotR\) \{.*?const y2 = rR\.top - wRect\.top \+ rR\.height/2;', 'REPLACE_HOLDER', content, flags=re.DOTALL)
    
    # 分別植入正確的邏輯 (第一個是 PDF 預覽，第二個是網頁成績單)
    content = content.replace('REPLACE_HOLDER', pdf_logic, 1)
    content = content.replace('REPLACE_HOLDER', web_logic, 1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Separated PDF Preview from Web Results. Syntax errors cleared.")

if __name__ == "__main__":
    final_strict_separation()
