import os

def strengthen_print_and_hide_logic(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the robust hide code
    hide_controls_code = """
                // 強化隱藏所有 UI 元件
                const selectorsToHide = ['.zoom-controls', '.home-float-btn', '.mobile-toggle', '.side-nav-btn', '.sidebar', '.sidebar-header', '.sidebar-footer', '#progress-stats'];
                selectorsToHide.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => {
                        el.style.setProperty('display', 'none', 'important');
                        el.classList.add('no-print');
                    });
                });
    """
    
    # 1. Inject at start of prepareAndPrint
    target_start = "function prepareAndPrint(onlyMistakes = false) {"
    if target_start in content:
        content = content.replace(target_start, target_start + hide_controls_code)

    # 2. Add final CSS override before </style>
    final_css = """
        /* 終極列印隱藏確保 */
        @media print {
            .zoom-controls, .home-float-btn, .mobile-toggle, .side-nav-btn, .sidebar, .sidebar-header, .sidebar-footer, #progress-stats, .no-print { 
                display: none !important; 
                visibility: hidden !important;
                opacity: 0 !important;
                pointer-events: none !important;
            }
        }
    </style>"""
    if "</style>" in content:
        content = content.replace("</style>", final_css)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Strengthened print logic in {file_path}")

# Target files
files_to_fix = [
    'www/ITS_AI/ITS_AI.html',
    'www/ITS_AI/mock_v34.html'
]

for f in files_to_fix:
    strengthen_print_and_hide_logic(f)
