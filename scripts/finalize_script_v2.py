import os
import re

file_path = 'final_clean_repair.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 使用 String.fromCharCode(10) 徹底避開 Python 的 
 轉義地獄
# 使用 split/join 避開 正則表達式衝突
super_stable_js = r"""    function processContent(content, item) {
        if (!content) return '';
        var lines = Array.isArray(content) ? content : [String(content)];
        var nl = String.fromCharCode(10);
        var text = lines.join(nl);
        var result = text;
        for (var i = 1; i <= 5; i++) {
            var tag = '[[image0' + i + ']]';
            var src = item['image0' + i];
            if (src && result.indexOf(tag) !== -1) {
                var breakout = '</code></pre><img src="' + src + '" class="q-img"><pre><code class="language-python">';
                result = result.split(tag).join(breakout);
            }
        }
        return result;
    }"""

# 替換腳本中的所有 processContent 函式
content = re.sub(r'function processContent\(content, item\) \{.*?\}', super_stable_js, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully applied SUPER STABLE logic to final_clean_repair.py")
