import glob
import re

def refine_stats_v6():
    files = glob.glob('www/**/*.html', recursive=True)
    
    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: continue
        
        print(f"Refining stats in {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. 更新 updateUI 中的統計數字邏輯
        # 將 `${visitedSet.size} / ${quizData.length}` 改為 `${Object.keys(userAnswers).length} / ${quizData.length}`
        content = content.replace(
            "document.getElementById('progress-stats').innerText = `${visitedSet.size} / ${quizData.length}`;",
            "document.getElementById('progress-stats').innerText = `${Object.keys(userAnswers).length} / ${quizData.length}`;"
        )

        # 2. 停止記錄點閱 (visited)
        content = content.replace("visitedSet.add(index);", "// visitedSet.add(index);")

        # 3. 清理已不再使用的 visitedSet 相關程式碼
        content = content.replace("let visitedSet = new Set();", "")
        content = content.replace("const savedVisited = localStorage.getItem(STORAGE_KEY);", "")
        # 移除載入邏輯區塊 (使用正則處理多行)
        content = re.sub(r'if \(savedVisited\) \{.*?\}', '', content, flags=re.DOTALL)
        content = content.replace("localStorage.setItem(STORAGE_KEY, JSON.stringify([...visitedSet]));", "")
        content = content.replace("localStorage.removeItem(STORAGE_KEY);", "")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    refine_stats_v6()
