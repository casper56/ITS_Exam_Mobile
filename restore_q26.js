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

function patch(filePath) {
    if (!fs.existsSync(filePath)) return;
    let content = fs.readFileSync(filePath, 'utf-8');
    
    // 正則替換 ID 26
    const pattern = /\{\s*"id": 26,[\s\S]*?\}(,)?/g;
    content = content.replace(pattern, (match, comma) => {
        return JSON.stringify(q26, null, 4) + (comma || "");
    });
    
    fs.writeFileSync(filePath, content, 'utf-8');
    console.log(`SUCCESS: Patched ID 26 in ${filePath}`);
}

patch('www/ITS_Python/questions_ITS_python.json');
patch('www/ITS_Python/ITS_Python.html');
patch('www/ITS_Python/mock_v34.html');
