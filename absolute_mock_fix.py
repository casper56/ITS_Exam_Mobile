import re

def absolute_mock_line_fix():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修復 HTML 結構 (確保 ID 與 類別正確)
    content = content.replace('id="pmock-${idx}"', 'id="print-match-${idx}"')

    # 2. 徹底重寫 prepareMockPrint (PDF 列印點)
    # 這裡使用最穩定的座標抓取方式
    pdf_logic = """                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const wRect = wrapper.getBoundingClientRect();
                        // 絕對對準：純粹座標差
                        const x1 = rL.left - wRect.left + rL.width/2;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2 - 20;
                        const y2 = rR.top - wRect.top + rR.height/2;"""
    
    # 3. 徹底重寫 submitExam 繪圖 (網頁成績單點)
    web_logic = """                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const wRect = wrapper.getBoundingClientRect();
                        // 絕對對準：純粹座標差
                        const x1 = rL.left - wRect.left + rL.width/2;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2;
                        const y2 = rR.top - wRect.top + rR.height/2;"""

    # 執行強力替換，確保變數 y1 一定存在且公式正確
    # 針對 PDF 點
    content = re.sub(r'const x1 = rL\.left - wRect\.left \+ rL\.width/2 \+ 5;.*?const y2 = rR\.top - wRect\.top \+ rR\.height/2;', pdf_logic, content, flags=re.DOTALL)
    # 針對 Web 點
    content = re.sub(r'const x1 = rL\.left - wRect\.left \+ rL\.width/2;.*?const y2 = rR\.top - wRect\.top \+ rR\.height/2;', web_logic, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("MOCK Lines Restored: Web(0), PDF(-20).")

if __name__ == "__main__":
    absolute_mock_line_fix()
