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
        # Skip git markers
        if strip_l.startswith('<<<<<<<') or strip_l.startswith('=======') or strip_l.startswith('>>>>>>>'):
            continue
            
        # Check for duplicated category property
        is_category = '"category":' in l
        if is_category and last_was_category:
            continue # Skip this duplicated line
            
        if is_category:
            last_was_category = True
            # Check if previous line ended with a quote but no comma
            if len(clean_lines) > 0:
                prev = clean_lines[-1].rstrip()
                if prev.endswith('"') and not prev.endswith(','):
                    clean_lines[-1] = prev + ',
'
        else:
            if strip_l != "": # don't reset on empty lines
                last_was_category = False
                
        clean_lines.append(l)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
    print("Safe Repair Completed.")

final_safe_repair()
