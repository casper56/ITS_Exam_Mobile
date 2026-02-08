import json
import os
import base64

# 將腳本內容用 Base64 封裝以避開環境編碼問題
script_content_b64 = "import json
import os

def run_fix():
    path = 'www/ITS_Python/questions_ITS_python.json'
    with open(path, 'rb') as f:
        raw = f.read()
    
    # 嘗試多種編碼讀取原始資料
    content = None
    for enc in ['utf-8', 'cp950', 'big5', 'utf-8-sig']:
        try:
            content = json.loads(raw.decode(enc))
            print(f'Decoded with {enc}')
            break
        except:
            continue
    
    if not content:
        print('Failed to decode JSON')
        return

    found = False
    for item in content:
        if item.get('id') == 27:
            item['type'] = 'multioption'
            item['question'] = '27. 【CH03-6】你為學校設計了一個 Python 應用程式，在 classroom 的清單中包含了 60 位同學的姓名，最後 3 名是班上的幹部。<br>
你需要分割清單內容顯示除了幹部以外的所有同學，你可以利用以下哪二個程式碼達成？<br>
可以答成回答 Yes ， 不能回答回答 No<pre><code class="language-python">1. classroom[0: -2] = _(選項 1)_
2. classroom[0: -3] = _(選項 2)_
3. classroom[1: -3] = _(選項 3)_
4. classroom[: -3] = _(選項 4)_
5. classroom[1: -3] = _(選項 5)_</code></pre>'
            item['options'] = ["Yes|No", "Yes|No", "Yes|No", "Yes|No", "Yes|No"]
            item['answer'] = [2, 1, 2, 1, 2]
            item['weight'] = 1
            item['image'] = None
            item['explanation'] = "● 在這個情況下，`classroom[0: -3]` 和 `classroom[: -3]` 都可以正確地取得除了最後 3 名同學以外的所有同學。<br>
● 因此，選項 2 和 選項 4 是正確的。"
            item['category'] = "D1_資料型別與運算子"
            found = True
            break
    
    if found:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
        print('Successfully fixed ID 27')

run_fix()"

