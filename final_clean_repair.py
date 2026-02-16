import json
import os
import glob

def clean_repair_all():
    subject_dirs = [d for d in os.listdir('www') if os.path.isdir(os.path.join('www', d)) and d != 'assets']
    
    # 這是標準的 V3.4 輔助函式
    helper_code = """
    function parseAnswerToIndex(val) {
        if (typeof val === 'number') return val - 1;
        if (typeof val === 'string') {
            const code = val.toUpperCase().charCodeAt(0);
            if (code >= 65 && code <= 90) return code - 65;
            return parseInt(val) - 1;
        }
        return -1;
    }
    """

    for subject_dir in subject_dirs:
        if subject_dir == 'ITS_Python':
            print(f"Skipping {subject_dir} (Manually optimized V3.4)")
            continue
        dir_path = os.path.join('www', subject_dir)
        mock_path = os.path.join(dir_path, 'mock_exam.html')
        if not os.path.exists(mock_path): continue
        
        json_files = glob.glob(os.path.join(dir_path, 'questions_*.json'))
        if not json_files: continue
        
        with open(json_files[0], 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)
        json_str = json.dumps(quiz_data, ensure_ascii=False, indent=2)
        
        with open(mock_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 精確同步數據 (不使用正則，改用 Marker 查找)
        start_marker = 'const allQuestions = ['
        end_marker = '];'
        
        s_idx = content.find(start_marker)
        if s_idx != -1:
            # 尋找最近的結尾
            e_idx = content.find(end_marker, s_idx)
            if e_idx != -1:
                # 替換數據
                content = content[:s_idx] + "const allQuestions = " + json_str + content[e_idx+2:]
        
        # 2. 注入輔助函式 (僅在不存在時)
        if 'function parseAnswerToIndex' not in content:
            # 注入在 const allQuestions 之前
            content = content.replace('const allQuestions =', helper_code + "\n    const allQuestions =")
            
        # 3. 修復比對邏輯 (parseInt 升級)
        # 僅做最基本的文字替換，避免損壞結構
        content = content.replace('(parseInt(a) - 1)', 'parseAnswerToIndex(a)')
        content = content.replace('parseInt(item.answer) - 1', 'parseAnswerToIndex(item.answer)')
        if 'item.answer.map(a => parseAnswerToIndex(a))' not in content:
            content = content.replace('item.answer.map(a => parseInt(a) - 1)', 'item.answer.map(a => parseAnswerToIndex(a))')

        # 4. 強制寫回 (UTF-8)
        with open(mock_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"V3.4 Safe Refresh: {subject_dir}")

if __name__ == "__main__":
    clean_repair_all()
