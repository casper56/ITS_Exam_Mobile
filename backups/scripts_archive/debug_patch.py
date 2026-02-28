import re

def apply_debug_patch():
    with open('final_clean_repair.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 針對模擬考網頁成績單繪圖點 (L754 附近)
    # 尋找 submitExam 內部的繪圖邏輯
    target_pattern = r'const x2 = rR\.left - wRect\.left \+ rR\.width/2.*?;'
    # 替換為巨大的偏移量並加入 alert
    new_logic = 'const x2 = rR.left - wRect.left + rR.width/2 + 300; console.log("Web Drawing triggered");'
    
    # 全域搜尋並替換所有匹配項
    updated_content = re.sub(target_pattern, new_logic, content)
    
    with open('final_clean_repair.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Debug patch applied successfully.")

if __name__ == "__main__":
    apply_debug_patch()
