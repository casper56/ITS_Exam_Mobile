
import os
import re

template = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REPLACE_TITLE</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css">
    <style>
        body { background-color: #f8f9fa; font-family: "Microsoft JhengHei", sans-serif; padding: 40px 0; }
        .container { max-width: 950px; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        h1, h2, h3 { color: #0d6efd; border-bottom: 2px solid #0d6efd; padding-bottom: 10px; margin-top: 30px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; border: 1px solid #dee2e6; font-size: 0.95rem; }
        th, td { border: 1px solid #dee2e6; padding: 12px; vertical-align: top; word-break: break-word; }
        th { background-color: #212529; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        code { color: #d63384; font-family: Consolas, monospace; }
        pre { background: #f1f1f1; padding: 15px; border-radius: 8px; overflow-x: auto; }
        .btn-home { position: fixed; top: 20px; right: 20px; z-index: 1000; }
        @media (max-width: 768px) { .container { padding: 20px; } table { font-size: 0.8rem; } }
    </style>
</head>
<body>
    <a href="../index.html" class="btn btn-dark btn-home">🏠 回首頁</a>
    <div class="container">
        <div id="content"></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script>
        const rawMd = `REPLACE_MD_CONTENT`;
        document.getElementById('content').innerHTML = marked.parse(rawMd);
        Prism.highlightAll();
    </script>
</body>
</html>
"""

md_files = [
    'ITS_AI_TECH.md', 'ITS_DATABASE_TECH.md', 'ITS_SOFTDEVELOP.md', 'ITS_Python_TECH.md'
]

for md_name in md_files:
    path = os.path.join('www', md_name)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 處理反引號轉義，防止破壞 JS 字串
        safe_content = content.replace('', '').replace('`', '`').replace('$', '\$')
        
        title = md_name.replace('.md', '').replace('_', ' ')
        html_content = template.replace('REPLACE_TITLE', title).replace('REPLACE_MD_CONTENT', safe_content)
        
        output_name = md_name.replace('.md', '.html')
        with open(os.path.join('www', output_name), 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Generated: {output_name}")

print("All technical HTML pages generated successfully.")
