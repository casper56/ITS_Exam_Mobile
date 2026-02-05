# Git 操作指南

本專案採用 **Git** 進行版本控制，並使用 **GitHub** 作為遠端儲存庫與雲端編譯平台。

## 🌲 分支說明
- **`main`**: 正式分支，存放最穩定且測試過的內容。
- **`dev`**: 開發分支，所有的新題目補充、程式修復請在此分支進行。

---

## 🛠️ 常用指令流程

### 1. 切換開發分支
開始修改題目或程式前，請確保您在 `dev` 分支：
```bash
git checkout dev
```

### 2. 同步並提交變更 (Commit)
當您修改了 `www/` 目錄下的題目或程式後，請執行以下步驟：
```bash
# 1. 檢視變更狀態
git status

# 2. 將所有變更加入暫存區
git add .

# 3. 提交變更並說明原因
git commit -m "Update: 補充 Python 第 119-125 題"
```

### 3. 推送到雲端 (Push)
將本地的變更同步到 GitHub，這也會觸發 **自動化編譯 (APK Build)**：
```bash
git push origin dev
```

---

## 🚀 同步與下載流程

1. **修改**：在本地修改 `www/` 中的 JSON。
2. **同步 HTML/PDF**：執行當地的 `json_to_html.py` 與 `json_to_pdf.py`。
3. **Commit & Push**：依照上述 Git 流程推送到 `dev`。
4. **下載 APK**：前往 GitHub -> Actions -> 下載生成的 `app-debug`。

---

## 🧹 清理與維護
如果您發現遠端分支名稱混亂，可以使用以下指令清理：
```bash
# 同步遠端分支狀態並移除已不存在的分支
git fetch --all --prune
```
