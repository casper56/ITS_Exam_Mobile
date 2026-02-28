import glob
import os

def patch_matching_header():
    # 遍歷所有 HTML 檔案
    files = glob.glob('www/**/*.html', recursive=True)
    target_text = '<div class="match-header-title">回答區</div>'
    new_text = '<div class="match-header-title" style="width:50px; line-height:1.2; text-align:left;">回答區</div>'
    
    count = 0
    for f in files:
        # 只針對模擬考與練習區檔案
        if 'mock_v34.html' in f or ('ITS_' in f and f.endswith('.html')):
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                if target_text in content:
                    print(f"正在更新: {f}")
                    updated_content = content.replace(target_text, new_text)
                    with open(f, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    count += 1
            except Exception as e:
                print(f"讀取 {f} 時出錯: {e}")
                
    print(f"完成！共更新 {count} 個檔案。")

if __name__ == "__main__":
    patch_matching_header()
