import os

def clean_conflict_markers(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    clean_lines = []
    skip = False
    for line in lines:
        # Check for Git markers
        if line.startswith('<<<<<<<') or line.startswith('=======') or line.startswith('>>>>>>>'):
            continue
        # Also handle cases where marker might be slightly indented
        stripped = line.strip()
        if stripped.startswith('<<<<<<<') or stripped.startswith('>>>>>>>') or stripped.startswith('======='):
            continue
        clean_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
    print(f"Cleaned {file_path}")

files_to_clean = [
    'www/ITS_Python/questions_ITS_python.json',
    'www/ITS_Python/ITS_Python.html',
    'www/ITS_Python/mock_exam.html'
]

for f in files_to_clean:
    clean_conflict_markers(f)
