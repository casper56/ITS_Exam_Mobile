const fs = require('fs');

const jsonPath = 'www/ITS_Python/questions_ITS_python.json';
const htmlPath = 'www/ITS_Python/ITS_Python.html';

if (fs.existsSync(jsonPath) && fs.existsSync(htmlPath)) {
    const processedJson = fs.readFileSync(jsonPath, 'utf-8');
    let htmlContent = fs.readFileSync(htmlPath, 'utf-8');
    
    // 尋找 quizData 的範圍
    // 這裡使用更強健的尋找方式
    const startMarker = 'const quizData = [';
    const endMarker = '];';
    
    const startIndex = htmlContent.indexOf(startMarker);
    const endIndex = htmlContent.indexOf(endMarker, startIndex);
    
    if (startIndex !== -1 && endIndex !== -1) {
        // 替換整塊內容
        const newHtmlContent = htmlContent.substring(0, startIndex + 'const quizData = '.length) + 
                               processedJson + 
                               htmlContent.substring(endIndex + endMarker.length - 1);
        
        fs.writeFileSync(htmlPath, newHtmlContent, 'utf-8');
        console.log('SUCCESS: HTML quizData synced with JSON.');
    } else {
        console.log('ERROR: Could not find quizData section in HTML.');
    }
}
