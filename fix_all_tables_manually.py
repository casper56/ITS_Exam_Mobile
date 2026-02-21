import json
import re

# 從最原始備份讀取
with open('backups/CLEAN_ORIGINAL_PYTHON.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_table(html):
    html = re.sub(r'<table[^>]*>', '<table class="q-table w-100 t-left"><thead>', html)
    if '</th></tr>' in html:
        html = html.replace('</th></tr>', '</th></tr></thead><tbody>', 1)
    if '</table>' in html:
        html = html.replace('</table>', '</tbody></table>')
    return html

def code_block(text):
    return f'<pre><code class="language-python">{text.strip()}</code></pre>'

for q in data:
    qid = q['id']
    if qid == 9:
        q['explanation'] = [
            "<b>⭐ 運算順序拆解：</b>",
            code_block(r'''1. a % b (24 % 7) = 3
2. 3 * 100 = 300
3. 2.0 ** 3.0 = 8.0
4. 300 // 8.0 = 37.0 (註：地板除法結果為 float)
5. 37.0 - 7 = 30.0'''),
            "<b>⭐ 補充：負數的地板除法與取餘數規則</b>",
            clean_table(r'''<table border='1'><tr><th>運算子</th><th>規則</th><th>正數範例</th><th>負數範例</th></tr><tr><td><b>地板除 //</b></td><td>向左取整</td><td>7 // 2 = 3</td><td>-7 // 2 = -4</td></tr><tr><td><b>取餘數 %</b></td><td>r = a - (b * (a // b))</td><td>7 % 3 = 1</td><td>-7 % 3 = 2</td></tr></table>'''),
            "<b>💡 記住：</b>負數除法時，// 會向負無窮大方向靠攏（-3.5 變成 -4）。"
        ]
    elif qid == 101:
        q['explanation'] = [
            code_block(r'''● random.sample(population, k) -> 「不重覆」抽樣
● random.choices(population, k=N) -> 「可重覆」抽樣'''),
            "<b>⭐ 常用隨機方法功能比較表：</b>",
            clean_table(r'''<table border='1'><tr><th>方法 (Method)</th><th>功能</th><th>語法範例</th><th>參數 k</th><th>特點</th></tr><tr><td><b>sample</b></td><td>抽樣</td><td>sample(seq, 3)</td><td>k=3 (必填)</td><td>不重覆</td></tr><tr><td><b>choices</b></td><td>抽樣</td><td>choices(seq, k=3)</td><td>k=3 (選填)</td><td>可重覆</td></tr><tr><td><b>choice</b></td><td>隨機挑一</td><td>choice(seq)</td><td>不支援</td><td>單次不可重覆</td></tr></table>''')
        ]
    elif qid == 102:
        q['explanation'] = [
            code_block(r'''● random.choices：支援 weights 參數。
● random.sample：不支援 weights 參數。'''),
            "<b>⭐ 選項解析與錯誤原因：</b>",
            clean_table(r'''<table border='1'><tr><th>序號</th><th>語法範例</th><th>結果與錯誤說明</th></tr><tr><td>1 (正確)</td><td>choices(..., weights=[...], k=5)</td><td>成功依權重抽取 5 次</td></tr><tr><td>2</td><td>sample(..., weights=...)</td><td>引發 TypeError</td></tr><tr><td>3</td><td>choices(..., k=5)</td><td>機率均等 (各 33.3%)</td></tr><tr><td>4</td><td>sample(..., 5)</td><td>引發 ValueError (樣本不足)</td></tr></table>''')
        ]
    elif qid == 106:
        q['explanation'] = [
            code_block(r'''● assertTrue(x)：驗證 x 是否為 True。
● assertIs(x, True)：驗證 x 是否「就是」True 物件。'''),
            "<b>⭐ unittest 正確斷言對照表：</b>",
            clean_table(r'''<table border='1'><tr><th>驗證目標</th><th>錯誤用法</th><th>正確用法</th></tr><tr><td>判斷為 True</td><td>assertIsTrue</td><td><b>assertTrue</b></td></tr><tr><td>判斷為 False</td><td>assertIsFalse</td><td><b>assertFalse</b></td></tr></table>''')
        ]
    elif qid == 108:
        q['explanation'] = [
            "<b>⭐ unittest 常用斷言方法比較表：</b>",
            clean_table(r'''<table border='1'><tr><th>方法 (Method)</th><th>對應語法</th><th>說明</th></tr><tr><td>assertEqual(a, b)</td><td>a == b</td><td>內容相等</td></tr><tr><td>assertIs(a, b)</td><td>a is b</td><td>同一物件</td></tr><tr><td>assertIn(a, b)</td><td>a in b</td><td>包含於容器中</td></tr><tr><td>assertIsInstance(a, b)</td><td>isinstance(a, b)</td><td>類型檢查</td></tr></table>''')
        ]
    elif qid == 110:
        q['explanation'] = [
            "<b>⭐ 1. 容器類型定義語法對照表：</b>",
            clean_table(r'''<table border='1'><tr><th>型別</th><th>符號</th><th>範例</th></tr><tr><td>List</td><td>[]</td><td>[1, 2]</td></tr><tr><td>Tuple</td><td>()</td><td>(1, 2)</td></tr><tr><td>Dict</td><td>{}</td><td>{'k': 'v'}</td></tr><tr><td>Set</td><td>{}</td><td>{1, 2}</td></tr></table>'''),
            "<b>⭐ 2. 集合運算符號表：</b>",
            clean_table(r'''<table border='1'><tr><th>運算</th><th>符號</th><th>功能</th></tr><tr><td>交集</td><td>&</td><td>AND (兩者皆有)</td></tr><tr><td>聯集</td><td>|</td><td>OR (合併)</td></tr><tr><td>差集</td><td>-</td><td>移除 (A有B沒有)</td></tr></table>''')
        ]
    elif qid == 112:
        q['explanation'] = [
            "<b>⭐ 容器新增/修改方法比較表：</b>",
            clean_table(r'''<table border='1'><tr><th>型別</th><th>主要方法</th><th>說明</th></tr><tr><td>List</td><td>append, insert</td><td>有序、可修改</td></tr><tr><td>Set</td><td>add</td><td>無序、不重覆</td></tr><tr><td>Dict</td><td>d[key] = val</td><td>鍵值對</td></tr><tr><td>Tuple</td><td>不支援</td><td>不可修改</td></tr></table>''')
        ]
    elif qid == 115:
        q['explanation'] = [
            "<b>⭐ 程式執行步驟拆解表：</b>",
            clean_table(r'''<table border='1'><tr><th>步驟</th><th>數據變化</th><th>說明</th></tr><tr><td>nums = [1, 2, 2, 3]</td><td>[1, 2, 2, 3]</td><td>初始列表</td></tr><tr><td>set(nums)</td><td>{1, 2, 3}</td><td>轉集合 (去重)</td></tr><tr><td>list(...)</td><td>[1, 2, 3]</td><td>轉回列表</td></tr><tr><td>append(4)</td><td>[1, 2, 3, 4]</td><td>新增元素</td></tr></table>''')
        ]
    elif qid == 116:
        q['explanation'] = [
            "<b>⭐ 集合運算 (Intersection) 說明：</b>",
            clean_table(r'''<table border='1'><tr><th>符號</th><th>名稱</th><th>結果</th></tr><tr><td>&</td><td>交集</td><td>{3, 4} (重疊部分)</td></tr></table>''')
        ]
    elif qid == 117:
        q['explanation'] = [
            "<b>⭐ Dictionary 取值方式對照表：</b>",
            clean_table(r'''<table border='1'><tr><th>方式</th><th>範例</th><th>結果</th></tr><tr><td>Key 取值</td><td>data['b']</td><td>20 (正確)</td></tr><tr><td>Index 取值</td><td>data[1]</td><td>KeyError</td></tr><tr><td>屬性取值</td><td>data.b</td><td>AttributeError</td></tr></table>''')
        ]
    elif qid == 120:
        q['explanation'] = [
            "<b>⭐ 數據型別與修改方法合法性檢查：</b>",
            clean_table(r'''<table border='1'><tr><th>型別</th><th>方法</th><th>結果</th></tr><tr><td>List</td><td>append</td><td>合法</td></tr><tr><td>Set</td><td>add</td><td>合法</td></tr><tr><td>Tuple</td><td>append</td><td>錯誤 (AttributeError)</td></tr></table>''')
        ]
    elif qid == 124:
        q['explanation'] = [
            "<b>⭐ 檔案與目錄刪除指令對照表：</b>",
            clean_table(r'''<table border='1'><tr><th>目標</th><th>os / shutil</th><th>pathlib</th></tr><tr><td>刪除檔案</td><td>os.remove()</td><td>Path.unlink()</td></tr><tr><td>刪除空目錄</td><td>os.rmdir()</td><td>Path.rmdir()</td></tr><tr><td>刪除整棵樹</td><td>shutil.rmtree()</td><td>不可直接刪除</td></tr></table>''')
        ]
    elif qid == 132:
        q['explanation'] = [
            "<b>⭐ random 模組常用函式比較表：</b>",
            clean_table(r'''<table border='1'><tr><th>函式</th><th>型別</th><th>範圍</th></tr><tr><td>random()</td><td>Float</td><td>[0.0, 1.0)</td></tr><tr><td>randint(a, b)</td><td>Int</td><td>[a, b] (包含b)</td></tr><tr><td>randrange(a, b)</td><td>Int</td><td>[a, b) (不含b)</td></tr><tr><td>uniform(a, b)</td><td>Float</td><td>[a, b]</td></tr></table>''')
        ]

with open('www/ITS_Python/questions_ITS_python.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("13 題表格解析已全部完成手動精構！")
