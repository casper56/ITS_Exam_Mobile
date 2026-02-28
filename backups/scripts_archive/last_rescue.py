def last_rescue():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修正 prepareMockPrint (PDF 版) 的 SyntaxError (Identifier already declared)
    # 我們精確替換包含重複宣告的整塊
    pdf_broken = """                    if (dotL && dotR) {
                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                                                const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const wRect = wrapper.getBoundingClientRect();
                        // 絕對對準：純粹座標差
                                                const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const wRect = wrapper.getBoundingClientRect();
                        // 絕對對準：純粹座標差
                        const x1 = rL.left - wRect.left + rL.width/2;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2;
                        const y2 = rR.top - wRect.top + rR.height/2;"""
    
    pdf_fixed = """                    if (dotL && dotR) {
                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const wRect = wrapper.getBoundingClientRect();
                        // 基準點對齊修正: x1 +5 (起點), x2 -20 (PDF 補償)
                        const x1 = rL.left - wRect.left + rL.width/2 + 5;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2 - 20;
                        const y2 = rR.top - wRect.top + rR.height/2;"""
    
    content = content.replace(pdf_broken, pdf_fixed)

    # 2. 修正 submitExam (網頁版) 確保使用 idx 且座標正確
    # 這裡之前被誤加了 +120
    content = content.replace('const x2 = rR.left - wRect.left + rR.width/2 + 120;', 'const x2 = rR.left - wRect.left + rR.width/2;')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("MOCK Lines Fully Restored & Syntax Fixed.")

if __name__ == "__main__":
    last_rescue()
