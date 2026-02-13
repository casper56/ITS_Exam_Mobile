# -*- coding: utf-8 -*-
import json
import os

path = 'www/ITS_Python/questions_ITS_python.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q['id'] == 82:
        q['question'] = '82. 【CH08-1】針對下列有關 Python 例外處理 (try-except-finally) 的語法敘述，如果是正確的就選擇 <b>Yes</b>，否則請選擇 <b>No</b>：<br><br>● <b>選項 1</b>：在 try 語法中可以有不只一個 except 子句。<br>● <b>選項 2</b>：在 try 語法中可以不加 except 子句 (需配合 finally)。<br>● <b>選項 3</b>：在 try 語法中可以有一個 finally 子句與 except 子句。<br>● <b>選項 4</b>：在 try 語法中可以有不只一個 finally 子句。<pre><code class="language-python">'
        q['options'] = [
            '選項 1|Yes|No',
            '選項 2|Yes|No',
            '選項 3|Yes|No',
            '選項 4|Yes|No'
        ]
        q['answer'] = [1, 1, 1, 2]
        break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('ID 82 fixed successfully.')
