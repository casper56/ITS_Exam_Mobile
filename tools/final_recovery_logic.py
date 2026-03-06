
import os
import re

def fix_everything_correctly():
    file_path = 'final_clean_repair.py'
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 修正 A: 物理移除按鈕並恢復 prepareAndPrint 變數 (源頭模板修正) ---
    # 我們針對腳本內的 prepareAndPrint 模板進行精確修復
    new_print_logic = """
                // 顯示處理中遮罩
                const overlay = document.getElementById('loading-overlay');
                if (overlay) overlay.style.display = 'flex';

                // 物理移除所有干擾列印的 UI 元件 (源頭徹底刪除)
                const selectorsToRemove = ['.zoom-controls', '.home-float-btn', '.mobile-toggle', '.side-nav-btn', '.sidebar', '.sidebar-header', '.sidebar-footer', '#progress-stats'];
                selectorsToRemove.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });

                // 記錄原始狀態以便後續恢復
                const oldZoom = document.body.style.zoom || "1.0";
                const content = document.querySelector('.content-area');
                
                // 暫時重置縮放與隱藏側邊欄，確保座標計算基準與列印佈局一致
                document.body.style.zoom = "1.0";
                if (content) content.style.marginLeft = '0';

                const area = document.getElementById('review-area');
                if (!area) return;
                area.style.display = 'block'; // 強制顯示以計算座標
"""
    # 尋找 function prepareAndPrint 的開始部分並替換
    # 我們找到 function 定義後，直到 area.innerHTML 被設定前的那段邏輯
    content = re.sub(
        r'function prepareAndPrint\(onlyMistakes = false\) \{.*?const area = document\.getElementById\('review-area'\);',
        lambda m: f'function prepareAndPrint(onlyMistakes = false) {{{new_print_logic}
                const area = document.getElementById('review-area');',
        content,
        flags=re.DOTALL
    )

    # --- 修正 B: 修正題目題號清理邏輯 (把之前的 '    ' 改回正確的 '$1') ---
    # 這裡有兩處，一處在 mock 模板，一處在練習區模板
    content = content.replace("cleanQ[0].replace(/^((?:<[^>]+>)*)\d+\.\s*/, '    ');", "cleanQ[0].replace(/^((?:<[^>]+>)*)\d+\.\s*/, '$1');")
    content = content.replace("replace(/^((?:<[^>]+>)*)\d+\.\s*/, '    ')", "replace(/^((?:<[^>]+>)*)\d+\.\s*/, '$1')")

    # --- 修正 C: 強化 CSS @media print (確保不破壞原有 CSS) ---
    ultimate_print_css = """
        @media print {
            .zoom-controls, .home-float-btn, .mobile-toggle, .side-nav-btn, .sidebar, .sidebar-header, .sidebar-footer, #progress-stats, .no-print { 
                display: none !important; 
                visibility: hidden !important;
                position: absolute !important;
                top: -9999px !important;
                left: -9999px !important;
                width: 0 !important;
                height: 0 !important;
                opacity: 0 !important;
                pointer-events: none !important;
            }
            body { background: white !important; overflow: visible !important; }
            #review-area { position: static !important; display: block !important; width: 100% !important; margin: 0 !important; padding: 0 !important; }
            .review-item { border-bottom: 1px solid #eee !important; width: 100% !important; page-break-inside: auto; margin: 0 0 10px 0 !important; padding: 0 !important; }
        }
"""
    # 替換腳本中的 CSS 區塊
    content = re.sub(r'@media print\s*\{.*?\}\s*\}', ultimate_print_css.strip(), content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully repaired final_clean_repair.py to its correct state.")

fix_everything_correctly()
