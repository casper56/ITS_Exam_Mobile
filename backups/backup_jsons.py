
import os
import shutil

all_jsons = [
    'www/AI900/questions_AI900.json',
    'www/AZ900/questions_AZ900.json',
    'www/Generative_AI/questions_Generative_AI_Foundations.json',
    'www/ITS_AI/questions_ITS_AI.json',
    'www/ITS_Database/questions_ITS_Database.json',
    'www/ITS_softdevelop/questions_ITS_csharp.json',
    'www/ITS_Python/questions_ITS_python.json'
]

for path in all_jsons:
    if os.path.exists(path):
        backup = path.replace('.json', '_backup_YN.json')
        shutil.copy(path, backup)
        print(f"Backup created: {backup}")
