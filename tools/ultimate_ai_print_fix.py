
import os
import re

def ultimate_print_fix(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 強制為所有懸浮按鈕加上 no-print 類別
    content = content.replace('class="zoom-controls', 'class="zoom-controls no-print')
    content = content.replace('class="home-float-btn', 'class="home-float-btn no-print')
    content = content.replace('class="mobile-toggle', 'class="mobile-toggle no-print')
    content = content.replace('class="side-nav-btn', 'class="side-nav-btn no-print')
    
    # 2. 強化 CSS 隱藏邏輯 (暴力移除法)
    print_css_fix = """
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
            }
            body, html { overflow: visible !important; }
        }
    </style>"""
    
    # Replace existing final CSS fix or append before </style>
    if "/* 終極列印隱藏確保 */" in content:
        content = re.sub(r'/\* 終極列印隱藏確保 \*/.*?\}\s*\}', print_css_fix.strip().replace('</style>', ''), content, flags=re.DOTALL)
    else:
        content = content.replace('</style>', print_css_fix)

    # 3. 確保 JS 延遲足夠長
    # Find window.print() and wrap it with enough delay and force a repaint
    print_logic = """
                // 強制隱藏 UI 元件並確保渲染
                document.querySelectorAll('.no-print, .zoom-controls, .home-float-btn, .mobile-toggle, .side-nav-btn, .sidebar').forEach(el => {
                    el.style.setProperty('display', 'none', 'important');
                });
                
                // 延遲執行列印，確保瀏覽器已處理隱藏狀態
                setTimeout(() => {
                    window.print();
                    // 列印完成後不自動恢復，由使用者手動重新整理或點擊，以維持列印環境乾淨
                }, 500);
    """
    
    # Replace the old window.print call or previous setTimeouts
    content = re.sub(r'setTimeout\(\(\) => \{ window\.print\(\); \}, \d+\);', print_logic.strip(), content)
    content = re.sub(r'window\.print\(\);', print_logic.strip(), content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Applied ultimate print fix to {file_path}")

# Target files
files_to_fix = [
    'www/ITS_AI/ITS_AI.html',
    'www/ITS_AI/mock_v34.html'
]

for f in files_to_fix:
    ultimate_print_fix(f)
