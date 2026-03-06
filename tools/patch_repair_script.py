
import os

def fix_script_source():
    file_path = 'final_clean_repair.py'
    if not os.path.exists(file_path):
        print("Error: final_clean_repair.py not found")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修改腳本內的 prepareAndPrint 模板，改為「物理移除」按鈕
    # 尋找模板中的隱藏邏輯並替換為物理移除
    old_hide_block = """
                if (zoomBtns) zoomBtns.style.display = 'none';
                if (homeBtn) homeBtn.style.display = 'none';
"""
    new_hide_block = """
                // 物理移除所有干擾列印的 UI 元件 (源頭刪除)
                const selectorsToRemove = ['.zoom-controls', '.home-float-btn', '.mobile-toggle', '.side-nav-btn', '.sidebar', '.sidebar-header', '.sidebar-footer', '#progress-stats'];
                selectorsToRemove.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });
"""
    
    if old_hide_block in content:
        content = content.replace(old_hide_block, new_hide_block)
    else:
        # 嘗試更通用的替換，針對所有可能的變體
        content = content.replace("if (zoomBtns) zoomBtns.style.display = 'none';", new_hide_block)
        content = content.replace("if (homeBtn) homeBtn.style.display = 'none';", "")

    # 2. 強化 @media print CSS 模板 (在腳本內的 CSS 區塊)
    # 確保腳本在修復 HTML 時，會注入最強力的隱藏 CSS
    ultimate_css = """
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
        }
"""
    # 替換腳本中 CSS 模板的部分
    if "@media print" in content:
        # 這裡較複雜，假設腳本中有一個固定的 CSS 區塊
        import re
        content = re.sub(r'@media print\s*\{.*?\}\s*\}', ultimate_css.strip(), content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully patched final_clean_repair.py source code.")

# 執行源頭修正
fix_script_source()
