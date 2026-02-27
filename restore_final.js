const fs = require('fs');
const htmlPath = 'www/ITS_Python/ITS_Python.html';
const logicPath = 'logic.js';

if (fs.existsSync(htmlPath) && fs.existsSync(logicPath)) {
    const logicCode = fs.readFileSync(logicPath, 'utf-8');
    let htmlContent = fs.readFileSync(htmlPath, 'utf-8');
    
    const startTag = '<script>';
    const endTag = '</script>';
    const s = htmlContent.lastIndexOf(startTag);
    const e = htmlContent.lastIndexOf(endTag);
    
    if (s !== -1 && e !== -1) {
        const newHtml = htmlContent.substring(0, s + startTag.length) + 
                        logicCode + 
                        htmlContent.substring(e);
        fs.writeFileSync(htmlPath, newHtml, 'utf-8');
        console.log('SUCCESS: JS logic fully restored.');
    }
}
