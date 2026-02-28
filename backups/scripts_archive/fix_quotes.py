import os

path = 'final_clean_repair.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修正 handleDragStart 的引號衝突問題
# 將 'left' 改為 "left" (使用 double quotes 避開單引號衝突)
content = content.replace("handleDragStart(event,'left',", 'handleDragStart(event,"left",')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Quoting conflict fixed in template.")
