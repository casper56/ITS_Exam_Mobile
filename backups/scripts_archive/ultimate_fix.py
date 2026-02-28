import re

def apply_500px_test():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 強力全域替換：將所有用於模擬考成績單網頁顯示的 x2 公式全部改為 500
    # 規則：只要不是帶有 -20 或 x1+5 (PDF特徵) 的，全部強制改為 500
    
    # 識別 PDF 版並保護
    content = content.replace('const x2 = rR.left - wRect.left + rR.width/2 - 20;', 'const x2 = PDF_MARKER;')
    
    # 替換所有可能的網頁繪圖點 (包含 const x2 = rR.left... 和之前的 +120)
    # 使用 Regex 覆蓋所有變體
    content = re.sub(r'const x2 = rR\.left - wRect\.left \+ rR\.width/2.*?;', 'const x2 = 500;', content)
    
    # 還原 PDF 版
    content = content.replace('const x2 = PDF_MARKER;', 'const x2 = rR.left - wRect.left + rR.width/2 - 20;')
    
    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("500px Test Applied to all web result points.")

if __name__ == "__main__":
    apply_500px_test()
