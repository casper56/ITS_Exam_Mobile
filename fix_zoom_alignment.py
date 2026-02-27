import re

file_path = 'www/ITS_Python/ITS_Python.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 移除 CSS 動畫延遲，確保縮放座標計算精準 (移除 transition)
content = content.replace('transition: transform 0.1s ease-out;', 'transition: none !important;')
content = content.replace('transition: all 0.2s;', 'transition: none !important;')

# 2. 優化 drawLines 邏輯與 changeZoom 呼叫
js_fix = """
    window.changeZoom = function(delta) {
        window.globalZoom = (Math.round((window.globalZoom + delta) * 10) / 10);
        if (window.globalZoom < 0.7) window.globalZoom = 0.7;
        if (window.globalZoom > 2.0) window.globalZoom = 2.0;
        const container = document.getElementById('question-container');
        if (container) {
            container.style.transform = `scale(${window.globalZoom})`;
            container.style.transformOrigin = 'top center';
            if (window.globalZoom > 1) container.style.marginBottom = ((window.globalZoom - 1) * 80) + "%";
            else container.style.marginBottom = "0";
            // 縮放後立即重繪
            if (window.drawLines) window.drawLines();
        }
    };

    window.drawLines = function() {
        const svg = document.getElementById('matching-svg');
        const wrapper = document.getElementById('matching-wrapper');
        if (!svg || !wrapper) return;
        
        const zoom = window.globalZoom || 1.0;
        const rect = wrapper.getBoundingClientRect();
        
        // 設定畫布大小 (原始尺寸)
        svg.setAttribute('width', rect.width / zoom);
        svg.setAttribute('height', rect.height / zoom);
        svg.innerHTML = '';

        const currentAns = userAnswers[currentIndex];
        if (!currentAns) return;
        
        currentAns.forEach((rIdx, lIdx) => {
            if (rIdx === null) return;
            const dotL = document.getElementById(`dot-left-${lIdx}`);
            const dotR = document.getElementById(`dot-right-${rIdx}`);
            if (dotL && dotR) {
                const rectL = dotL.getBoundingClientRect();
                const rectR = dotR.getBoundingClientRect();
                
                // 計算相對於 wrapper 的原始座標 (排除 zoom 影響)
                const x1 = (rectL.left + rectL.width/2 - rect.left) / zoom;
                const y1 = (rectL.top + rectL.height/2 - rect.top) / zoom;
                const x2 = (rectR.left + rectR.width/2 - rect.left) / zoom;
                const y2 = (rectR.top + rectR.height/2 - rect.top) / zoom;

                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute('x1', x1); line.setAttribute('y1', y1);
                line.setAttribute('x2', x2); line.setAttribute('y2', y2);
                line.setAttribute('stroke', '#0d6efd');
                line.setAttribute('stroke-width', '2.5');
                svg.appendChild(line);
            }
        });
    };
"""

# 替換舊的變數與函式區塊
content = re.sub(r'window\.globalZoom = 1\.0;.*?window\.changeZoom = function\(delta\) \{.*?\}\s*;', '', content, flags=re.DOTALL)
content = re.sub(r'window\.drawLines = function\(\) \{.*?\}\s*;', js_fix, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Zoom alignment fix applied.")
