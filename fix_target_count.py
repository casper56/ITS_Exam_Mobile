import os

mock_files = [
    'www/AI900/mock_v34.html',
    'www/AZ900/mock_v34.html',
    'www/Generative_AI/mock_v34.html',
    'www/ITS_AI/mock_v34.html',
    'www/ITS_Database/mock_v34.html',
    'www/ITS_softdevelop/mock_v34.html',
    'www/ITS_Python/mock_v34.html',
    'www/ITS_JAVA/mock_v34.html'
]

for file_path in mock_files:
    if not os.path.exists(file_path): continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(
        "const TARGET_OFF_COUNT = 60; // 官方題改為 60 題",
        "const TARGET_OFF_COUNT = 59; // 官方題改為 59 題"
    )
    content = content.replace(
        "const TARGET_SUPP_COUNT = EXAM_LIMIT - TARGET_OFF_COUNT; // 補充題則為 0 題",
        "const TARGET_SUPP_COUNT = EXAM_LIMIT - TARGET_OFF_COUNT; // 補充題則為 1 題"
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")

print("Done.")