import os

# 1. Read the correct template (V3.2 Standard)
with open('www/ITS_Python/mock_exam.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 2. Define targets and replacements
targets = [
    {
        'path': 'www/Generative_AI/mock_exam.html',
        'title': 'Generative AI Foundations',
        'wrong_key': 'generative_ai_wrong_ids',
        'limit': 40
    },
    {
        'path': 'www/ITS_AI/mock_exam.html',
        'title': 'ITS Artificial Intelligence',
        'wrong_key': 'its_ai_wrong_ids',
        'limit': 40
    },
    {
        'path': 'www/ITS_Database/mock_exam.html',
        'title': 'ITS Database Administration',
        'wrong_key': 'its_database_wrong_ids',
        'limit': 40
    },
    {
        'path': 'www/ITS_softdevelop/mock_exam.html',
        'title': 'ITS Software Development',
        'wrong_key': 'its_softdevelop_wrong_ids',
        'limit': 50
    }
]

# 3. Apply changes
for t in targets:
    new_content = template
    
    # 1. Replace Title in <title> and <h5>
    new_content = new_content.replace('ITS Python Programming', t['title'])
    
    # 2. Replace WRONG_KEY and EXAM_LIMIT
    old_const_line = "const EXAM_LIMIT = 50, WRONG_KEY = 'its_python_wrong_ids';"
    new_const_line = f"const EXAM_LIMIT = {t['limit']}, WRONG_KEY = '{t['wrong_key']}';"
    new_content = new_content.replace(old_const_line, new_const_line)

    # 3. Replace External Script Source
    # The template uses <script src="questions_data.js"></script>
    # We want to replace it with inline placeholder for final_clean_repair.py to fill
    new_content = new_content.replace(
        '<script src="questions_data.js"></script>',
        '<script>\n    const allQuestions = []; // Placeholder for injection'
    )
    
    # Write file
    with open(t['path'], 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {t['path']}")
