const fs = require('fs');
let html = fs.readFileSync('www/ITS_Python/mock_v34.html', 'utf-8');

let m = html.match(/function initExam\(\) \{(.+?)function renderQuestion/s);
if (m) {
    let code = `
        let confirm = () => true;
        let localStorage = {getItem:()=>null, setItem:()=>{}};
        let document = {getElementById:()=>({innerText:""})};
        let window = {};
        let EXAM_LIMIT = 5;
        let startTimer = () => {};
        let allQuestions = ` + JSON.stringify(JSON.parse(fs.readFileSync('www/ITS_Python/questions_ITS_python.json', 'utf-8'))) + `;
        let examQuestions = [];
        let selectedSlotIdx = -1;
        let historySet = new Set();
        let userAnswers = {};
        let REPLACE_CUTOFF = 60;
        function renderQuestion() {}
        ` + html.match(/function parseAnswerToIndex\(val\) \{.*?\}/s)[0] + `
        function initExam() {` + m[1] + `}
        initExam();
        console.log(JSON.stringify(examQuestions.filter(q => q.type==="choicelist").slice(0, 3).map(q => ({id: q.id, type: q.type, answer: q.answer, options: q.options})), null, 2));
    `;
    fs.writeFileSync('test_mock.js', code);
}
