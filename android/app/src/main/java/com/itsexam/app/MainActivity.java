package com.itsexam.app;

import com.getcapacitor.BridgeActivity;
import android.webkit.WebSettings;
import android.webkit.WebView;

public class MainActivity extends BridgeActivity {
    @Override
    public void onStart() {
        super.onStart();
        WebView webView = this.getBridge().getWebView();
        WebSettings settings = webView.getSettings();
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false); // 隱藏討厭的放大鏡按鈕圖示
        settings.setSupportZoom(true);
    }

}
