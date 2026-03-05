
import os

def fix_css():
    file_path = 'final_clean_repair.py'
    if not os.path.exists(file_path): return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 直接補回遺失的統計表 CSS
    if ".header-bg" not in content:
        css_to_add = """
        .q-table td { vertical-align: middle; } 
        .header-bg { background: #f8f9fa !important; font-weight: bold; text-align: center; } 
        .category-title { background: #e2e3e5 !important; font-weight: bold; color: #383d41; } 
        .code-font { font-family: 'Cascadia Code', Consolas, monospace; color: #0056b3; font-size: 13px; }
    """
        content = content.replace("</style>", css_to_add + "
    </style>", 1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Restored MOCK Table CSS")

fix_css()