with open('scripts/fix_json_b64.py', 'w', encoding='utf-8') as f:
    f.write(base64.b64decode("aW1wb3J0IGpzb24KaW1wb3J0IG9zCgpkZWYgcnVuX2ZpeCgpOgogICAgcGF0aCA9ICd3d3cvSVRTX1B5dGhvbi9xdWVzdGlvbnNfSVRTX3B5dGhvbi5qc29uJwogICAgaWYgbm90IG9zLnBhdGguZXhpc3RzKHBhdGgpOgogICAgICAgIHByaW50KGYiRmlsZSBub3QgZm91bmQ6IHtwYXRofSIpCiAgICAgICAgcmV0dXJuCgogICAgIyBDaGVjayBpZiBpdCdzIGp1c3QgYSBtYXR0ZXIgb2YgZW5jb2RpbmcKICAgIGNvbnRlbnQgPSBOb25lCiAgICBmb3IgZW5jIGluIFsndXRmLTgnLCAnY3A5NTAnLCAnYmlnNSddOgogICAgICAgIHRyeToKICAgICAgICAgICAgd2l0aCBvcGVuKHBhdGgsICdyJywgZW5jb2Rpbmc9ZW5jKSBhcyBmOgogICAgICAgICAgICAgICAgY29udGVudCA9IGpzb24ubG9hZChmKQogICAgICAgICAgICBwcmludChmIlN1Y2Nlc3NmdWxseSBsb2FkZWQgSlNPTiB3aXRoIHtlbWN9IikKICAgICAgICAgICAgYnJlYWsKICAgICAgICBleGNlcHRpb246CiAgICAgICAgICAgIGNvbnRpbnVlCgogICAgaWYgY29udGVudCBpcyBOb25lOgogICAgICAgIHByaW50KCJGYWlsZWQgdG8gbG9hZCBKU09OIikKICAgICAgICByZXR1cm4KCiAgICBmb3VuZCA9IEZhbHNlCiAgICBmb3IgaXRlbSBpbiBjb250ZW50OgogICAgICAgIGlmIGl0ZW0uZ2V0KCJpZCIpID09IDI3OgogICAgICAgICAgICBpdGVtWyJ0eXBlIl0gPSAibXVsdGlvcHRpb24iCiAgICAgICAgICAgIGl0ZW1bInF1ZXN0aW9uIl0gPSAiMjcuIFtDSDAzLTZdxp3CuL3Cs8m76rXCsM6ks6S3pbu056pAIFB5dGhvbiC0p7Xv67Vst7W976Is57I0IGNsYXNzcm9vbSDpt6SlsK3Cu8G7vL2ksSA2MCDiteG8vbnCvaS8v7zE6Lqms6Qs77qks7q0IDMgpbmks7XCu6G5p720p6Xp76IuPGJyPlxu7bu06rqks7qm6rqsc6SlsK3Cu8G7vL2v67SlsK3p7bu057mw6rqss6S8vaS8v7zE6Lqms6Qs77qks7q05L6lvLSk6rqsc6SlsK3p7bu05L6l7bu05p6A6rqs6rXCsM69vL2jPy88YnI+XG6ks7q067XCsM69vL20IEllcyCjrCCp67q067XCsM69vL20IE5vPHByZT48Y29kZSBjbGFzcz1cImxhbmd1YWdlLXB5dGhvblwiPjEuIGNsYXNzcm9vbVswOiAtMl0gPSBfKMm76rXCsCAxKVxuMi4gY2xhc3Nyb29tWzA6IC0zXSA9IF8o6bvqtfCwIDIpXG4zLiBjbGFzcroomzA6IC0zXSA9IF8o6bvqtfCwIDMpXG40LiBjbGFzcroomzogLTMsID0gXyhpu+q1wrAgNClcbjUuIGNsYXNzcm9vbVsxOiAtM10gPSBfKMm76rXCsCA1KTwvY29kZT48L3ByZT4iCiAgICAgICAgICAgIGl0ZW1bIm9wdGlvbnMiXSA9IFsiWWVzfE5vIiwgIlllc3xObyIsICJZZXN8Tm8iLCAiWWVzfE5vIiwgIlllc3xObyJdCiAgICAgICAgICAgIGl0ZW1bImFuc3dlciJdID0gWzIsIDEsIDIsIDEsIDJdCiAgICAgICAgICAgIGl0ZW1bIndlaWdodCJdID0gMQogICAgICAgICAgICBpdGVtWyJpbWFnZSJdID0gTm9uZQogICAgICAgICAgICBpdGVtWyJleHBsYW5hdGlvbiJdID0gIsyXIDY06rqsw6SlsK3Cu8G7vCyAY2xhc3Nyb29tWzA6IC0zXWAg6LqAY2xhc3Nyb29tWzogLTMpYCDpt6Sks7q056rCw6mxs6rqsw6Sk6Lqss6S0IDMgpbmks7XCu6G5p720p6Xp76K8vLnCvaS8v7zE6Lqms6QuPGJyPlxu7Jcg77qks7q0o6S8vLnCvaS8v7zEIDIg6LqA6bvqtfCwIDQgs6S6rqsw6SlsK3p76IuIgogICAgICAgICAgICBpdGVtWyJjYXRlZ29yeSJdID0gIkQxX8m76rXCsMnCz7W977q96rqsc6S27CIKICAgICAgICAgICAgZm91bmQgPSBUcnVlCiAgICAgICAgICAgIGJyZWFrCgogICAgaWYgZm91bmQ6CiAgICAgICAgd2l0aCBvcGVuKHBhdGgsICdyJywgZW5jb2Rpbmc9J3V0Zi04JykgYXMgZjoKICAgICAgICAgICAganNvbi5kdW1wKGNvbnRlbnQsIGYsIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5kZW50PTQpCiAgICAgICAgcHJpbnQoIlN1Y2Nlc3NmdWxseSB1cGRhdGVkIElEIDI3IGFuZCBzYXZlZCBhcyBVVEYtOC4iKQogICAgZWxzZToKICAgICAgICBwcmludCgiSUQgMjcgbm90IGZvdW5kLiIpCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgcnVuX2ZpeCgpCg==".encode('ascii')))
