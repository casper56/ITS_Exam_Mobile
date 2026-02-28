import re

def absolute_cleanup_fix():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 徹底重寫 prepareMockPrint (PDF 列印點) - 解決 rL already declared 錯誤
    pdf_block = """                    if (dotL && dotR) {
                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const wRect = wrapper.getBoundingClientRect();
                        // 基準點對齊修正: x1 +5 (縮短起點), x2 -20 (補償 PDF 右側擠壓)
                        const x1 = rL.left - wRect.left + rL.width/2 + 5;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2 - 20;
                        const y2 = rR.top - wRect.top + rR.height/2;"""
    
    # 我們搜尋 pdf 專屬的 dotL 抓取模式
    content = re.sub(r'if \(dotL && dotR\) \{.*?const line = document\.createElementNS', pdf_block + '
                        
                        const line = document.createElementNS', content, flags=re.DOTALL, count=1)

    # 2. 徹底重寫 submitExam 繪圖 (網頁成績單點) - 確保使用 idx 且 0 補償
    web_block = """                    if (dotL && dotR) {
                        const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                        const wRect = wrapper.getBoundingClientRect();
                        // 網頁顯示: 0 補償 (精確對齊)
                        const x1 = rL.left - wRect.left + rL.width/2;
                        const y1 = rL.top - wRect.top + rL.height/2;
                        const x2 = rR.left - wRect.left + rR.width/2;
                        const y2 = rR.top - wRect.top + rR.height/2;"""

    # 針對 submitExam 內的繪圖點 (特徵是 index 附近的 setTimeout)
    # 我們找到 submitExam 函數後的第一個繪圖區塊
    content = re.sub(r'// 繪製模擬考試報告中的正確連線.*?if \(dotL && dotR\) \{.*?const line = document\.createElementNS', '// 繪製模擬考試報告中的正確連線 (視窗座標差值法修正)
        setTimeout(() => {
            document.querySelectorAll('.print-matching').forEach(wrapper => {
                const idx = parseInt(wrapper.getAttribute('data-idx'));
                const item = examQuestions[idx];
                const svg = wrapper.querySelector('.print-svg');
                if (!svg) return;
                const wRect = wrapper.getBoundingClientRect();
                if (wRect.width === 0) return;
                
                svg.setAttribute('width', wRect.width);
                svg.setAttribute('height', wRect.height);
                svg.style.width = wRect.width + 'px';
                svg.style.height = wRect.height + 'px';
                svg.innerHTML = ''; 
                
                const answers = Array.isArray(item.answer) ? item.answer : [item.answer];
                answers.forEach((ansVal, lIdx) => {
                    const rIdx = parseAnswerToIndex(ansVal);
                    const dotL = document.getElementById(`mdl-${idx}-${lIdx}`);
                    const dotR = document.getElementById(`mdr-${idx}-${rIdx}`);
' + web_block + '
                        
                        const line = document.createElementNS', content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Atomic cleanup SUCCESS: SyntaxErrors removed, Logic restored.")

if __name__ == "__main__":
    absolute_cleanup_fix()
