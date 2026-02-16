
import os
import shutil

subjects = [
    'www/AI900/questions_AI900.json',
    'www/AZ900/questions_AZ900.json',
    'www/Generative_AI/questions_Generative_AI_Foundations.json',
    'www/ITS_AI/questions_ITS_AI.json',
    'www/ITS_Database/questions_ITS_Database.json',
    'www/ITS_softdevelop/questions_ITS_csharp.json'
]

for f in subjects:
    backup = f.replace('.json', '_backup_v3.4.json')
    if os.path.exists(backup):
        shutil.copy(backup, f)
        print(f"Restored: {f}")
    else:
        print(f"Backup not found for: {f}")
