import os
import re

file_path = 'final_clean_repair.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修正 processContent 函式：改用 <br> 強制換行，並移除多餘反斜線
# 這裡採用更強大的正則替換，確保覆蓋模板中所有 processContent
stable_func = r"""    function processContent(content, item) {
        if (!content) return '';
        var lines = Array.isArray(content) ? content : [String(content)];
        // 使用 <br> 代替 
，保證在 HTML 任何地方都能絕對換行
        var text = lines.join('<br>');
        var result = text;
        for (var i = 1; i <= 5; i++) {
            var tag = '[[image0' + i + ']]';
            var src = item['image0' + i];
            if (src && result.indexOf(tag) !== -1) {
                var imgHtml = '</code></pre><img src="' + src + '" class="injected-q-img"><pre><code class="language-python">';
                result = result.split(tag).join(imgHtml);
            }
        }
        return result;
    }"""

content = re.sub(r'function processContent\(content, item\) \{.*?\}', stable_func, content, flags=re.DOTALL)

# 2. 補強 CSS，確保 code 標籤不會縮成一團
old_css = 'white-space: pre-wrap;'
new_css = 'white-space: pre-wrap !important; word-break: break-all !important;'
content = content.replace(old_css, new_css)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully applied ABSOLUTE NEWLINE fix to final_clean_repair.py")
