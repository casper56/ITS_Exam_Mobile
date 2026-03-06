import os
import re

def patch_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # 1. Fix submitMatching (Practice mode)
    # Pattern: if (String(finalUserAns[i] || "").trim().toUpperCase() !== String(correctAns[i] || "").trim().toUpperCase())
    submit_matching_pattern = r'if\s*\(\s*String\s*\(\s*finalUserAns\[i\]\s*\|\|\s*""\s*\)\.trim\(\)\.toUpperCase\(\)\s*!==\s*String\s*\(\s*correctAns\[i\]\s*\|\|\s*""\s*\)\.trim\(\)\.toUpperCase\(\)\s*\)'
    new_matching_logic = 'if (parseAnswerToIndex(finalUserAns[i]) !== parseAnswerToIndex(correctAns[i]))'
    
    if re.search(submit_matching_pattern, content):
        content = re.sub(submit_matching_pattern, new_matching_logic, content)
        changed = True

    # 2. Fix submitExam (Mock mode)
    # Pattern: if (String(userLetters[i] || "").trim().toUpperCase() !== String(answers[i] || "").trim().toUpperCase())
    submit_exam_pattern = r'if\s*\(\s*String\s*\(\s*userLetters\[i\]\s*\|\|\s*""\s*\)\.trim\(\)\.toUpperCase\(\)\s*!==\s*String\s*\(\s*answers\[i\]\s*\|\|\s*""\s*\)\.trim\(\)\.toUpperCase\(\)\s*\)'
    new_exam_logic = 'if (parseAnswerToIndex(userLetters[i]) !== parseAnswerToIndex(answers[i]))'

    if re.search(submit_exam_pattern, content):
        content = re.sub(submit_exam_pattern, new_exam_logic, content)
        changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk('www'):
        for file in files:
            if file.endswith('.html'):
                if patch_file(os.path.join(root, file)):
                    print(f"Patched {os.path.join(root, file)}")
                    count += 1
    print(f"Total patched: {count}")

if __name__ == "__main__":
    main()
