import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修正 CSS：改為靠左對齊佈局
css_left_align = """
        .matching-wrapper { position: relative; margin: 30px 0; padding: 10px; width: 100%; user-select: none; }
        
        .matching-columns { 
            display: flex; 
            justify-content: flex-start; /* 靠左對齊 */
            gap: 120px; /* 控制左右兩欄之間的連線距離 */
            position: relative; 
            z-index: 2; 
            padding-left: 10px;
        }
        
        .match-col { 
            display: flex; 
            flex-direction: column; 
            gap: 25px; 
            min-width: 200px;
        }
        
        .match-title { 
            font-weight: bold; 
            color: #333; 
            font-size: 1.2rem; 
            margin-bottom: 15px; 
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
            width: 100%;
        }
        .match-title-left { text-align: left; }
        .match-title-right { text-align: left; padding-left: 55px; } 
        
        .match-item { display: flex; align-items: center; min-height: 45px; cursor: pointer; }
        .match-item-left { justify-content: flex-end; } /* 內容靠右對齊圓點 */
        .match-item-right { justify-content: flex-start; }
        
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

# 替換 CSS 段落
content = re.sub(r'/\* 完全復刻配對題樣式 \*/.*?#matching-svg \{.*?\}', '/* 完全復刻配對題樣式 */' + css_left_align, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: PC Layout fixed to left-align.")
