
import os

def fix_mock_print_source():
    file_path = 'final_clean_repair.py'
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 修正 MOCK 模板內的 prepareMockPrint 函式 ---
    # 尋找 MOCK 列印前的按鈕隱藏邏輯並替換為物理移除
    # 這裡針對的是 mock_top_tmpl 內部的 JavaScript
    old_mock_hide = """
            setTimeout(() => {
                window.print();
                if (overlay) overlay.style.display = 'none';
                // 注意：在「考試結束」畫面中，這些按鈕應保持隱藏，不可恢復 display: 'flex'
"""
    new_mock_hide = """
            setTimeout(() => {
                // 物理移除所有干擾列印的 UI 元件 (MOCK 專用源頭刪除)
                ['.zoom-controls', '.home-float-btn', '.mobile-toggle', '.side-nav-btn', '.sidebar', '.sidebar-header', '.sidebar-footer', '#progress-stats'].forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });
                
                window.print();
                if (overlay) overlay.style.display = 'none';
"""
    
    if old_mock_hide in content:
        content = content.replace(old_mock_hide, new_mock_hide)
    else:
        # 通用匹配，針對更廣泛的變體
        content = content.replace("window.print();", "document.querySelectorAll('.home-float-btn, .zoom-controls, .side-nav-btn, .mobile-toggle').forEach(el => el.remove()); window.print();")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully patched MOCK print logic in final_clean_repair.py")

# 執行 MOCK 修正
fix_mock_print_source()
