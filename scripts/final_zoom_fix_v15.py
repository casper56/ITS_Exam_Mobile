import glob
import os

def final_zoom_fix_v15():
    # 1. 修改所有 HTML 檔案中的按鈕縮放限制至 6px
    files = glob.glob('www/**/*.html', recursive=True)
    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: continue
        
        print(f"Lowering zoom limit in {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 將下限 8px 或 10px 降至 6px
        content = content.replace('if (_zoomLevel < 8) _zoomLevel = 8;', 'if (_zoomLevel < 6) _zoomLevel = 6;')
        content = content.replace('if (_zoomLevel < 10) _zoomLevel = 10;', 'if (_zoomLevel < 6) _zoomLevel = 6;')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # 2. 修改 MainActivity.java 以啟用原生雙指縮放
    java_path = 'android/app/src/main/java/com/itsexam/app/MainActivity.java'
    if os.path.exists(java_path):
        print(f"Enabling native zoom in {java_path}...")
        with open(java_path, 'r', encoding='utf-8') as f:
            java_content = f.read()
        
        # 檢查是否已經有自訂邏輯，如果沒有則注入
        if 'setBuiltInZoomControls' not in java_content:
            # 導入需要的類別
            if 'import android.webkit.WebSettings;' not in java_content:
                java_content = java_content.replace('import com.getcapacitor.BridgeActivity;', 
                                                   'import com.getcapacitor.BridgeActivity;\nimport android.webkit.WebSettings;\nimport android.webkit.WebView;')
            
            # 覆寫 onResume 或在 onCreate 之後設定 (Capacitor 推薦在初始化後設定)
            zoom_logic = """
    @Override
    public void onStart() {
        super.onStart();
        WebView webView = this.getBridge().getWebView();
        WebSettings settings = webView.getSettings();
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false); // 隱藏討厭的放大鏡按鈕圖示
        settings.setSupportZoom(true);
    }
"""
            # 在最後一個括號前注入
            last_bracket = java_content.rfind('}')
            java_content = java_content[:last_bracket] + zoom_logic + "\n" + java_content[last_bracket:]
            
            with open(java_path, 'w', encoding='utf-8') as f:
                f.write(java_content)

if __name__ == "__main__":
    final_zoom_fix_v15()
