const fs = require('fs');

const q48 = {
    "id": 48,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">48. 【CH05-6】你設計一個 Python 程式來檢查使用者輸入的數字是 1 位數、 2 位數還是 2 位數以上。
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

const q49 = {
    "id": 49,
    "type": "matching",
    "question": [
        "<pre><code class="language-python">49. 【CH05-7】你在設計一個 Python 程式遊戲，讓參加的人從 1 到 100 之間猜一個數字，最多有三次機會。
請將正確的程式碼片段配對到對應的遊戲邏輯中：</code></pre>"
    ],
    "left": [
        "(1) 設定重複執行次數 (最多 3 次)",
        "(2) 當猜對時，立即跳出迴圈",
        "(3) 每次猜錯後，將次數加 1"
    ],
    "right": [
        "A. while chance <= 3:",
        "B. break",
        "C. pass",
        "D. chance += 1",
        "E. while chance < 3:",
        "F. chance = 2"
    ],
    "answer": [0, 1, 3],
    "weight": 1,
    "image": null,
    "explanation": [
        "<pre><code class="language-python">● 使用 while chance <= 3: 可確保程式執行 3 次 (1, 2, 3)。
● 當猜中數字時，使用 break 立即結束 while 迴圈。
● 每次迴圈結尾執行 chance += 1 紀錄進度。</code></pre>"
    ],
    "category": "D2_流程控制與判斷"
};

function patchFile(filePath) {
    if (!fs.existsSync(filePath)) return;
    let content = fs.readFileSync(filePath, 'utf-8');
    
    // 替換 ID 48
    const pattern48 = /\{\s*"id": 48,[\s\S]*?\}(,)?/g;
    content = content.replace(pattern48, (match, comma) => {
        return JSON.stringify(q48, null, 4) + (comma || "");
    });

    // 替換 ID 49
    const pattern49 = /\{\s*"id": 49,[\s\S]*?\}(,)?/g;
    content = content.replace(pattern49, (match, comma) => {
        return JSON.stringify(q49, null, 4) + (comma || "");
    });

    fs.writeFileSync(filePath, content, 'utf-8');
    console.log(`Patched ${filePath}`);
}

patchFile('www/ITS_Python/questions_ITS_python.json');
patchFile('www/ITS_Python/ITS_Python.html');
patchFile('www/ITS_Python/mock_v34.html');
