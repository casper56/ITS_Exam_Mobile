import re

def apply_final_fix():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # 1. 識別 PDF 補償點 (特徵是包含 x1 + 5 或 -20)
        if 'x1 + 5' in line or '- 20' in line:
            new_lines.append(line)
            continue
        
        # 2. 識別所有其他的網頁繪圖點 (包含 500, +120, 或零補償)
        # 我們強制將這些點統一設定為 +120
        if 'const x2 = rR.left - wRect.left' in line or 'const x2 = 500' in line or 'const x2 = (rR.left' in line:
            # 保留原本的縮進
            indent = line[:line.find('const')]
            # 判斷是否為答題中 (含有 zoom)
            if '/ zoom' in line:
                new_lines.append(f'{indent}const x2 = (rR.left + rR.width/2 - rect.left) / zoom + 120; // 全域網頁補償
')
            else:
                new_lines.append(f'{indent}const x2 = rR.left - wRect.left + rR.width/2 + 120; // 全域網頁補償
')
        else:
            new_lines.append(line)
            
    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("All drawing points synchronized to +120px successfully.")

if __name__ == "__main__":
    apply_final_fix()
