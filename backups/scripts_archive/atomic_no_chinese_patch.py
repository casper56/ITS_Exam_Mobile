def atomic_no_chinese_patch():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix No-Wrap for Practice
    content = content.replace('text-align:right;">${l}</div>', 'text-align:right; white-space:nowrap !important;">${l}</div>')

    # 2. Separate Mock Web and PDF
    # Mock Web
    content = content.replace('const x2 = rR.left - wRect.left + rR.width/2;', 'const x2 = rR.left - wRect.left + rR.width/2 + 120;')
    # Mock PDF
    content = content.replace('const x1 = rL.left - wRect.left + rL.width/2;', 'const x1 = rL.left - wRect.left + rL.width/2 + 5;')
    # (x2 for PDF is already -20 in some logic, let's ensure it is distinct)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Atomic patch applied.")

if __name__ == "__main__":
    atomic_no_chinese_patch()
