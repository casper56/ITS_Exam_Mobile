# Building the APK

本專案已設定自動化雲端編譯，推薦使用 **GitHub Actions** 進行編譯，無需在本機安裝 Java 或 Android SDK。

## 🚀 推薦方法：GitHub Actions (雲端編譯)

1. **推送代碼**：
   將您的變更 `git push` 到 GitHub 的 `main` 或 `dev` 分支。
2. **自動編譯**：
   前往 GitHub 儲存庫頁面的 **"Actions"** 標籤頁。
3. **下載 APK**：
   - 點擊正在執行或已完成的 **"Build Android APK"** 工作。
   - 在頁面最下方的 **"Artifacts"** 區域，點擊 **"app-debug"** 下載壓縮檔。
   - 解壓縮後即可獲得 `app-debug.apk`。

---

## 🛠️ 本地開發 (進階)

如果您仍想在本機進行開發或除錯：

### 準備環境
- 安裝 Node.js
- 安裝 JDK 17 (並設定 `JAVA_HOME`)
- 安裝 Android Studio (內建 Android SDK)

### 同步變更
當您修改 `www/` 內容後，需同步至原生專案：
```bash
npx cap sync android
```

### 本地編譯
```bash
cd android
./gradlew assembleDebug
```
編譯產物位於：`android/app/build/outputs/apk/debug/app-debug.apk`

---

## 📁 目錄說明
- `www/`: 網頁原始碼與題庫資料（主要編輯區）。
- `android/`: Capacitor 生成的 Android 原生專案。
- `.github/workflows/`: 雲端自動化編譯設定檔。