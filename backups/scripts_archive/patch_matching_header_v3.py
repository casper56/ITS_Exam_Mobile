import glob
import os
import re

def patch_matching_header_v3():
    files = glob.glob('www/**/*.html', recursive=True)
    # 匹配 <div class="match-header-title">回答區</div>，不論其是否有 style
    pattern = re.compile(r'<div class="match-header-title"[^>]*>回答區</div>')
    new_text = '<div class="match-header-title" style="width:80px; text-align:left; white-space:nowrap;">回答區</div>'
    
    count = 0
    for f in files:
        if 'mock_v34.html' in f or ('ITS_' in f and f.endswith('.html')):
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                if pattern.search(content):
                    print(f"正在修正: {f}")
                    updated_content = pattern.sub(new_text, content)
                    with open(f, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    count += 1
            except Exception as e:
                print(f"處理 {f} 時出錯: {e}")
                
    print(f"完成！共修正 {count} 個檔案。")

if __name__ == "__main__":
    patch_matching_header_v3()
