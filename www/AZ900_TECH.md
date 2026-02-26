# AZ-900: Azure Fundamentals 技術考點導讀 (AZ900_TECH.md)

本文件根據 `www/AZ900/questions_AZ900.json` 題庫內容進行深度分析，涵蓋雲端基礎概念、Azure 架構與治理。

---

## 1. 雲端運算概念 (Cloud Concepts)
*   **共享責任模型 (Shared Responsibility)**：明確區分雲端供應商與客戶在不同服務模式下的責任。
*   **服務模式**：
    *   **IaaS (基礎結構即服務)**：彈性最高，客戶負責操作系統與應用程式（如 VM）。
    *   **PaaS (平台即服務)**：專注於開發應用，由 Azure 管理伺服器與運行環境（如 App Service）。
    *   **SaaS (軟體即服務)**：直接使用軟體，由 Azure 管理一切（如 Office 365）。
*   **雲端特性**：高可用性 (High Availability)、可延展性 (Scalability)、敏捷性 (Agility) 與災難復原 (Disaster Recovery)。

---

## 2. Azure 核心架構 (Architecture)
*   **區域 (Region)**：資料中心的分組，地理上相互獨立。
*   **可用性區域 (Availability Zones)**：單一區域內獨立的資料中心，防止機房級故障。
*   **資源群組 (Resource Group)**：邏輯容器，用於管理生命週期相同的 Azure 資源。
*   **管理群組 (Management Groups)**：管理多個訂閱 (Subscription) 的治理。

---

## 3. 治理與管理工具
*   **Azure Policy**：強制執行規則，確保資源符合合規性。
*   **RBAC (角色型存取控制)**：精確管理「誰可以對資源做什麼」。
*   **Azure Resource Manager (ARM)**：部署與管理資源的入口。
*   **成本管理 (TCO/Cost Management)**：預測、監控與優化 Azure 開銷。

---

## 4. Azure 安全性與識別
*   **Microsoft Entra ID (原 AAD)**：核心身分識別服務（支援多重要素驗證 MFA）。
*   **Zero Trust (零信任)**：核心原則為「不信任，始終驗證」。
