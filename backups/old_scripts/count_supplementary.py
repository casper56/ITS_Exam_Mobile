
import json
import os

cutoffs = {
    "AI900": 213,
    "AZ900": 100,
    "Generative_AI": 100,
    "ITS_AI": 94,
    "ITS_Database": 69,
    "ITS_softdevelop": 98,
    "ITS_Python": 94,
    "ITS_JAVA": 80
}

files = {
    "AI900": "www/AI900/questions_AI900.json",
    "AZ900": "www/AZ900/questions_AZ900.json",
    "Generative_AI": "www/Generative_AI/questions_Generative_AI_Foundations.json",
    "ITS_AI": "www/ITS_AI/questions_ITS_AI.json",
    "ITS_Database": "www/ITS_Database/questions_ITS_Database.json",
    "ITS_softdevelop": "www/ITS_softdevelop/questions_ITS_softdevelop.json",
    "ITS_Python": "www/ITS_Python/questions_ITS_python.json",
    "ITS_JAVA": "www/ITS_JAVA/questions_ITS_JAVA.json"
}

print(f"{'Subject':<25} | {'Cutoff':<6} | {'Supp Count':<10} | {'Mock Drawn'}")
print("-" * 65)

for subject, path in files.items():
    if not os.path.exists(path):
        print(f"{subject:<25} | {cutoffs[subject]:<6} | {'FILE NOT FOUND':<10} | -")
        continue
        
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            cutoff = cutoffs[subject]
            supp_questions = [q for q in data if q.get('id', 0) > cutoff]
            supp_count = len(supp_questions)
            
            # Logic from final_clean_repair.py
            # EXAM_LIMIT = 60
            # TARGET_OFF_COUNT = 57 (95%)
            # TARGET_SUPP_COUNT = 3 (5%)
            # stage C fills up to 60 with supplementary questions
            # So if supp_count >= 3, it will draw 3. If less, it draws all available.
            mock_drawn = min(supp_count, 3)
            
            print(f"{subject:<25} | {cutoff:<6} | {supp_count:<10} | {mock_drawn}")
        except Exception as e:
            print(f"{subject:<25} | {cutoffs[subject]:<6} | {'ERROR':<10} | - {e}")
