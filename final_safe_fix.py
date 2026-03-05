
import os

def final_safe_print_fix():
    file_path = 'final_clean_repair.py'
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 修正 1: 物理移除 UI (不宣告變數，防止重複宣告錯誤) ---
    # 尋找這兩行並替換
    old_logic = """
                if (zoomBtns) zoomBtns.style.display = 'none';
                if (homeBtn) homeBtn.style.display = 'none';
"""
    new_logic = """
                // 物理移除所有干擾列印的 UI 元件 (源頭刪除)
                ['.zoom-controls', '.home-float-btn', '.mobile-toggle', '.side-nav-btn', '.sidebar', '.sidebar-header', '.sidebar-footer', '#progress-stats'].forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });
"""
    # 執行精確替換 (僅此處改動)
    if old_logic in content:
        content = content.replace(old_logic, new_logic)
    else:
        # 通用匹配
        content = content.replace("if (zoomBtns) zoomBtns.style.display = 'none';", new_logic)
        content = content.replace("if (homeBtn) homeBtn.style.display = 'none';", "")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully applied safe print fix to final_clean_repair.py")

# 執行修正
final_safe_print_fix()
