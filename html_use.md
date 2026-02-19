# HTML 常用轉義字元 (HTML Entities) 參考指南

在維護 ITS 題庫或開發網頁時，若內容包含程式碼標籤（如 `<html>`）或特殊符號，必須使用轉義字元，以防止瀏覽器誤判。

## 1. 核心轉義符號 (最常用)
用於顯示程式碼邏輯、標籤符號，防止網頁結構壞掉。

| 顯示符號 | HTML 實體 | 說明 |
| :--- | :--- | :--- |
| `<` | `&lt;` | 小於 (Less than) - **顯示標籤必用** |
| `>` | `&gt;` | 大於 (Greater than) - **顯示標籤必用** |
| `&` | `&amp;` | 連結符 (Ampersand) |
| `"` | `&quot;` | 雙引號 |
| `'` | `&apos;` | 單引號 |

## 2. 空白與排版
HTML 會自動合併連續空格，若需手動排版請用以下字元。

| 顯示符號 | HTML 實體 | 說明 |
| :--- | :--- | :--- |
| (空格) | `&nbsp;` | 不換行空格 (Non-breaking space) |
| (寬空) | `&emsp;` | 全角空格 (一個中文字寬度，縮排好用) |
| `—` | `&mdash;` | 長破折號 |

## 3. 數學與邏輯符號
適合用在考題解析中的運算說明。

| 顯示符號 | HTML 實體 | 說明 |
| :--- | :--- | :--- |
| `×` | `&times;` | 乘法號 |
| `÷` | `&divide;` | 除法號 |
| `≠` | `&ne;` | 不等於 |
| `≤` | `&le;` | 小於等於 |
| `≥` | `&ge;` | 大於等於 |
| `±` | `&plusmn;` | 正負號 |

## 4. 其他特殊符號
| 顯示符號 | HTML 實體 | 說明 |
| :--- | :--- | :--- |
| `©` | `&copy;` | 版權符號 |
| `®` | `&reg;` | 註冊商標 |
| `™` | `&trade;` | 商標 |
| `→` | `&rarr;` | 右箭頭 (流程說明好用) |

---

## 5. CSS 預設樣式與代碼高亮規範 (V3.5+ 標準)
為了簡化 JSON 維護並確保全站視覺一致，系統已在 HTML 中設定了全域預設樣式。**除非特殊需求，否則 JSON 中不需再寫內聯 style。**

### 5.1 系統預設數值 (Default Styles)
當您使用 `<code>` 或在題目區域使用 `<span>` 時，系統會自動套用以下預設：
- **字體大小 (font-size)**: `1.0rem` (專業閱讀感)
- **行高 (line-height)**: `1.4` (黃金閱讀間距)
- **文字顏色 (color)**: `#222222` (深炭灰色，保護眼睛且具權威感)
- **上下間距 (margin)**: `5px 0` (針對 `<code>` 自動撐開距離)

### 5.2 語法高亮 (Prism.js Syntax Highlighting)
若要顯示具備顏色高亮的程式碼，請配合特定的 CSS 類別使用：

| 語言名稱 | 標籤類別 (Class) | 適用場景 |
| :--- | :--- | :--- |
| **C#** | `<code class="language-csharp">` | .NET 開發、ITS Software Development |
| **Python** | `<code class="language-python">` | ITS Python, AI-900 程式題 |
| **SQL** | `<code class="language-sql">` | ITS Database, 資料庫查詢題 |
| **HTML** | `<code class="language-html">` | 網頁前端開發題目 |

**語法高亮注意事項：**
1. **標籤閉合**：務必確保 `</code></pre>` 放在程式碼最後一行，不要把「問題文字」包進去。
2. **自動上色**：系統會在題目切換時自動觸發 `Prism.highlightAll()`，不需額外操作。

---

## 6. JSON 資料格式規範 (Array Format)
為了提高可讀性與維護效率，題目的 `question` 與 `explanation` 欄位建議採用 **字串陣列 (Array of Strings)**：

### 推薦 JSON 結構
```json
"question": [
    "你執行了下列程式碼：<br/>",
    "<pre><code class=\"language-csharp\">int a = 10;",
    "int b = 20;</code></pre>",
    "",
    "程式碼執行完畢之後，result 的值為何？"
]
```
- **優點**：每一行代表網頁上的一個區塊，易於搜尋與修改。
- **自動換行**：陣列中的每一項會被系統自動處理為獨立的顯示行。

---

## 7. 顏色與樣式控制 (Color & Style Control)
若需手動覆蓋預設樣式，請使用 `<span>` 標籤：

| 顏色名稱 | 代碼 | 範例 | 建議用途 |
| :--- | :--- | :--- | :--- |
| **標準藍** | `#0d6efd` | `<span style="color:#0d6efd">強調文字</span>` | 標題、重點、核心提示 |
| **正確綠** | `#198754` | `<span style="color:#198754">正確答案</span>` | 正確答案、解析成功提示 |
| **警示紅** | `#dc3545` | `<span style="color:#dc3545">錯誤警告</span>` | 重要警語、錯誤選項強調 |
| **中性灰** | `#6c757d` | `<span style="color:#6c757d">補充資訊</span>` | 次要內容、背景說明 |

---

## 8. 表格精確控制 (Table Style)
為了確保表格與前後文字有專業的間距感，建議採用以下標準樣式：
```html
<table class='table table-bordered' style='max-width: 350px; color: #000; font-size: 0.9rem; margin: 15px 0; line-height: 1.2;'>
    <tr><td>項目</td><td>內容</td></tr>
</table>
```
- **`max-width: 350px;`**：防止表格在窄螢幕下撐破佈局。
- **`font-size: 0.9rem;`**：讓表格內容呈現專業的學術微調感。
- **`margin: 15px 0;`**：確保表格上下各留出 15px 的呼吸空間。

---

## 9. 程式碼塊去粉紅規範 (No-Pink Rule)
根據系統 V3.4 核心規範，所有代碼塊必須維持專業感：
- **嚴禁粉紅**：禁止在 `<pre>` 或 `<code>` 中出現任何粉紅色系的背景或文字顏色。
- **高亮規範**：必須配合 `language-xxx` 類別使用，顏色應以純黑 (#000) 或語法高亮預設色為主。

---

## 備註：不同環境下的轉換 (對比)
- **HTML**: 使用 `&...;` (如 `&lt;`)
- **CSS**: 使用 `\` 十六進制 (如 `content: "\003c";`)
- **JavaScript**: 使用 `\u` Unicode (如 `\u003c`)

> **提示**：在維護 `questions_xxx.json` 時，若題目出現標籤，請務必將 `<` 換成 `&lt;`，將 `>` 換成 `&gt;`。
