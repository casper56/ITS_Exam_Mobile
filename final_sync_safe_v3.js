const fs = require('fs');

const jsonPath = 'www/ITS_Python/questions_ITS_python.json';
const htmlPath = 'www/ITS_Python/ITS_Python.html';

const data = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
let html = fs.readFileSync(htmlPath, 'utf-8');

const startMarker = 'const quizData = [';
const endMarker = '];';

const startIndex = html.indexOf(startMarker);
const lastIndex = html.lastIndexOf(endMarker);

if (startIndex !== -1 && lastIndex !== -1) {
    const newHtml = html.substring(0, startIndex + 'const quizData = '.length) + 
                    JSON.stringify(data, null, 4) + 
                    html.substring(lastIndex + endMarker.length - 1);
    fs.writeFileSync(htmlPath, newHtml, 'utf-8');
    console.log('FINAL SYNC SUCCESS');
}
