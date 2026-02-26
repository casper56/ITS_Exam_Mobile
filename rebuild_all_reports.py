import json
import os
import re

def generate_reports():
    config_path = 'www/config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    for subj in config['subjects']:
        json_path = os.path.join(subj['dir'], subj['json'])
        if not os.path.exists(json_path):
            continue

        with open(json_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)

        total = len(questions)
        types = {'single': 0, 'multiple': 0, 'multioption': 0}
        cats = {}
        for q in questions:
            t = q.get('type', 'single')
            if t == 'multioption' or any('|' in str(o) for o in (q.get('quiz', []) or q.get('options', []))):
                types['multioption'] += 1
            elif t == 'multiple':
                types['multiple'] += 1
            else:
                types['single'] += 1
            
            c = q.get('category', '一般')
            cats[c] = cats.get(c, 0) + 1

        md_file = subj['html'].replace('.html', '.md')
        md_path = os.path.join(subj['dir'], md_file)
        
        existing_strategy = ""
        existing_objectives = ""
        if os.path.exists(md_path):
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "## 5. 考前衝刺必勝策略" in content:
                    parts = content.split("## 5. 考前衝刺必勝策略")
                    if len(parts) > 1:
                        existing_strategy = parts[1].split("---")[0].strip()
                if "ITS SPECIALIST EXAM OBJECTIVES" in content:
                    existing_objectives = content.split("---")[-1].strip()

        report = []
        report.append(f"# {subj['title']} 認證題庫統計分析 (2026-02-27 更新)")
        report.append("")
        report.append("## 1. 題庫規模與組成")
        report.append(f"*   **總題數**：{total} 題")
        report.append(f"*   **官方版本 (1-{subj['cutoff']})**：{subj['cutoff']} 題")
        report.append(f"*   **補充/模擬版本 ({subj['cutoff']+1}-{total})**：{total - subj['cutoff']} 題")
        report.append("")
        report.append("## 2. 題型分佈 (精確統計)")
        report.append(f"*   **單選題 (Single Choice)**：{types['single']} 題")
        report.append(f"*   **複選題 (Multiple Choice)**：{types['multiple']} 題")
        report.append(f"*   **多重下拉/題組 (Multi-option)**：{types['multioption']} 題")
        report.append("")
        report.append("## 3. 2026-02-27 系統性編排更新")
        report.append("今日針對全科系題庫執行了以下優化：")
        report.append(f"*   **ID 全域重索引**：因應題量微調，確保所有題目 ID 具備連續性且與 `config.json` 同步。")
        report.append(f"*   **模擬考權重校準**：基於最新題量分佈，調整了模擬考抽取演算法，確保高頻考點覆蓋率。")
        report.append("")
        report.append("## 4. 考點分佈與出題權重評估")
        report.append("")
        report.append(f"若以正式考試 **40 題** 為抽題標準，建議分佈如下：")
        report.append("")
        report.append("| 類別 | 母體題數 | 佔比 | 建議考題數 | 強度評估 |")
        report.append("| :--- | :---: | :---: | :---: | :--- |")
        
        # Sort cats by their prefix (D0, D1, D2...)
        def get_cat_prefix(cat_name):
            match = re.search(r'D(\d+)', cat_name)
            return int(match.group(1)) if match else 999
        
        sorted_cats = sorted(cats.items(), key=lambda x: get_cat_prefix(x[0]))
        
        for cat_name, count in sorted_cats:
            percentage = (count / total) * 100
            suggested = round(40 * (count / total))
            intensity = "🔴 高強度" if percentage > 20 else ("🟡 核心" if percentage > 10 else "🟢 適中")
            report.append(f"| {cat_name} | {count} | {percentage:.1f}% | {suggested} | {intensity} |")
        
        report.append("")
        report.append("> **維護提醒**：本題庫已完成全量分析，建議考生優先練習高佔比類別以獲取認證基本盤。")
        report.append("")
        report.append("## 5. 考前衝刺必勝策略 (超額訓練法)")
        report.append("")
        if existing_strategy:
            report.append(existing_strategy)
        else:
            report.append("1. **耐力加強**：實際考試 40 題，模擬考 60 題，鍛鍊高強度專注力。")
            report.append("2. **時間壓測**：平均 50 秒處理 1 題，確保實測時有充裕檢查時間。")
        
        report.append("")
        report.append("---")
        report.append("")
        if existing_objectives:
            report.append(existing_objectives)
        else:
            report.append("### ITS SPECIALIST EXAM OBJECTIVES")
            report.append("詳細考試大綱請參閱官方文件。")

        with open(md_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(report))
        print(f"Generated: {md_path}")

if __name__ == '__main__':
    generate_reports()
