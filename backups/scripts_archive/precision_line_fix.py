def precision_line_fix():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # L391 (索引 390) 模擬考答題中
    lines[390] = '                const x2 = (rR.left + rR.width/2 - rect.left) / zoom, y2 = (rR.top + rR.height/2 - rect.top) / zoom;
'
    
    # L1123 (索引 1122) 練習區答題中
    lines[1122] = '                const x2 = (rR.left + rR.width/2 - rect.left) / zoom, y2 = (rR.top + rR.height/2 - rect.top) / zoom;
'
    
    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Precision Line Fix: L391 and L1123 restored to correct Zoom formulas.")

if __name__ == "__main__":
    precision_line_fix()
