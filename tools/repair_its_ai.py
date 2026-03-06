
import json
import os
import re

def categorize_question(q_text):
    # D1: AI Problem Definition & Ethics
    if any(k in q_text for k in ['倫理', '道德', '成功指標', '未用AI', '未用 AI', 'CEO', '透明度', '公共問題', '法律', '合約', '偏差', '錄取標準', '公平性', '族群']):
        return "D1_AI問題定義與倫理"
    
    # D2: Data Collection & Engineering
    if any(k in q_text for k in ['磁碟使用量', '編碼', '影像資料', '圖像資料', '表格式資料', '文字資料', '時間序列', '特徵', 'One-Hot', 'PCA', '主成分分析', '資料集', '訓練集', '測試集', '驗證集', '降維', '維度', '資料不平衡', '資料缺失', '極端值', '擬合', '偏差', '方差', '變異性', '資料分享', '儲存空間', '伺服器']):
        return "D2_資料收集、處理與工程"
    
    # D3: AI Algorithms & Models
    if any(k in q_text for k in ['決策樹', '支援向量機', '神經網路', 'K-Means', '叢集', '分類', '迴歸', '增強式學習', '混淆矩陣', '準確率', '精確率', '查準率', '召回率', '均方根誤差', 'RMSE', 'BLEU', '推斷', 'Inference', '指標']):
        return "D3_AI演算法與模型"
    
    # D4: Application Integration & Deployment
    if any(k in q_text for k in ['臉部辨識', '保全人員', '培訓計畫', '部署', '生產環境', '業務效益', '整合', '管線']):
        return "D4_應用整合與部署"
    
    # D5: Maintenance & Monitoring
    if any(k in q_text for k in ['監視', '安全事件', '安全性事件', '漂移', '重新訓練', '監控', '退役', '效能的可見度']):
        return "D5_生產環境維護與監控"
    
    return "D1_AI問題定義與倫理" # Default

def process_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_data = []
    for i, item in enumerate(data):
        item['id'] = i + 1
        q_content = "".join(item['question'])
        item['category'] = categorize_question(q_content)
        
        # Additional logic for specific known items
        if '重新訓練' in q_content or '模型漂移' in q_content or '重新接受訓練' in q_content:
            item['category'] = "D5_生產環境維護與監控"
        if '安全性事件' in q_content or '安全事件' in q_content:
            item['category'] = "D5_生產環境維護與監控"
            
        new_data.append(item)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    print(f"Processed {file_path}")

# Paths
json_path = 'json_backup_test/questions_ITS_AI.json'
www_json_path = 'www/ITS_AI/questions_ITS_AI.json'
www_js_path = 'www/ITS_AI/questions_data.js' # Assuming it might exist or be questions_practice.js

# Execute
if os.path.exists(json_path):
    process_json(json_path)
if os.path.exists(www_json_path):
    process_json(www_json_path)
