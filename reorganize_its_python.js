const fs = require('fs');

function cleanQuestionText(text) {
    if (typeof text !== 'string') return text;
    // 移除開頭題號模式:
    // 1. "48. " 或 "48.【...】"
    // 2. "<pre><code class="...">48. "
    // 3. "<pre><code>48. "
    
    // 處理 HTML 標籤包裹的情況
    let cleaned = text.replace(/^(<pre[^>]*><code[^>]*>)\d+[\.．\s]*/i, '$1');
    cleaned = cleaned.replace(/^(<pre[^>]*>)\d+[\.．\s]*/i, '$1');
    // 處理純文字情況
    cleaned = cleaned.replace(/^\d+[\.．\s]*/, '');
    
    return cleaned;
}

function processData(data) {
    return data.map((item, index) => {
        const newItem = { ...item };
        newItem.id = index + 1; // 重新編號
        
        if (Array.isArray(newItem.question)) {
            newItem.question = newItem.question.map(q => cleanQuestionText(q));
        } else if (typeof newItem.question === 'string') {
            newItem.question = cleanQuestionText(newItem.question);
        }
        
        return newItem;
    });
}

// 1. 處理 JSON 檔案
const jsonPath = 'www/ITS_Python/questions_ITS_python.json';
if (fs.existsSync(jsonPath)) {
    const rawJson = fs.readFileSync(jsonPath, 'utf-8');
    const data = JSON.parse(rawJson);
    const processedData = processData(data);
    fs.writeFileSync(jsonPath, JSON.stringify(processedData, null, 4), 'utf-8');
    console.log('JSON: Re-indexed and cleaned.');
}

// 2. 處理 HTML 檔案 (quizData 區域)
const htmlPath = 'www/ITS_Python/ITS_Python.html';
if (fs.existsSync(htmlPath)) {
    let content = fs.readFileSync(htmlPath, 'utf-8');
    const startMarker = 'const quizData = [';
    const endMarker = '];';
    
    const startIndex = content.indexOf(startMarker);
    const endIndex = content.indexOf(endMarker, startIndex);
    
    if (startIndex !== -1 && endIndex !== -1) {
        const rawDataSection = content.substring(startIndex + startMarker.length - 1, endIndex + 1);
        try {
            // 注意: 這裡用 eval 是因為 quizData 在 JS 裡可能不是標準 JSON 格式
            const data = eval(rawDataSection);
            const processedData = processData(data);
            const newDataSection = JSON.stringify(processedData, null, 4);
            
            const newContent = content.substring(0, startIndex + startMarker.length - 1) + 
                               newDataSection + 
                               content.substring(endIndex + 1);
            
            fs.writeFileSync(htmlPath, newContent, 'utf-8');
            console.log('HTML: Re-indexed and cleaned.');
        } catch (e) {
            console.log('HTML: Error processing quizData section - ' + e.message);
        }
    }
}
