const fs = require('fs');

const q26 = {
    "id": 26,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">【CH03-5】你有以下清單結構：alph = "abcdefghijklmnopqrstuvwxyz"
以下各個程式碼片段的結果各是如何？
請將右側的執行結果拖拉或點選至左側對應的程式碼中：</code></pre>"
    ],
    "left": [
        "(1) alph[3:15]",
        "(2) alph[3:15:3]",
        "(3) alph[15:3:-3]",
        "(4) alph[::-3]"
    ],
    "right": [
        "A. zwtqnkheb",
        "B. pmjg",
        "C. defghijklmno",
        "D. ponmlkjihgfe",
        "E. defghijklmnop",
        "F. dgjm",
        "G. olif"
    ],
    "answer": [2, 5, 1, 0],
    "weight": 1,
    "image": null,
    "explanation": [
        "<pre><code class="language-python">● alph[3:15] -> 從索引 3 到 14 (d...o)，結果為 C (defghijklmno)
● alph[3:15:3] -> 從索引 3 開始每隔 3 格取一字 (d, g, j, m)，結果為 F (dgjm)
● alph[15:3:-3] -> 從索引 15 (p) 倒退回 3，每隔 3 格取一字 (p, m, j, g)，結果為 B (pmjg)
● alph[::-3] -> 全字串倒退，從最後一字 (z) 開始每隔 3 格取一字，結果為 A (zwtqnkheb)</code></pre>"
    ],
    "category": "D1_資料型別與運算子"
};

const q48 = {
    "id": 48,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">【CH05-6】你設計一個 Python 程式來檢查使用者輸入的數字是 1 位數、 2 位數還是 2 位數以上。
請將正確的 Python 條件判斷式配對到對應的邏輯描述中：</code></pre>"
    ],
    "left": [
        "(1) 判斷是否為 1 位數 ( < 10 )",
        "(2) 判斷是否為 2 位數 ( 10 ~ 99 )",
        "(3) 判斷是否為 2 位數以上 ( >= 100 )"
    ],
    "right": [
        "A. if num < 10:",
        "B. if num < 100:",
        "C. elif num < 100:",
        "D. else:"
    ],
    "answer": [0, 2, 3],
    "weight": 1,
    "image": null,
    "explanation": [
        "<pre><code class="language-python">● 第一步使用 if num < 10: 判斷 1 位數。
● 第二步使用 elif num < 100: 判斷 2 位數 (此時已排除 < 10 的情況)。
● 最後使用 else: 處理所有剩餘情況 (即 100 以上)。</code></pre>"
    ],
    "category": "D2_流程控制與判斷"
};

function patchFile(filePath) {
    if (!fs.existsSync(filePath)) return;
    let content = fs.readFileSync(filePath, 'utf-8');
    
    // 替換 ID 26
    const pattern26 = /\{\s*"id": 26,[\s\S]*?\}(,)?/g;
    content = content.replace(pattern26, (match, comma) => {
        return JSON.stringify(q26, null, 4) + (comma || "");
    });

    // 替換 ID 48
    const pattern48 = /\{\s*"id": 48,[\s\S]*?\}(,)?/g;
    content = content.replace(pattern48, (match, comma) => {
        return JSON.stringify(q48, null, 4) + (comma || "");
    });

    fs.writeFileSync(filePath, content, 'utf-8');
    console.log(`SUCCESS: Patched ${filePath}`);
}

patchFile('www/ITS_Python/questions_ITS_python.json');
patchFile('www/ITS_Python/ITS_Python.html');
patchFile('www/ITS_Python/mock_v34.html');
