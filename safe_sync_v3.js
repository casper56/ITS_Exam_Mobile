const fs = require('fs');

const jsonPath = 'www/ITS_Python/questions_ITS_python.json';
const htmlPath = 'www/ITS_Python/ITS_Python.html';

const jsonData = fs.readFileSync(jsonPath, 'utf-8');
let htmlContent = fs.readFileSync(htmlPath, 'utf-8');

// 尋找 quizData 的邊界
const startMarker = 'const quizData = [';
const endMarker = '];';

const startIndex = htmlContent.indexOf(startMarker);
const lastIndex = htmlContent.lastIndexOf(endMarker);

if (startIndex !== -1 && lastIndex !== -1) {
    // 關鍵：我們直接使用字串拼接，不解析 JSON，避免轉義問題
    const newHtml = htmlContent.substring(0, startIndex + 'const quizData = '.length - 1) + 
                    jsonData + 
                    htmlContent.substring(lastIndex + 1);
    
    fs.writeFileSync(htmlPath, newHtml, 'utf-8');
    console.log('SYNC SUCCESSFUL');
} else {
    console.log('ERROR: Markers not found. Start:', startIndex, 'End:', lastIndex);
}
