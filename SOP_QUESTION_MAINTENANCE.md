# ITS 題庫管理標準作業程序 (SOP) - 題目刪除與重編

本文件定義了在 ITS 測驗系統中刪除題目、重新編號及更新系統配置的標準流程，以確保資料完整性與統計數據的一致性。

## 🛠 處理流程

### 1. 備份與記錄 (Backup)
*   **動作**：將原始 JSON 備份至 `backups/`。
*   **目的**：發生錯誤時可隨時還原。
*   **紀錄**：記錄被刪除題目的原 ID 與類別（例如：ID 78, D3 類別）。

### 2. JSON 資料清理 (Data Cleaning)
*   **動作 1 (刪除)**：從 JSON 陣列中移除重複或錯誤的題目。
*   **動作 2 (標記清理)**：確保 `options` 欄位不含 `A. B. C.` 等字樣。
*   **動作 3 (重編 ID)**：執行 `reorder_ids.py`，確保 ID 從 1 開始且連續。
    *   *注意：ID 順序會影響官方題 (Pool A) 與補充題 (Pool B) 的界線。*

### 3. 系統配置同步 (Config Sync)
*   **檔案路徑**：`www/config.json`
*   **修改項**：
    *   `cutoff`：若刪除的是官方題，需依刪除題數減少此數值。
    *   `cutoff_info`：同步更新描述文字（如 "1-101 為官方版"）。

### 4. 統計與文件更新 (Docs Sync)
*   **README.md**：更新該科目的官方題數統計。
*   **科目文件** (如 `ITS_softdevelop.md`)：
    *   重新統計 D1~D5 各類別題數。
    *   更新百分比分佈。
    *   更新 Pool A/B 的 ID 範圍說明。

### 5. 模擬測驗出題評估 (Mock Exam Assessment)
*   **權重核對**：刪題後需核對 D1~D5 各類別是否仍有足夠題目進行隨機抽題。
*   **抽題邏輯檢查**：
    *   若程式碼中有寫死 ID 範圍，需同步更新。
    *   評估是否需要調整「隨機抽題比例」，確保模擬考的體感與正式考一致。

### 6. 驗證與提交 (Verification & Git)
*   **驗證**：在 Web 預覽模式下檢查是否有跳號或圖片載入失敗。
*   **提交**：
    ```bash
    git add .
    git commit -m "refactor: delete duplicate questions and rebase IDs for [Subject]"
    git push
    ```

---
*最後更新日期：2026-02-18*
