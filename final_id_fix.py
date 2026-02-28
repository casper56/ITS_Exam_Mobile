def final_id_fix():
    file_path = 'final_clean_repair.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修正 submitExam 內部的 HTML ID 與 變數名稱
    # 將 li 變數改為 lIdx 以匹配繪圖邏輯
    content = content.replace('item.left.map((l, li) =>', 'item.left.map((l, lIdx) =>')
    content = content.replace('id="mdl-${idx}-${li}"', 'id="mdl-${idx}-${lIdx}"')
    
    # 同理修正右側 ri
    content = content.replace('item.right.map((r, ri) =>', 'item.right.map((r, rIdx) =>')
    content = content.replace('id="mdr-${idx}-${ri}"', 'id="mdr-${idx}-${rIdx}"')

    # 2. 確保繪圖座標計算參考練習區方式 (純淨 0 補償)
    # 網頁版補償 +120 目前太過，先改回 0 看看是否因為 ID 對了就準了
    content = content.replace('const x2 = rR.left - wRect.left + rR.width/2 + 120;', 'const x2 = rR.left - wRect.left + rR.width/2;')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("ID variables unified. Drawing logic synced.")

if __name__ == "__main__":
    final_id_fix()
