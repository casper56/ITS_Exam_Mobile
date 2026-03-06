import re

def apply_final_config():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修正 PDF 版 (prepareMockPrint 內) -> 設定為 -20
    # 我們搜尋帶有 x1 + 5 的那一段，那是 PDF 專屬特徵
    content = re.sub(r'const x2 = rR\.left - wRect\.left \+ rR\.width/2 \+ \d+;', 'const x2 = rR.left - wRect.left + rR.width/2 - 20;', content)
    
    # 2. 修正 網頁版 (submitExam 內) -> 設定為 +120
    # 尋找剛剛 debug 時加入的 +300
    content = content.replace('+ 300; console.log("Web Drawing triggered");', '+ 120;')
    
    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Final configuration applied.")

if __name__ == "__main__":
    apply_final_config()
