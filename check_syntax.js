const fs = require('fs');
const content = fs.readFileSync('www/ITS_Python/ITS_Python.html', 'utf-8');

// extract the content of the script tags and run a simple syntax check
const scriptMatches = content.match(/<script>([\s\S]*?)<\/script>/g);
if (scriptMatches) {
    scriptMatches.forEach((script, index) => {
        const code = script.replace(/<\/?script>/g, '');
        try {
            new Function(code);
            console.log(`Script ${index + 1}: Syntax OK`);
        } catch (e) {
            console.log(`Script ${index + 1}: Syntax Error - ${e.message}`);
        }
    });
} else {
    console.log("No scripts found");
}
