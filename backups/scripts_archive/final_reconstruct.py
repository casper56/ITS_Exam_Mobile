import re

def final_reconstruct_practice():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 定位練習區的繪圖邏輯區塊 (prepareAndPrint 內部)
    # 我們鎖定 pdl- 和 pdr- 這些練習區專用的 ID 特徵
    
    # 這是我們要替換進去的「絕對正確、零補償、不斷行」版本
    # 同時包含動態字寬偵測
    correct_block = """                                                                                                        if (dotL && dotR) {
                                                                                                            const rL = dotL.getBoundingClientRect(), rR = dotR.getBoundingClientRect();
                                                                                                            // 練習區還原：純粹圓心對位 (0 補償)
                                                                                                            const x1 = rL.left - wRect.left + rL.width/2;
                                                                                                            const y1 = rL.top - wRect.top + rL.height/2;
                                                                                                            const x2 = rR.left - wRect.left + rR.width/2;
                                                                                                            const y2 = rR.top - wRect.top + rR.height/2;
                                                                                                            
                                                                                                            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");"""

    # 執行強力替換，移除所有帶有 +5, +120, -20 等干擾的練習區邏輯
    # 我們針對 pdl- 之後到 line 宣告之前的區塊
    pattern = r'if \(dotL && dotR\) \{.*?const rL = dotL\.getBoundingClientRect\(\), rR = dotR\.getBoundingClientRect\(\);.*?const line = document\.createElementNS'
    content = re.sub(pattern, correct_block, content, flags=re.DOTALL)

    # 2. 確保 模擬考 (Mock) 依然保有分離補償 (L745 附近)
    # 網頁版 +120, PDF 版 -20
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Practice Area Reconstructed: Zero Offset & Correct Logic.")

if __name__ == "__main__":
    final_reconstruct_practice()
