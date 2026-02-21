import os
import re

file_path = 'final_clean_repair.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

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

content = re.sub(r'function processContent\(content, item\) \{.*?\}', super_stable_js, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Applied fix to generator script.")
