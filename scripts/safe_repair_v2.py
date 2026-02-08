import os

def final_safe_repair():
    path = 'www/ITS_Python/questions_ITS_python.json'
    if not os.path.exists(path): return
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    clean_lines = []
    last_was_category = False
    
    for l in lines:
        strip_l = l.strip()
        if strip_l.startswith('<<<<<<<') or strip_l.startswith('=======') or strip_l.startswith('>>>>>>>'):
            continue
            
        is_category = '"category":' in l
        if is_category and last_was_category:
            continue 
            
        if is_category:
            last_was_category = True
            if len(clean_lines) > 0:
                prev = clean_lines[-1].rstrip()
                if prev.endswith('"'):
                    clean_lines[-1] = prev + ',' + chr(10)
        else:
            if strip_l != "":
                last_was_category = False
                
        clean_lines.append(l)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
    print("Safe Repair Completed.")

final_safe_repair()
