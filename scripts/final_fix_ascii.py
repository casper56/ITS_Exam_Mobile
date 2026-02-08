import json
import base64
import os

def run_fix():
    path = 'www/ITS_Python/questions_ITS_python.json'
    with open(path, 'rb') as f:
        data = json.load(f)
    
    # Correct ID 27 JSON string (Base64 encoded to avoid encoding issues in script)
    # Content: { "id": 27, "type": "multioption", "question": "...", "options": [...], "answer": [...], "category": "D1_資料型別與運算子" }
    b64_data = "eyAiaWQiOiAyNywgInR5cGUiOiAibXVsdGlvcHRpb24iLCAicXVlc3Rpb24iOiAiMjcuIFtDSDAzLTZdxp3CuL3Cs8m76rXCsM6ks6S3pbu056pAIFB5dGhvbiC0p7Xv67Vst7W976Is57I0IGNsYXNzcm9vbSDpt6SlsK3Cu8G7vL2ksSA2MCDiteG8vbnCvaS8v7zE6Lqms6Qs77qks7q0IDMgpbmks7XCu6G5p720p6Xp76IuPGJyPlxu7bu06rqks7qm6rqsc6SlsK3Cu8G7vL2v67SlsK3p7bu057mw6rqss6S8vaS8v7zE6Lqms6Qs77qks7q05L6lvLSk6rqsc6SlsK3p7bu05L6l7bu05p6A6rqs6rXCsM69vL2jPy88YnI+XG6ks7q067XCsM69vL20IEllcyCjrCCp67q067XCsM69vL20IE5vPHByZT48Y29kZSBjbGFzcz1cImxhbmd1YWdlLXB5dGhvblwiPjEuIGNsYXNzcm9vbVswOiAtMl0gPSBfKMm76rXCsCAxKVxuMi4gY2xhc3Nyb29tWzA6IC0zXSA9IF8o6bvqtfCwIDIpXG4zLiBjbGFzcroomzA6IC0zXSA9IF8o6bvqtfCwIDMpXG40LiBjbGFzcroomzogLTMsID0gXyhpu+q1wrAgNClcbjUuIGNsYXNzcm9vbVsxOiAtM10gPSBfKMm76rXCsCA1KTwvY29kZT48L3ByZT4iLCAib3B0aW9ucyI6IFsiWWVzfE5vIiwgIlllc3xObyIsICJZZXN8Tm8iLCAiWWVzfE5vIiwgIlllc3xObyJdLCAiYW5zd2VyIjogWzIsIDEsIDIsIDEsIDJdLCAid2VpZ2h0IjogMSwgImltYWdlIjogbnVsbCwgImVleHBsYW5hdGlvbiI6ICLMsiDpt6Sks7q056rCw6mxs6rqsw6Sk6Lqss6S0IDMgpbmks7XCu6G5p720p6Xp76K8vLnCvaS8v7zE6Lqms6QuPGJyPlxu7Jcg77qks7q0o6S8vLnCvaS8v7zEIDIg6LqA6bvqtfCwIDQgs6S6rqsw6SlsK3p76IuIiwgImNhdGVnb3J5IjogIkQxX8m76rXCsMnCz7W977q96rqsc6S27CIgfQ=="
    fixed_obj = json.loads(base64.b64decode(b64_data).decode('utf-8'))

    found = False
    for i, item in enumerate(data):
        if item.get("id") == 27:
            data[i] = fixed_obj
            found = True
            break
    
    if found:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Successfully fixed ID 27 in JSON.")
    else:
        print("ID 27 not found.")

if __name__ == "__main__":
    run_fix()
