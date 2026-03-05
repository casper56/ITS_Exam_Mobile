
import os
import re

def fix_mock_table_css():
    file_path = 'final_clean_repair.py'
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 補回遺失的 MOCK 表格與統計樣式
    missing_css = """
        /* MOCK 統計表與題目表格樣式 */
        .q-table td { vertical-align: middle; } 
        .header-bg { background: #f8f9fa !important; font-weight: bold; text-align: center; } 
        .category-title { background: #e2e3e5 !important; font-weight: bold; color: #383d41; } 
        .code-font { font-family: 'Cascadia Code', Consolas, monospace; color: #0056b3; font-size: 13px; }
        
        /* 確保表格基本樣式存在 */
        .q-table, table { width: 100%; border-collapse: collapse; margin: 15px 0; border: 1px solid #000; }
        .q-table th, .q-table td, table th, table td { border: 1px solid #000; padding: 10px 8px; vertical-align: top; }
    """
    
    # 尋找 CSS 區塊並插入
    if "</style>" in content:
        # 插入在 </style> 之前，但避免重複插入
        if ".header-bg" not in content:
            content = content.replace("</style>", missing_css + "
    </style>")
            print("Successfully restored missing CSS to final_clean_repair.py")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 執行修復
fix_mock_table_css()
