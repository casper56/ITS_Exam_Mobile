import glob
import re

def refine_ui_v7():
    files = glob.glob('www/**/*.html', recursive=True)
    
    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: continue
        
        print(f"Refining sidebar text in {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 更新 updateUI 中的文字邏輯
        # 尋找我們在 v6 加入的邏輯並替換
        old_pattern = r"document\.getElementById\('progress-stats'\)\.innerText = `\$\{Object\.keys\(userAnswers\)\.length\} / \$\{quizData\.length\}`;"
        new_logic = "document.getElementById('progress-stats').innerText = `第 ${currentIndex + 1} 題 / 共 ${quizData.length} 題`;"
        
        if 'progress-stats' in content:
            content = re.sub(old_pattern, new_logic, content)
            # 也要處理初始化的 HTML 部分 (預設顯示)
            content = re.sub(r'<small class="text-white-50" id="progress-stats">.*?</small>', 
                            '<small class="text-white-50" id="progress-stats"></small>', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    refine_ui_v7()
