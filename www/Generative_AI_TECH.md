# Generative AI Foundations 技術考點導讀 (Generative_AI_TECH.md)

本文件根據 `www/Generative_AI/questions_Generative_AI_Foundations.json` 題庫內容進行深度分析，涵蓋 LLM 架構、提示工程與 AI 倫理。

---

## 1. Transformer 架構與核心技術
*   **Transformer 模型**：現代生成式 AI 的基石，基於 **自注意力機制 (Self-Attention)**。
*   **編碼器 (Encoder) 與 解碼器 (Decoder)**：
    *   BERT 主要使用編碼器（適合理解）。
    *   GPT 系列主要使用解碼器（適合生成）。
*   **詞元化 (Tokenization)**：將文字拆分為最小單位（Tokens）。
*   **詞嵌入 (Embedding)**：將詞元轉為高維向量，捕捉語意關係。

---

## 2. 提示工程 (Prompt Engineering) —— **核心實務**
*   **Zero-shot Learning**：直接下指令，不提供任何範例。
*   **Few-shot Learning**：提供 1 到 3 個範例，引導模型學習任務模式。
*   **思維鏈 (Chain of Thought, CoT)**：引導模型「一步步思考」，大幅提升複雜問題的準確度。
*   **溫度 (Temperature)**：控制生成結果的隨機性（0 為最精確，1 為最具創意）。

---

## 3. 生成式 AI 的挑戰與倫理
*   **AI 幻覺 (Hallucination)**：模型生成看似真實但事實錯誤的內容。
*   **偏見 (Bias)**：訓練數據中的社會性偏見可能被模型放大。
*   **安全性 (Safety)**：防止模型生成有害、仇恨或不當內容。
*   **事實查核 (Fact-checking)**：生成式內容必須經過人工驗證。

---

## 4. 應用場景
*   **內容生成**：自動寫作、翻譯、總結。
*   **代碼輔助**：輔助編寫、調試與重構程式碼。
*   **多模態 (Multimodal)**：結合文字、圖像、音訊的跨媒介生成。
