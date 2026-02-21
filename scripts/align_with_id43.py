import os
import re

file_path = 'final_clean_repair.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 採用 ID 43 的成功模式：徹底斷開標籤，讓圖片在 code 區塊外獨立
# 我們使用 Python 的 raw string 來避免轉義災難
safe_js_func = r"""    function processContent(content, item) {
        if (!content) return '';
        var lines = Array.isArray(content) ? content : [String(content)];
        var text = lines.join('
');
        var result = text;
        for (var i = 1; i <= 5; i++) {
            var tag = '[[image0' + i + ']]';
            var src = item['image0' + i];
            if (src && result.indexOf(tag) !== -1) {
                // 核心關鍵：閉合原本標籤 -> 插入圖片 -> 重新開啟標籤 (帶正確 class)
                var breakout = '</code></pre><img src="' + src + '" class="q-img"><pre><code class="language-python">';
                result = result.split(tag).join(breakout);
            }
        }
        return result;
    }"""

# 替換掉腳本中所有的 processContent 函式
content = re.sub(r'function processContent\(content, item\) \{.*?\}', safe_js_func, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully aligned processContent logic with ID 43 success pattern.")
