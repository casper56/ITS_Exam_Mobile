def final_atomic_fix():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 不論縮排、不論前後文，只要看到 x2 計算公式，除了 PDF 特徵外全部改為 500
    import re
    
    # 1. 保護 PDF 版 (L251)
    content = content.replace('const x2 = rR.left - wRect.left + rR.width/2 - 20;', 'const x2 = PDF_MARKER;')
    
    # 2. 強力替換所有 x2 = ... 為 x2 = 500;
    # 覆蓋 L393, L747, L1125, L1350
    content = re.sub(r'const x2 = [^;]+;', 'const x2 = 500;', content)
    
    # 3. 還原 PDF 版
    content = content.replace('const x2 = PDF_MARKER;', 'const x2 = rR.left - wRect.left + rR.width/2 - 20;')
    
    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Atomic 500px fix applied to all points.")

if __name__ == "__main__":
    final_atomic_fix()
