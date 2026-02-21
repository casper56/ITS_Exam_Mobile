import json
import re

# 從剛才備份的最乾淨檔案讀取
with open('backups/questions_ITS_softdevelop_pre_fix.json.bak', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_table(html):
    html = re.sub(r'<table[^>]*>', '<table class="q-table w-100 t-left"><thead>', html)
    if '</th></tr>' in html:
        html = html.replace('</th></tr>', '</th></tr></thead><tbody>', 1)
    if '</table>' in html:
        html = html.replace('</table>', '</tbody></table>')
    return html

def code_block(text, lang="csharp"):
    return f'<pre><code class="language-{lang}">{text.strip()}</code></pre>'

for q in data:
    qid = q['id']
    if qid == 10:
        q['explanation'] = [
            "<b>⭐ 核心概念：抽象類別與繼承</b>",
            "題目要求建立一個<b>無法直接實例化</b> (instantiate)，但必須由<b>衍生類別實作方法</b>的類型。",
            "<b>修飾詞功能對照：</b>",
            clean_table(r'''<table border='1'><tr><th>修飾詞</th><th>實例化 (New)</th><th>是否繼承</th><th>主要用途</th></tr><tr><td><b>abstract</b></td><td>❌ 禁止</td><td>✅ 必須</td><td><b>定義樣版</b>，強制子類別實作。</td></tr><tr><td><b>protected</b></td><td>視建構子而定</td><td>✅ 可以</td><td><b>限制存取</b>，僅限類別內部與子類別。</td></tr><tr><td><b>sealed</b></td><td>✅ 可以</td><td>❌ 禁止</td><td><b>封印類別</b>，防止方法被覆寫或繼承。</td></tr><tr><td><b>public</b></td><td>✅ 可以</td><td>✅ 可以</td><td><b>完全公開</b>，任何地方皆可存取。</td></tr></table>'''),
            "<b>選項解析：</b>",
            code_block(r'''A. abstract (正確) -> 符合無法實例化且供繼承實作的要求。
B. protected -> 成員存取修飾詞，不代表類別無法實例化。
C. sealed -> 防止繼承，與題目要求相反。
D. public -> 任何人皆可存作，無法限制繼承行為。''')
        ]
    elif qid == 14:
        q['explanation'] = [
            "<b>⭐ 存取修飾詞存取權限比較：</b>",
            clean_table(r'''<table border='1'><tr><th>修飾詞</th><th>類別內部</th><th>衍生類別(繼承)</th><th>外部專案</th></tr><tr><td>private</td><td>✅</td><td>❌</td><td>❌</td></tr><tr><td><b>protected</b></td><td>✅</td><td><b>✅</b></td><td>❌</td></tr><tr><td>internal</td><td>✅</td><td>✅ (限同專案)</td><td>❌</td></tr><tr><td>public</td><td>✅</td><td>✅</td><td>✅</td></tr></table>'''),
            "<b>選項解析：</b>",
            code_block(r'''A. internal -> 限定在同一個編譯組件 (DLL/EXE) 內存取。
B. private -> 最嚴格，僅限類別內部存取。
C. protected (正確) -> 允許衍生類別存取，但對外部隱藏。
D. public -> 最寬鬆，對外完全開放。''')
        ]
    elif qid == 15:
        q['explanation'] = [
            "<b>⭐ Boxing (裝箱) 與 Unboxing (拆箱) 概念：</b>",
            "當我們將<b>值型別</b> (如 int) 轉換為 <b>object</b> 型別時，這個過程稱為 <b>Boxing</b>。",
            "<b>特性對照：</b>",
            clean_table(r'''<table border='1'><tr><th>術語</th><th>轉換方向</th><th>數據存儲位置</th><th>效能影響</th></tr><tr><td><b>Boxing (裝箱)</b></td><td>值型別 -> 參考型別</td><td>Stack 移至 Heap</td><td>較大 (需分配記憶體)</td></tr><tr><td><b>Unboxing (拆箱)</b></td><td>參考型別 -> 值型別</td><td>Heap 移至 Stack</td><td>較小</td></tr></table>'''),
            "<b>選項解析：</b>",
            code_block(r'''A. Boxing (正確) -> 將值型別物件化。
B. Unboxing -> 將物件還原為原始數值。
C. 介面 (Interface) -> 定義契約，與型別轉換無關。
D. 映射 (Mapping) -> 通常指數據欄位對應。''')
        ]
    elif qid == 16:
        q['explanation'] = [
            "<b>⭐ C# 屬性存取子 (Accessors) 功能：</b>",
            clean_table(r'''<table border='1'><tr><th>關鍵字</th><th>正式名稱</th><th>功能與權限</th></tr><tr><td><b>get</b></td><td>取得器 (Getter)</td><td>讀取屬性值 (唯讀屬性)。</td></tr><tr><td><b>set</b></td><td>設定器 (Setter)</td><td><b>寫入或修改</b>屬性值 (可寫屬性)。</td></tr><tr><td><b>value</b></td><td>預設參數</td><td>代表外部傳入要寫入的新值。</td></tr></table>'''),
            "<b>語法範例：</b>",
            code_block(r'''public int Score {
    get { return _score; }
    set { _score = value; } // 使用 set 來允許外部修改
}''')
        ]
    elif qid == 17:
        q['explanation'] = [
            "<b>⭐ 繼承關係：基底類別 vs 衍生類別</b>",
            clean_table(r'''<table border='1'><tr><th>類別類型</th><th>角色定義</th><th>繼承特性</th></tr><tr><td><b>基底類別 (Base)</b></td><td>父類別 / 模板</td><td>提供通用功能供子類別繼承。</td></tr><tr><td><b>衍生類別 (Derived)</b></td><td>子類別 / 擴充</td><td><b>繼承並擴充</b>父類別功能的類型。</td></tr></table>'''),
            "<b>解析：</b>",
            "題目描述「繼承了另一個類別的所有功能」，這就是 <b>衍生類別 (Derived Class)</b> 的定義。"
        ]
    elif qid == 18:
        q['explanation'] = [
            "<b>⭐ Protected (受保護) 的繼承路徑：</b>",
            "在多層繼承中，<code>protected</code> 成員會順著繼承鏈向下傳遞，只要是衍生類別都能存取。",
            "<b>繼承結構：</b>",
            code_block(r'''A (m1) <- B (m2) <- C (m3)
               <- D (m4)'''),
            "<b>存取權限分析：</b>",
            clean_table(r'''<table border='1'><tr><th>成員來源</th><th>成員名稱</th><th>C 類別是否可存取</th><th>說明</th></tr><tr><td>A 類別</td><td>m1</td><td>✅ 可以</td><td>C 是 A 的子類的子類。</td></tr><tr><td>B 類別</td><td>m2</td><td>✅ 可以</td><td>C 是 B 的直接子類。</td></tr><tr><td>C 類別</td><td>m3</td><td>✅ 可以</td><td>C 類別自己的成員。</td></tr><tr><td>D 類別</td><td>m4</td><td>❌ 禁止</td><td>C 與 D 是平級，無法互相讀取。</td></tr></table>''')
        ]
    elif qid == 19:
        q['explanation'] = [
            "<b>⭐ Upcasting (向上轉型) 概念：</b>",
            "將子類別（較具體）轉型為父類別（較通用）的過程，稱為向上轉型。",
            "<b>特性比較：</b>",
            clean_table(r'''<table border='1'><tr><th>轉型方式</th><th>方向</th><th>隱式轉換</th><th>安全性</th></tr><tr><td><b>向上轉型 (Up)</b></td><td>子類 -> 父類</td><td>✅ 自動</td><td>百分之百安全</td></tr><tr><td><b>向下轉型 (Down)</b></td><td>父類 -> 子類</td><td>❌ 需強制轉型</td><td>有失敗風險</td></tr></table>'''),
            "<b>解析：</b>",
            "將 PictureCanvas 視為較通用的 Canvas 處理，就是 <b>向上轉型 (Upcasting)</b>。"
        ]
    elif qid == 20:
        q['explanation'] = [
            "<b>⭐ Override (覆寫) 的必要條件：</b>",
            "若要在子類別中覆寫父類別的方法，該方法必須在存取權限上允許存取，且具備 <code>virtual</code> 關鍵字。",
            "<b>條件對照表：</b>",
            clean_table(r'''<table border='1'><tr><th>宣告方式</th><th>可否覆寫</th><th>原因說明</th></tr><tr><td>static</td><td>❌</td><td>靜態方法屬於類別，不屬於物件。</td></tr><tr><td>private virtual</td><td>❌</td><td>子類別根本看不到 private 方法。</td></tr><tr><td><b>protected virtual</b></td><td>✅</td><td><b>子類別可見且允許擴充。</b></td></tr><tr><td>Non-virtual</td><td>❌</td><td>基底類別未宣告允許覆寫。</td></tr></table>''')
        ]
    elif qid == 22:
        q['explanation'] = [
            "<b>⭐ 顯式介面實作與方法覆寫：</b>",
            "題目考點在於如何同時處理「類別繼承的覆寫」與「介面顯式實作」。",
            "<b>實作細節對照：</b>",
            clean_table(r'''<table border='1'><tr><th>實作方式</th><th>技術名稱</th><th>存取與行為</th></tr><tr><td>override Display()</td><td>方法覆寫</td><td>取代父類別行為。</td></tr><tr><td>DisplayRaw()</td><td>一般方法</td><td>類別專屬新功能。</td></tr><tr><td>IDisplayResult.Display()</td><td>顯式介面實作</td><td><b>必須轉型為介面</b>才能呼叫。</td></tr></table>'''),
            "<b>執行結果解析：</b>",
            code_block(r'''r1.Display() -> 執行 override -> 99
r2.Display() -> 執行介面實作 -> 99 seconds
r1.DisplayRaw() -> 執行新方法 -> 1.65 minutes''')
        ]

with open('www/ITS_softdevelop/questions_ITS_softdevelop.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ITS_softdevelop 表格修正成功！")
