# ITS 測驗系統 UI/UX 規格 (V3.2)

## 1. 導覽按鈕 (Navigation Buttons)
*   **尺寸**: 寬 `25px`, 高 `65px`
*   **圓角**: `15px` (長方形圓角樣式)
*   **顏色**: 背景 `rgba(13, 110, 253, 0.7)`，文字 `white`
*   **Hover**: 背景變為 `#0d6efd`，**寬度固定 25px (不變寬)**
*   **層級**: `z-index: 2000` (確保不被選單擋住)
*   **定位**:
    *   **模擬考**: 貼齊螢幕邊緣 (`left: 0`, `right: 0`)
    *   **自主練習**: 
        *   電腦版：上一題 `left: 280px` (避開側邊欄)，下一題 `right: 0`
        *   手機版：上一題 `left: 0` (側邊欄隱藏時)

## 2. 顯示區域與邊距 (Layout)
*   **單邊留白 (Border Gap)**: **30px** (按鈕 25px + 5px 間隙)
*   **寬度計算**: `width: calc(100% - 60px)`
*   **最大寬度**: `1200px`
*   **對齊**: **水平置中** (`margin-left: auto; margin-right: auto`)
*   **內距**: 容器 `padding` 必須為 `0`，避免累積留白。

## 3. 字體與顏色 (Typography)
*   **題目內容**: `1.05rem`, 純黑色 (`#000`)
*   **選項文字**: `1rem`, 純黑色 (`#000`)
*   **程式碼高亮**:
    *   **Prism 主題**: `prism-solarized-light.min.css` (適合白底)
    *   **去粉紅規則**: `code { background-color: transparent !important; }`
    *   **清晰度**: 禁止使用 `color: inherit !important` 覆蓋程式碼顏色。
