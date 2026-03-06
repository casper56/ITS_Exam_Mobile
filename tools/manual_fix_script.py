
import os

file_path = 'final_clean_repair.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修正題號清理產生的空格
content = content.replace("'    '", "'$1'")

# 2. 恢復 prepareAndPrint 遺失的變數
bad_block = """
                const area = document.getElementById('review-area');
                if (!area) return;
"""
good_block = """
                // 物理移除所有干擾列印的 UI 元件
                const selectorsToRemove = ['.zoom-controls', '.home-float-btn', '.mobile-toggle', '.side-nav-btn', '.sidebar', '.sidebar-header', '.sidebar-footer', '#progress-stats'];
                selectorsToRemove.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });

                const overlay = document.getElementById('loading-overlay');
                if (overlay) overlay.style.display = 'flex';

                const content = document.querySelector('.content-area');
                document.body.style.zoom = "1.0";
                if (content) content.style.marginLeft = '0';

                const area = document.getElementById('review-area');
                if (!area) return;
"""
content = content.replace(bad_block, good_block)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Manually fixed final_clean_repair.py")
