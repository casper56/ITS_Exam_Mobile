# 更新紀錄 (Changelog)

## [V3.1] - 2026-02-13
### 🚀 核心技術轉型：前端列印引擎 (Browser-side Printing)
- **捨棄 Python 後端生成 PDF**：由於 `reportlab` 難以 100% 模擬現代 CSS 陰影與圓角，全面改用前端 `window.print()` 技術。
- **動態解析渲染區**：新增 `#review-area` 容器，平時隱藏，僅在點擊「列印預覽」時由 JavaScript 遍歷 JSON 即時生成高格調 HTML 結構。
- **PDF 預設檔名實作**：在 `prepareAndPrint` 函式中，透過暫時修改 `document.title` 來欺騙作業系統的列印存檔視窗，實現自動命名（如 `ITS Software Development.pdf`）。

### 🎨 視覺格調深度訂製 (1:1 復刻)
- **去粉紅規則 (Kill Bootstrap Pink)**：
  - 核心 CSS 強制覆蓋：`code { color: inherit !important; background-color: transparent !important; }`。
  - 徹底解決了 Bootstrap 預設將 `<code>` 標籤顯示為粉紅色的問題，回歸純淨黑/灰配色。
- **專業選項外觀**：
  - **純圓圈化**：將所有單選、複選、題組的 `checkbox/radio` 統一改為圓形 (`border-radius: 50%`)。
  - **無勾勾設計**：使用 `background-image: none !important` 移除勾選圖示，僅保留實心填充色。
- **模擬考格調 (V3.1 版)**：
  - **綠裝飾條**：正確答案左側 5px 粗線。
  - **灰色解析盒**：`#f8f9fa` 背景 + `1px #eee` 邊框 + `10px` 圓角。

### 🧠 互動邏輯優化
- **離題自動檢查 (Evaluate on Leave)**：
  - 實作 `evaluateCurrentQuestion()` 邏輯。
  - 使用者在複選題或題組題中，若「已勾選但未完成」即按上下頁或側邊欄切換題目，系統會自動將該題標示為「紅色 (錯誤)」，確保進度不會消失。
- **橘色訂正流程**：
  - 題目判定狀態分為：`correct` (一次答對)、`incorrect` (答錯)、`corrected` (答錯後改對)。
  - `corrected` 狀態在 UI 上顯示為橘色，且此狀態下選項會被鎖定以防再次修改。
- **題型自動偵測**：
  - 透過 JS 判定 `item.type === 'multiple'` 或選項包含 `|` 來自動標註「單選」、「複選」或「題組」標籤。

### 📦 資料清洗與維護
- **強制 UTF-8 編碼標準**：
  - 全專案（JSON, HTML, JS, PY）統一採用 **UTF-8 (無 BOM)** 編碼。
  - 解決了當機後因編碼衝突導致的 `SyntaxError` 與網頁亂碼問題。
- **ITS_Database 重編**：完成全題庫 ID 重編 (1-103)，並同步更新題目內文開頭的 `^\d+\.` 序號。
- **同步工具化**：確立 `final_clean_repair.py` 為萬用同步引擎，支援全科目目錄偵測、標題映射與專業檔名配置。

### 📌 關鍵記憶
- **ITS 流出題**：編號僅限 **1 至 69**，後續題目均為補充。
