import json
import sys

def run():
    files = ['www/ITS_Python/questions_ITS_python.json', 'www/ITS_softdevelop/questions_ITS_csharp.json']
    for fp in files:
        print("\nFILE:", fp)
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        stats = {}
        for q in data:
            c = q.get('category', 'None')
            stats[c] = stats.get(c, 0) + 1
        for name in sorted(stats.keys()):
            h = name.encode('utf-8').hex()
            # print separately to avoid encoding issues in combined f-string
            sys.stdout.write("Name: ")
            sys.stdout.flush()
            # Try to write name, fallback if fails
            try:
                # Use a safe way to print to windows console
                print(name, end='')
            except:
                print("[Encoding Error]", end='')
            print(f" | Count: {stats[name]} | Hex: {h}")

if __name__ == "__main__":
    run()
