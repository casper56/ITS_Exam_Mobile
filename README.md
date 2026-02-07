# ITS 認證模擬測驗 行動應用程式 (ITS Exam Mobile)

本專案是一款專為準備 ITS (Information Technology Specialist) 及 Microsoft 相關認證考試而設計的模擬測驗行動應用程式。基於 Capacitor 與原生 Web 技術開發，目前主要針對 **Android** 平台提供行動端練習體驗。

## 📱 主要功能說明

### 1. 多樣化考科分類
*   首頁提供直觀的考科選擇介面。
*   支援考科包含：Python 程式設計、C# 軟體開發、Database 資料庫管理、AI 人工智慧基礎、Azure AI-900、AZ-900 等。

### 2. 智慧作答與確認機制
*   **即時反饋**：答題後立即標示對錯，並自動開啟詳細的「正確答案」與「題目解析」區塊。
*   **多種題型支援**：完整支援單選題、複選題及複雜的題組（Multi-option）類型。

### 3. 進度管理與記憶功能
*   **作答紀錄追蹤**：系統會以顏色標示（⚪未讀、🟢答對、🔴答錯）方便重點複習。
*   **自動還原狀態**：重新進入頁面時，系統會自動恢復先前的作答紀錄與解析顯示。

### 4. 閱讀體驗優化
*   **靈活縮放**：提供縮放按鈕並支援行動裝置兩指撥弄 (Pinch-to-zoom) 手勢。
*   **語法高亮**：內建 Prism.js 支援程式碼區塊排版，解決橫向溢出問題。

## 📦 如何取得 APK (Android)

本專案已設定 **GitHub Actions 雲端自動化編譯**，您無需在本地安裝複雜的 Android 開發環境即可取得安裝檔。

1.  **推送變更**：將代碼 `git push` 到 GitHub 後。
2.  **查看 Actions**：前往 GitHub 儲存庫的 **"Actions"** 標籤頁。
3.  **下載產物**：點擊最近一次成功的 **"Build Android APK"** 工作，在頁面最下方的 **"Artifacts"** 下載 `app-debug` 壓縮檔。
4.  **安裝**：解壓後將 `app-debug.apk` 傳送至手機安裝即可。

*詳情請參閱 [BUILD_APK.md](./BUILD_APK.md)*

## 🐍 內容產生工具 (Python 腳本)

如果您需要修改題庫 JSON 並重新產生網頁或 PDF，請使用以下工具：

### 環境準備
```powershell
python -m pip install reportlab Pillow
```

### 執行指令
切換到考科目錄（如 `www/ITS_Python`）執行：
*   **更新網頁**：`python json_to_html.py` (採優化後的緊湊版面)
*   **產生 PDF**：`python json_to_pdf.py` (具備自動相依性檢查)

---
*本專案僅供學習與考照準備使用。*