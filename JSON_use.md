# ITS 測驗系統 JSON 資料格式與使用規範

本文件彙整了目前 ITS 測驗系統 (`questions_*.json`) 所使用的資料格式規範與重點要求，以確保資料完整性與前端渲染正確。

## 1. JSON 基本結構與編碼要求
*   **資料結構**：整個 JSON 檔案為一個**陣列 (Array)**，陣列中的每一個**物件 (Object)** 代表一個獨立的考題。
*   **編碼格式**：必須儲存為 **UTF-8 (無 BOM)**。專案規範中有嚴格要求，絕不能有編碼錯誤。
*   **陣列化字串 (V3.4.6 規範)**：為避免單行字串過長導致渲染問題，所有長文本欄位（如 `question`, `explanation`, `slots` 等）**強制使用「字串陣列 (Array of Strings)」** 來表示，每一行代表陣列中的一個元素。

---

## 2. 共用核心欄位 (所有題型必備)
```json
{
  "id": 1, 
  "type": "single",
  "category": "D1_資料型別與運算子",
  "weight": 1,
  "image": null,
  "question": [
    "<pre><code class=\"language-python\">【CH01-1】這是題目第一行",
    "這是題目第二行</code></pre>"
  ],
  "explanation": [
    "<pre><code class=\"language-python\">解題分析：",
    "1. 這裡是詳解說明...</code></pre>"
  ]
}
```
*   **`id` (Number)**：題號。必須從 1 開始且連續，系統會根據 `config.json` 中的 `cutoff` 值，利用 ID 來區分「官方題 (Pool A)」與「補充題 (Pool B)」。
*   **`type` (String)**：題型。支援 `single` (單選)、`multiple` (複選)、`multioption` (多選)、`choicelist` (填充/下拉選單)、`matching` (配對)。
*   **`category` (String)**：題目所屬類別。用於統計分析與模擬測驗抽題權重。
*   **`weight` (Number)**：佔分權重，通常設定為 `1`。
*   **`image` (String | null)**：若題目有附圖，填寫圖片路徑（如 `"images/q1.png"`）；無圖則設為 `null`。
*   **`question` / `explanation` (Array of Strings)**：題目與詳解內容。支援寫入 HTML 標籤（如 `<pre><code class="language-python">`）以高亮程式碼。

---

## 3. 題型專屬欄位

### A. 選擇題 (`single`, `multiple`, `multioption`)
*   **`options` (Array of Strings)**：選項內容的陣列。
    *   **⚠️ 嚴格規範**：選項內**絕對禁止**手動加入 `A.`, `B.`, `(A)`, `(B)` 等前綴字樣，前端 UI 會自動動態加上。
*   **`answer` (String 或 Array)**：正確答案。單選題通常是 `"A"` 或是 `["A"]`，複選題則為 `["A", "C"]` 等。

### B. 填充選單題 (`choicelist`)
用於程式碼填空，每個空格會有一個下拉選單。
*   **`slots` (Array of Strings)**：包含程式碼與挖空標籤的陣列。挖空處必須使用 `<slot01>`, `<slot02>` 等特定標籤。
*   **`options` (Array of Strings)**：提供給所有 `<slot>` 選擇的可用選項庫。
*   **`answer` (Array of Strings)**：對應每一個 slot 的正確選項，例如 `["C", "A", "A"]`。

### C. 配對題 (`matching`)
*   **`left` (Array of Strings)**：要配對的左側項目（通常是題目或變數）。
*   **`right` (Array of Strings)**：可供選擇的右側目標項目（通常是型別或結果）。
*   **`answer` (Array of Strings)**：左側項目依序對應到的右側正確選項，例如 `["A", "B", "C", "D", "C"]`。

---

## 4. 進階與樣式控制欄位 (選填)

### A. 字體縮放 (`sz`)
*   **`sz` (String)**：自訂特定題目的字體大小 (例如：`"0.95rem"`)。若題目程式碼過多可用此縮小字體以防破版。

### B. 選項標籤控制 (`labelType`)
`labelType` 用來改變前端選項標籤的顯示風格。預設會自動加上英文字母標籤 `(A), (B), (C)`（**但若未定義 `labelType`，系統將自動視為 `"none"`，不會顯示任何前綴標籤**）。

1. **設置為數字標籤 (`"num"`)**
   如果題目要求選項是按照順序步驟排列，設定為 `"labelType": "num"`，會將選項標籤轉為 `1.`, `2.`, `3.`。
   ```json
   {
     "id": 10,
     "type": "single",
     "labelType": "num",
     "question": ["請選擇正確的執行步驟："],
     "options": ["開啟檔案", "寫入資料", "關閉檔案"],
     "answer": "A"
   }
   ```
2. **隱藏標籤 (`"none"` 或未定義，或使用 `"hideLabel": true`)**
   如果不希望出現任何字母或數字前綴，設定為 `"labelType": "none"`，**或是直接不設定該欄位**，系統將預設隱藏標籤。
   另外，你也可以使用 `"hideLabel": true` 來達到完全相同的隱藏效果。
   ```json
   {
     "id": 11,
     "type": "single",
     "hideLabel": true,
     "question": ["以下哪一個是 Python 的保留字？"],
     "options": ["def", "function", "define"],
     "answer": "A"
   }
   ```
> **注意**：使用 `labelType` 時，請確保 `options` 內的文字本身是純淨的（不含任何標籤前綴），讓前端程式自動負責渲染前綴即可。

---

## 🚨 異動與維護 SOP 提醒
1. **備份優先**：修改前必須將 JSON 備份到 `backups/` 資料夾。
2. **重編題號與 Cutoff**：刪題導致 ID 變動時，必須確保 ID 連續，並同步修改 `www/config.json` 中的 `cutoff` 數量。
3. **重建與驗證**：只要修改過任何 JSON 或 HTML 內容，**強制要求**必須執行 `python .\final_clean_repair.py` 來重新封裝生成對應的 HTML 與 JavaScript 檔案。
