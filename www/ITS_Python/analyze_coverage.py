import json
import re
import os

def analyze_its_python():
    json_path = 'questions_ITS_python.json'
    output_path = 'ITS_Python_Analysis.md'

    # 1. 定義章節映射
    chapter_map = {
        'CH01': '一、使用資料型別和運算子進行操作 (CH01)',
        'CH02': '二、使用決策和迴圈進行流程控制 (CH02)',
        'CH03': '三、輸入和輸出操作 (CH03)',
        'CH04': '四、程式碼文件和結構 (CH04)',
        'CH05': '五、故障排除和錯誤處理 (CH05)',
        'CH06': '六、使用模組和工具進行操作 (CH06)',
        'CH07': '七、進階模組與應用 (CH07)',  # 擴增
        'CH08': '八、單元測試與錯誤處理進階 (CH08)', # 擴增
        'Advanced': '進階/其他主題 (APCS/演算法/其他)',
        '補充': '補充教材'
    }

    # 2. 讀取題目 JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found.")
        return

    # 3. 分析數據
    stats = {}
    for key in chapter_map.keys():
        stats[key] = {'title': chapter_map[key], 'count': 0, 'question_ids': []}
    stats['Unknown'] = {'title': '未分類/格式不符', 'count': 0, 'question_ids': []}

    # 正則表達式
    # 捕捉 【CHxx...】
    ch_pattern = re.compile(r'【(CH\d+)')
    # 捕捉 【演算法...】, 【APCS...】, 【Python...】
    other_pattern = re.compile(r'【(演算法|APCS|Python)')

    for q in questions:
        q_id = q.get('id')
        q_text = q.get('question', '')
        
        category = 'Unknown'
        
        ch_match = ch_pattern.search(q_text)
        other_match = other_pattern.search(q_text)

        if ch_match:
            ch_code = ch_match.group(1)
            if ch_code in stats:
                category = ch_code
            else:
                # 如果是 CH09 等未定義的，暫時歸類為 Unknown 或動態新增
                # 這裡簡單處理，若有 CH09 就歸 Unknown，除非我們想動態加
                pass 
        elif other_match:
            category = 'Advanced'
        elif '補充' in q_text:
            category = '補充'

        stats[category]['count'] += 1
        stats[category]['question_ids'].append(q_id)

    # 4. 生成報告
    report_lines = []
    report_lines.append("# ITS Python 題庫分佈分析報告")
    report_lines.append(f"\n- **分析檔案**: `{json_path}`")
    report_lines.append(f"- **總題數**: {len(questions)}")
    report_lines.append("\n## 章節分佈統計\n")
    
    report_lines.append("| 章節代號 | 章節名稱 | 題數 | 佔比 |")
    report_lines.append("| :--- | :--- | :---: | :---: |")

    total_count = len(questions)
    
    # 排序鍵值
    sorted_keys = sorted([k for k in stats.keys() if k.startswith('CH')]) + ['Advanced', '補充', 'Unknown']
    
    for key in sorted_keys:
        if key not in stats: continue
        data = stats[key]
        percentage = (data['count'] / total_count * 100) if total_count > 0 else 0
        report_lines.append(f"| {key} | {data['title']} | {data['count']} | {percentage:.1f}% |")

    report_lines.append("\n## 詳細題目清單\n")
    
    for key in sorted_keys:
        if key not in stats: continue
        data = stats[key]
        if data['count'] == 0: continue
        
        report_lines.append(f"### {data['title']} (共 {data['count']} 題)")
        
        ids = data['question_ids']
        ids_str_list = []
        chunk_size = 15
        for i in range(0, len(ids), chunk_size):
            chunk = ids[i:i+chunk_size]
            ids_str_list.append(", ".join(map(str, chunk)))
            
        report_lines.append("> " + "<br>".join(ids_str_list))
        report_lines.append("")

    # 5. 寫入檔案
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"Analysis complete. Report saved to {output_path}")

if __name__ == "__main__":
    analyze_its_python()
