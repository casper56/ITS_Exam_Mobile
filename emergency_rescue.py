def rescue_logic():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # 1. 修復答題中 (window.drawLines) - 必須有 zoom
        if 'const x2 = rR.left - wRect.left + rR.width/2 + 120;' in line and '/ zoom' in line:
             indent = line[:line.find('const')]
             new_lines.append(f'{indent}const x2 = (rR.left + rR.width/2 - rect.left) / zoom; // 修正: 還原答題模式公式
')
        
        # 2. 針對被誤改的 L391 和 L1123 (即使沒寫 / zoom 的情況)
        elif 'const x2 = rR.left - wRect.left + rR.width/2 + 120;' in line and ('rect.left' in line or 'drawLines' in line or line.startswith('                const x2')):
             indent = line[:line.find('const')]
             new_lines.append(f'{indent}const x2 = (rR.left + rR.width/2 - rect.left) / zoom;
')

        else:
            new_lines.append(line)
            
    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Emergency Rescue: Correct formulas restored.")

if __name__ == "__main__":
    rescue_logic()
