import json
import os
import re

def generate_reports():
    config_path = 'www/config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 各科目專屬的官方大綱摘要 (用於補強文件底部)
    objectives_map = {
        "itspy": "* 一、資料型別與運算子\n* 二、流程控制與迴圈\n* 三、輸入與輸出操作\n* 四、程式碼文件與結構\n* 五、故障排除與錯誤處理\n* 六、使用模組與工具",
        "itscs": "* 一、核心程式設計概念\n* 二、物件導向程式設計\n* 三、一般軟體開發\n* 四、網頁應用程式\n* 五、資料庫概念",
        "itsdb": "* 一、資料庫概念\n* 二、資料庫設計\n* 三、資料操作 (SQL)\n* 四、安全性與維護\n* 五、資料庫維護(正規化)",
        "itsai": "* 一、AI 問題定義與倫理\n* 二、資料收集、處理與工程\n* 三、AI 演算法與模型訓練\n* 四、應用整合、部署與監控",
        "ai900": "* 一、AI 工作負載與倫理\n* 二、機器學習基礎\n* 三、Azure 電腦視覺功能\n* 四、Azure 自然語言處理功能\n* 五、知識採礦與生成式 AI",
        "az900": "* 一、雲端基礎概念\n* 二、Azure 架構與服務\n* 三、Azure 管理與治理",
        "genai": "* 一、生成式 AI 基礎概念\n* 二、大型語言模型 (LLM) 運作原理\n* 三、提示工程 (Prompt Engineering)\n* 四、負責任的生成式 AI"
    }

    for subj in config['subjects']:
        json_path = os.path.join(subj['dir'], subj['json'])
        if not os.path.exists(json_path): continue

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
        report.append(f"*   **去重與修復**：清理重複題目，並全面修復 JSON 語法錯誤與圖片路徑。")
        report.append(f"*   **ID 全域重索引**：確保所有題目 ID 具備連續性 (1-{total})，並與系統 Cutoff 同步。")
        report.append(f"*   **模擬考權重校準**：調整隨機抽取演算法，確保各類別覆蓋率符合官方權重。")
        report.append("")
        report.append("## 4. 考點分佈與出題權重評估")
        report.append("")
        report.append(f"若以正式考試 **40 題** 為抽題標準，建議分佈如下：")
        report.append("")
        report.append("| 類別 | 母體題數 | 佔比 | 建議考題數 | 強度評估 |")
        report.append("| :--- | :---: | :---: | :---: | :--- |")
        
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
        report.append(f"> **維護提醒**：本題庫已完成重複項清理，{sorted_cats[0][0] if sorted_cats else ''} 等高佔比類別是獲取認證的基本盤。")
        report.append("")
        report.append("## 5. 考前衝刺必勝策略 (超額訓練法)")
        report.append("")
        report.append("本系統模擬考設定為 **60 題 / 50 分鐘**，而官方實測僅約 **40 題**。這種「超額訓練」旨在建立考生的抗壓性。")
        report.append("")
        report.append("1. **耐力加強**：能在 60 題壓力下維持 80 分，實測 40 題將游刃有餘。")
        report.append("2. **時間壓測**：目標 50 秒處理 1 題，確保實測時有極大餘裕進行檢查。")
        report.append("3. **官方池反射**：目標是看到題目關鍵字即反射正確答案。")
        report.append("")
        report.append("---")
        report.append("")
        report.append("### ITS SPECIALIST EXAM OBJECTIVES")
        report.append(objectives_map.get(subj['id'], "詳細考試大綱請參閱官方文件。"))

        with open(md_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(report))
        print(f"Standardized Report Generated: {md_path}")

if __name__ == '__main__':
    generate_reports()
