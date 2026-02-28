import glob
import os

def patch_matching_header_v2():
    # 遍歷所有 HTML 檔案
    files = glob.glob('www/**/*.html', recursive=True)
    # 這是剛才設定的「兩行版」目標
    target_text = '<div class="match-header-title" style="width:50px; line-height:1.2; text-align:left;">回答區</div>'
    # 這是新的「一行固定寬度版」
    new_text = '<div class="match-header-title" style="width:80px; text-align:left; white-space:nowrap;">回答區</div>'
    
    count = 0
    for f in files:
        if 'mock_v34.html' in f or ('ITS_' in f and f.endswith('.html')):
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                if target_text in content:
                    print(f"正在恢復一行顯示: {f}")
                    updated_content = content.replace(target_text, new_text)
                    with open(f, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    count += 1
            except Exception as e:
                print(f"讀取 {f} 時出錯: {e}")
                
    print(f"完成！共修正 {count} 個檔案。")

if __name__ == "__main__":
    patch_matching_header_v2()
