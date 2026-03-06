# ITS Exam Mobile 專案結構說明 (V3.6)

本文件詳述專案目錄結構與核心工具用途，供後續維護與開發參考。

## 1. 根目錄核心檔案 (Root Directory)

| 檔案名稱 | 類型 | 用途說明 |
| :--- | :--- | :--- |
| `final_clean_repair.py` | Python 腳本 | **專案維護總司令**。自動修復 HTML 標籤、同步 JSON/JS 資料、校正 UI 佈局規範 (calc(100%-60px))。 |
| `convert_csv_to_json.py` | Python 腳本 | **題庫轉換工具**。負責將外部 CSV 格式題庫轉換為系統標準 JSON。 |
| `study_checklist.html` | HTML | **MOCK 進度追蹤表**。與 MOCK 測驗系統連動，自動記錄 03/06 - 04/04 的學習進度與成績。 |
| `index.html` | HTML | 專案入口首頁。 |
| `package.json` | JSON | Node.js 專案配置與依賴項。 |
| `spec.md` | Markdown | 系統技術規格書與 UI/UX 標準。 |
| `GEMINI.md` | Markdown | 核心 Mandates 與 AI 操作強制規範。 |

## 2. 目錄結構 (Directory Layout)

### `www/` (核心應用程式區)
存放所有科目內容與前端靜態檔案。
*   **`config.json`**：全域科目配置中心（定義題目數量、CUTOFF、路徑等）。
*   **各科目資料夾 (如 `ITS_Python/`, `ITS_Database/`)**：
    *   `mock_v34.html`：各科模擬考試主程式。
    *   `questions_*.json`：該科目的核心題庫資料。
    *   `questions_practice.js`：練習區專用的題庫 JS 封裝（由 `final_clean_repair.py` 自動同步）。
    *   `images/`：存放題目相關圖片。

### `tools/` (維護工具箱)
存放所有過往的一次性修復、批量更新、或是特定問題的處理腳本（移自根目錄）。
*   包含 `fix_*.py`, `repair_*.py`, `update_*.py` 等。

### `backups/` (備份存放區)
存放所有修改前的原始檔案備份（`.bak`）。
*   **規範**：執行任何破壞性修改前，必須先將原始檔移入此處並加上日期後綴。

### `android/` (原生建置區)
Capacitor/Cordova 的 Android 原生專案開發環境，用於打包 APK。

## 3. 核心維護規範 (Maintenance Rules)

1.  **修改題庫後**：必須執行 `python .\final_clean_repair.py` 以確保 `questions_practice.js` 與 JSON 同步，並檢查 HTML 結構。
2.  **重編 ID 規範**：若重編題目 ID，必須同步更新 `www/config.json` 中的 `cutoff` 值，以維持 MOCK 抽題邏輯正確。
3.  **編碼誠信**：所有 JSON 檔案必須維持 UTF-8 編碼，嚴禁使用會破壞編碼的編輯器或腳本。
4.  **UI 標準**：題目容器必須維持 `width: calc(100% - 60px); margin: 20px auto;` 以確保全屏外擴與對齊。

---
*最後更新日期：2026/03/06*
