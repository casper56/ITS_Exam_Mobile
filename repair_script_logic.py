
import os
import re

def repair_final_clean_script():
    file_path = 'final_clean_repair.py'
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修正 prepareAndPrint 函式開頭，確保變數定義存在且執行物理移除
    # 我們尋找函式開始的部分並替換為穩定版本
    old_start_pattern = re.compile(r'function prepareAndPrint\(onlyMistakes = false\) \{.*?const area = document\.getElementById\('review-area'\);', re.DOTALL)
    
    stable_start = """function prepareAndPrint(onlyMistakes = false) {
                let targetItems = quizData.map((item, idx) => ({ item, idx }));
                let title = "REPLACE_TITLE 認證完整解析";
                if (onlyMistakes) {
                    targetItems = targetItems.filter(({ idx }) => incorrectSet.has(idx) || correctedSet.has(idx));
                    if (targetItems.length === 0) { alert('目前沒有錯題或訂正紀錄可供列印！'); return; }
                    title = "REPLACE_TITLE 訂正解析講義";
                }

                // 物理移除所有干擾列印的 UI 元件
                const selectorsToRemove = ['.zoom-controls', '.home-float-btn', '.mobile-toggle', '.side-nav-btn', '.sidebar', '.sidebar-header', '.sidebar-footer', '#progress-stats'];
                selectorsToRemove.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });

                const overlay = document.getElementById('loading-overlay');
                if (overlay) overlay.style.display = 'flex';

                // 記錄原始狀態以便後續恢復 (雖然已移除，但保留變數以防後續邏輯報錯)
                const oldZoom = document.body.style.zoom || "1.0";
                const content = document.querySelector('.content-area');
                document.body.style.zoom = "1.0";
                if (content) content.style.marginLeft = '0';

                const area = document.getElementById('review-area');"""
    
    if old_start_pattern.search(content):
        content = old_start_pattern.sub(stable_start, content)

    # 2. 修正題號清理邏輯 (不留空白)
    content = content.replace("cleanQ[0].replace(/^((?:<[^>]+>)*)\d+\.\s*/, '    ');", "cleanQ[0].replace(/^((?:<[^>]+>)*)\d+\.\s*/, '$1');")
    
    # 3. 確保 CSS @media print 區塊包含對 review-item 的修正
    print_css = """
        @media print {
            @page { size: auto; margin: 8mm !important; }
            .no-print { display: none !important; }
            body { background: white !important; overflow: visible !important; }
            #review-area { position: static !important; display: block !important; width: 100% !important; margin: 0 !important; padding: 0 !important; }
            .review-item { border-bottom: 1px solid #eee !important; width: 100% !important; page-break-inside: auto; margin: 0 0 10px 0 !important; padding: 0 !important; }
            .review-ans { color: #198754 !important; font-weight: bold !important; padding: 8px 5px !important; border-left: 5px solid #198754 !important; margin: 5px 0 !important; }
        }"""
    
    # 使用正則替換 @media print 區塊，確保不破壞其他部分
    content = re.sub(r'@media print\s*\{.*?\}\s*\}', print_css.strip(), content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Repaired final_clean_repair.py.")

repair_final_clean_script()
