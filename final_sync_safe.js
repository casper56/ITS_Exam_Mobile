const fs = require('fs');

const jsonPath = 'www/ITS_Python/questions_ITS_python.json';
const htmlPath = 'www/ITS_Python/ITS_Python.html';

if (fs.existsSync(jsonPath) && fs.existsSync(htmlPath)) {
    const data = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
    let html = fs.readFileSync(htmlPath, 'utf-8');
    
    const startTag = 'const quizData = [';
    const endTag = '];';
    const s = html.indexOf(startTag);
    const e = html.indexOf(endTag, s);
    
    if (s !== -1 && e !== -1) {
        const newHtml = html.substring(0, s + 'const quizData = '.length) + 
                        JSON.stringify(data, null, 4) + 
                        html.substring(e + 1);
        fs.writeFileSync(htmlPath, newHtml, 'utf-8');
        console.log('SUCCESS: HTML Synced from JSON.');
    }
}
