import json

def audit_git():
    with open('www/ITS_softdevelop/questions_ITS_csharp.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("===== Git Related Questions in ITS SoftDevelop =====")
    for q in data:
        q_text = q['question'].lower()
        if 'git' in q_text or 'github' in q_text:
            print(f"ID {q['id']} | Category: {q.get('category')} | {q['question'][:60]}...")

if __name__ == "__main__":
    audit_git()
