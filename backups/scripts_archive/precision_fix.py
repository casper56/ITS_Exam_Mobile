import re

def final_precision_restoration():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 還原答題中的連線 (window.drawLines) -> 設為 0 補償
    # 特徵是包含 rect.left 和 zoom
    content = re.sub(r'const x2 = 500; // 答題中模式', 'const x2 = (rR.left + rR.width/2 - rect.left) / zoom;', content)
    # 也要捕捉沒註解的版本 (L393, L1125)
    content = content.replace('const x2 = 500; y2 = (rR.top + rR.height/2 - rect.top) / zoom;', 'const x2 = (rR.left + rR.width/2 - rect.left) / zoom; const y2 = (rR.top + rR.height/2 - rect.top) / zoom;')
    
    # 2. 設定網頁成績單/解析連線 (L747, L1350) -> 設為 +120
    # 特徵是包含 rR.left - wRect.left
    content = content.replace('const x2 = 500; // 網頁成績單模式', 'const x2 = rR.left - wRect.left + rR.width/2 + 120;')
    # 捕捉其他的 500 (L747, L1350)
    content = re.sub(r'const x2 = 500;', 'const x2 = rR.left - wRect.left + rR.width/2 + 120;', content)
    
    # 3. 確保 PDF 專屬點維持 -20 (L251)
    # 如果剛剛被誤改了，這裡強行校正
    if 'const x2 = rR.left - wRect.left + rR.width/2 - 20;' not in content:
         content = re.sub(r'const x1 = rL\.left - wRect\.left \+ rL\.width/2 \+ 5;.*?const x2 = [^;]+;', 'const x1 = rL.left - wRect.left + rL.width/2 + 5; const x2 = rR.left - wRect.left + rR.width/2 - 20;', content, flags=re.DOTALL)

    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Precision Restoration Applied.")

if __name__ == "__main__":
    final_precision_restoration()
