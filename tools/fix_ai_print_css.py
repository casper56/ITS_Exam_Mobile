
import os

def fix_print_css(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the print CSS block to ensure everything is hidden
    print_styles = """
        @media print {
            @page { size: auto; margin: 8mm !important; }
            * { box-sizing: border-box !important; -webkit-print-color-adjust: exact; overflow: visible !important; }
            html, body { margin: 0 !important; padding: 0 !important; width: 100% !important; background: white !important; font-size: 1.0rem !important; line-height: 1.8 !important; }
            .main-wrapper, .mobile-toggle, .side-nav-btn, .no-print, .sidebar, .sidebar-header, .sidebar-footer, .zoom-controls, .home-float-btn, #progress-stats { display: none !important; }
            .content-area { margin-left: 0 !important; padding: 0 !important; margin-top: 0 !important; }
            #review-area { display: block !important; width: 100% !important; padding: 0 !important; margin: 0 !important; }
            .review-item { border-bottom: 1px solid #eee !important; width: 100% !important; page-break-inside: auto; margin: 0 0 10px 0 !important; padding: 0 !important; }
            .review-ans { color: #198754 !important; font-weight: bold !important; padding: 8px 5px !important; border-left: 5px solid #198754 !important; margin: 5px 0 !important; }
            pre, code { white-space: pre-wrap !important; word-break: break-all !important; border: none !important; font-size: 1.0rem !important; margin: 0 !important; padding: 0 !important; }
            .q-table, table { font-size: 0.7rem !important; max-width: 98% !important; margin: 10px 0 !important; page-break-inside: avoid; -webkit-print-color-adjust: exact; border-collapse: collapse !important; }
            .q-table td, .q-table th, td, th { border: 1px solid #000 !important; padding: 6px !important; }
        }"""
    
    # Find the existing @media print block and replace it
    import re
    # This regex tries to find the @media print { ... } block
    # It handles nested braces by matching until the final closing brace of the media query
    pattern = re.compile(r'@media print\s*\{.*?\}\s*\}', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(print_styles.strip(), content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated print styles in {file_path}")
    else:
        # If not found with nested brace, try simple match
        pattern_simple = re.compile(r'@media print\s*\{.*?\}', re.DOTALL)
        if pattern_simple.search(content):
            new_content = pattern_simple.sub(print_styles.strip(), content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated simple print styles in {file_path}")
        else:
            print(f"Could not find @media print in {file_path}")

# Target files
files_to_fix = [
    'www/ITS_AI/ITS_AI.html',
    'www/ITS_AI/mock_v34.html'
]

for f in files_to_fix:
    fix_print_css(f)
