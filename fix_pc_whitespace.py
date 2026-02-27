import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 重構 CSS：改為緊湊且置中的佈局，消除左側空白
css_compact = """
        .matching-wrapper { position: relative; margin: 40px auto; padding: 10px; max-width: 900px; user-select: none; }
        
        .matching-columns { 
            display: flex; 
            justify-content: center; /* 整個區塊置中 */
            gap: 100px; /* 控制左右兩欄之間的連線距離 */
            position: relative; 
            z-index: 2; 
        }
        
        .match-col { 
            display: flex; 
            flex-direction: column; 
            gap: 25px; 
            min-width: 250px; /* 確保欄位有足夠空間 */
        }
        
        /* 標題樣式：直接放在欄位頂部 */
        .match-title { 
            font-weight: bold; 
            color: #333; 
            font-size: 1.2rem; 
            margin-bottom: 15px; 
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }
        .match-title-left { text-align: left; padding-left: 0; }
        .match-title-right { text-align: left; padding-left: 55px; } /* 對齊圓點後的文字 */
        
        .match-item { display: flex; align-items: center; min-height: 45px; cursor: pointer; }
        .match-item-left { justify-content: flex-end; text-align: right; }
        .match-item-right { justify-content: flex-start; text-align: left; }
        
        .match-dot {
            width: 22px; height: 22px;
            border: 1.5px solid #333; border-radius: 50%;
            margin: 0 15px; display: flex; align-items: center; justify-content: center;
            background: #fff; position: relative; flex-shrink: 0;
        }
        .match-dot::after {
            content: ""; width: 10px; height: 10px;
            background: transparent; border-radius: 50%; transition: all 0.1s;
        }
        .match-item.matched .match-dot::after, .match-item.selected .match-dot::after { background: #333; }
        .match-item.selected .match-dot { border-color: #0d6efd; }
        
        #matching-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
"""

# 替換舊的 CSS
content = re.sub(r'/\* 完全復刻配對題樣式 \*/.*?#matching-svg \{.*?\}', '/* 完全復刻配對題樣式 */' + css_compact, content, flags=re.DOTALL)

# 2. 更新 renderMatchingQuestion：將標題移入欄位內部以達成精準對齊
new_html_structure = """
        html += `<div class="matching-wrapper" id="matching-wrapper" onmousemove="handleDragMove(event)" onmouseup="handleDragEnd(event)" ontouchmove="handleDragMove(event)" ontouchend="handleDragEnd(event)">
                    <svg id="matching-svg"></svg>
                    <div class="matching-columns">
                        <!-- 左側：程式碼片段欄 -->
                        <div class="match-col left-col">
                            <div class="match-title match-title-left">程式碼片段</div>`;
        item.left.forEach((text, lIdx) => {
            const isMatched = currentAns[lIdx] !== null;
            html += `<div class="match-item match-item-left ${isMatched?'matched':''}" id="left-item-${lIdx}">
                        <div style="font-family:Consolas,monospace; font-size:1.1rem;">${text}</div>
                        <div class="match-dot" id="dot-left-${lIdx}" onmousedown="handleDragStart(event, 'left', ${lIdx})" ontouchstart="handleDragStart(event, 'left', ${lIdx})"></div>
                     </div>`;
        });
        html += `</div>
                        <!-- 右側：回答區欄 -->
                        <div class="match-col right-col">
                            <div class="match-title match-title-right">回答區</div>`;
        item.right.forEach((text, rIdx) => {
            const isMatchedByAny = currentAns.includes(rIdx);
            html += `<div class="match-item match-item-right ${isMatchedByAny?'matched':''}" id="right-item-${rIdx}" data-right-idx="${rIdx}">
                        <div class="match-dot" id="dot-right-${rIdx}"></div>
                        <div style="font-family:sans-serif; font-size:1.1rem;">${text}</div>
                     </div>`;
        });
        html += `</div></div></div>`;
"""

# 使用正則替換 renderMatchingQuestion 內部的 HTML 結構
content = re.sub(r'html \+= `<div class="matching-wrapper".*?html \+= `</div></div></div>`;', new_html_structure, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: PC Layout fixed. Whitespace removed and headers aligned.")
激進
