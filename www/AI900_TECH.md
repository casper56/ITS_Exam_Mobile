# AI-900: Azure AI Fundamentals 技術考點導讀 (AI900_TECH.md)

本文件根據 `www/AI900/questions_AI900.json` 題庫內容進行深度分析，協助考生掌握微軟 Azure AI 認證的核心邏輯。

---

## 1. 責任 AI 準則 (Responsible AI) —— **絕對核心**
微軟強調的六大 AI 準則在題庫中佔比極高：
*   **公平性 (Fairness)**：AI 系統應公平對待所有人，避免偏見。
*   **可靠性與安全性 (Reliability & Safety)**：AI 系統應在預期內運作，並能抵禦惡意攻擊。
*   **隱私與安全性 (Privacy & Security)**：尊重個人隱私，保護數據安全。
*   **包容性 (Inclusiveness)**：AI 應賦予每個人權力並吸引人們參與。
*   **透明性 (Transparency)**：使用者應了解 AI 系統的運作方式與限制。
*   **權責歸屬 (Accountability)**：設計與部署 AI 的人應對其行為負責。

---

## 2. 核心 AI 工作負載 (Workloads)
*   **機器學習 (Machine Learning)**：預測性模型的基礎（回歸、分類、分群）。
*   **異常偵測 (Anomaly Detection)**：識別資料中的異常變動（如詐欺偵測）。
*   **電腦視覺 (Computer Vision)**：影像分析、臉部辨識、OCR（文字識別）。
*   **自然語言處理 (NLP)**：文字分析、情感分析、語言翻譯。
*   **對話式 AI (Conversational AI)**：機器人與虛擬助理（Bot Service）。

---

## 3. Azure AI 服務工具
*   **Azure Machine Learning**：雲端端對端機器學習平台。
*   **Azure Cognitive Services (現併入 Azure AI Services)**：
    *   **Vision**: 影像處理。
    *   **Speech**: 語音轉文字/文字轉語音。
    *   **Language**: 語法分析、翻譯。
*   **Azure OpenAI Service**：整合了 GPT-3, GPT-4, DALL-E 等先進模型。

---

## 4. 機器學習基礎概念
*   **特徵 (Features)**：用於預測的輸入變數。
*   **標籤 (Labels)**：模型嘗試預測的結果（僅監督式學習有標籤）。
*   **模型評估**：
    *   **回歸**: RMSE, R²。
    *   **分類**: Accuracy, Precision, Recall。
