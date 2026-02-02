import glob
import re

def fix_width_v16():
    files = glob.glob('www/**/*.html', recursive=True)
    
    width_fix_css = """
        /* --- Width Fix V16 --- */
        pre, code {
            white-space: pre-wrap !important;       /* 讓程式碼自動換行 */
            word-wrap: break-word !important;
            word-break: break-all !important;
        }
        .question-body {
            padding: 20px !important;               /* 縮小內邊距，增加顯示寬度 */
        }
        .content-area {
            padding: 15px !important;
        }
        img, .question-image {
            max-width: 100% !important;
            height: auto !important;
        }
        @media (max-width: 576px) {
            .question-body {
                padding: 10px !important;
            }
            .content-area {
                padding: 10px !important;
            }
        }
        /* --------------------- */
"""

    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: continue
        
        print(f"Applying width fix to {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '/* --- Width Fix V16 --- */' not in content:
            # 注入 CSS 到 </style> 標籤前
            content = content.replace('</style>', width_fix_css + '\n    </style>')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_width_v16()
