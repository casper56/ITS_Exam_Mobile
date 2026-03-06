
import os
import re

def ultimate_print_fix_global(file_path):
    if not file_path.endswith('.html') or not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False

    # 1. 強制為所有懸浮按鈕加上 no-print 類別 (如果還沒有)
    replacements = {
        'class="zoom-controls"': 'class="zoom-controls no-print"',
        'class="home-float-btn"': 'class="home-float-btn no-print"',
        'class="mobile-toggle"': 'class="mobile-toggle no-print"',
        'class="side-nav-btn"': 'class="side-nav-btn no-print"'
    }
    
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            modified = True

    # 2. 強化 CSS 隱藏邏輯 (暴力移除法)
    print_css_fix = """
        /* 終極列印隱藏確保 */
        @media print {
            .no-print, .zoom-controls, .home-float-btn, .mobile-toggle, .side-nav-btn, .sidebar, .sidebar-header, .sidebar-footer, #progress-stats { 
                display: none !important; 
                visibility: hidden !important;
                position: absolute !important;
                top: -9999px !important;
                left: -9999px !important;
                width: 0 !important;
                height: 0 !important;
                z-index: -1 !important;
                pointer-events: none !important;
            }
            body, html { overflow: visible !important; }
        }
    </style>"""
    
    if "/* 終極列印隱藏確保 */" not in content and "</style>" in content:
        content = content.replace('</style>', print_css_fix)
        modified = True

    # 3. 確保 JS 延遲足夠長
    print_logic = """
                // 強制隱藏 UI 元件並確保渲染
                document.querySelectorAll('.no-print, .zoom-controls, .home-float-btn, .mobile-toggle, .side-nav-btn, .sidebar').forEach(el => {
                    el.style.setProperty('display', 'none', 'important');
                });
                
                // 延遲執行列印，確保瀏覽器已處理隱藏狀態
                setTimeout(() => {
                    window.print();
                }, 500);
    """
    
    # Replace the old window.print call if it's not already using the delayed logic
    if "window.print();" in content and "setTimeout(() => {" not in content.split("window.print();")[0][-50:]:
        # Remove any existing simple setTimeout print
        content = re.sub(r'setTimeout\(\(\) => \{ window\.print\(\); \}, \d+\);', '', content)
        # Replace the direct print
        content = re.sub(r'window\.print\(\);', print_logic.strip(), content)
        modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied ultimate print fix to {file_path}")
        return True
    return False

# 遍歷 www 目錄
fixed_count = 0
for root, dirs, files in os.walk('www'):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            if ultimate_print_fix_global(file_path):
                fixed_count += 1

print(f"Total files fixed: {fixed_count}")
