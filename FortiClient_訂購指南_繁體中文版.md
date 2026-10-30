# Fortinet FortiClient 訂購指南 (Ordering Guide)
**版本代碼：FC-OG-R27-20260429**  
**繁體中文專業對照版**

---

## 目錄
1. [FortiClient 產品概述與關鍵要點](#1-forticlient-產品概述與關鍵要點)
2. [完整功能比較表 (Feature Matrix)](#2-完整功能比較表-feature-matrix)
3. [訂購資訊：依設備授權 (Device-based Licensing)](#3-訂購資訊依設備授權-device-based-licensing)
4. [FortiCare 最佳實踐諮詢服務 (BPS)](#4-forticare-最佳實踐諮詢服務-bps)
5. [升級路徑矩陣 (Upgrade Matrix)](#5-升級路徑矩陣-upgrade-matrix)
6. [獨立版 FortiClient (Standalone / User-based)](#6-獨立版-forticlient-standalone--user-based)
7. [原廠教育訓練與認證 (Training & Certification)](#7-原廠教育訓練與認證-training--certification)
8. [常見問題集 (FAQ)](#8-常見問題集-faq)
9. [導入與上線服務 (Onboarding)](#9-導入與上線服務-onboarding)

---

## 1. FortiClient 產品概述與關鍵要點

FortiClient 提供極具彈性的訂購架構以滿足各企業組織多樣化的資安需求，全面支援**依設備授權模式（Device-based Licensing）**。

### 核心要點包含：
* **部署模式選擇 (Deployment Options)**：客戶可依架構自由選擇**雲端代管（Cloud）**或**地端內部部署（On-Premise）**。
* **解決方案料號 (Solution SKUs)**：針對不同安全層級量身打造特定 SKU 套件，包含 **VPN/ZTNA**、**EPP/ATP** 以及 **Managed FortiClient（原廠專家代管服務）**。
* **附加增值服務 (Additional Services)**：提供專用服務料號，例如端點數位鑑識分析（Endpoint Forensics Analysis）與 FortiCare 最佳實踐顧問諮詢（BPS）。
* **FortiToken 授權限制**：FortiClient 軟體授權**不包含** FortiToken 多因子驗證授權，必須依需求另行加購。
* **設備階梯授權包 (Device-Based Licensing)**：FortiClient 訂購單位為設備數量包，標準級距為 **25、500、2000 與 10000 台設備**。
* **訂單生命週期管理 (Order Lifecycle Management)**：推薦使用 **Co-term（合約到期日對齊工具）**管理後續增購（Additions）、續約（Renewals）與升級（Upgrades），藉此將多筆合約統一至相同到期日，大幅簡化授權管理。
* **跨架構升級限制 (Upgrade Limitations)**：**不支援**直接由地端（On-Premise）SKU 升級為雲端（Cloud）SKU。若欲切換架構，必須購買全新 SKU 並綁定至新的 EMS 執行個體。

---

## 2. 完整功能比較表 (Feature Matrix)

> 符號說明：`✔` 代表內含該功能；`—` 代表未包含；`加購` 代表需額外選購料號。

| 功能類別與特性項目 | VPN / ZTNA | EPP / ATP | MANAGED (代管) |
| :--- | :---: | :---: | :---: |
| **零信任代理 (ZERO TRUST AGENT)** | | | |
| 零信任網路存取 (ZTNA) | ✔ | ✔ | ✔ |
| 集中化管理 (Central Management via EMS) | ✔ | ✔ | ✔ |
| 集中日誌記錄與報表 (Central Logging and Reporting) | ✔ | ✔ | ✔ |
| SSL VPN 支援多因子驗證 (MFA)* | ✔ | ✔ | ✔ |
| IPsec VPN 支援多因子驗證 (MFA)* | ✔ | ✔ | ✔ |
| 行動代理單一登入 (Single Sign On Mobility Agent) | ✔ | ✔ | ✔ |
| **IT 系統衛生與弱點管理 (IT HYGIENE)** | | | |
| 弱點偵測代理與自動修補 (Vulnerability Agent & Remediation) | ✔ | ✔ | ✔ |
| FortiGuard 網頁過濾 (Web Filtering) | ✔ | ✔ | ✔ |
| 軟體資產清冊盤點 (Software Inventory) | — | ✔ | ✔ |
| 抽取式媒體控制 / 外接儲存裝置管控 (Removable Media Control) | — | ✔ | ✔ |
| **雲端存取安全代理 (CASB)** | | | |
| 基於雲端/API 之 CASB (Cloud/API-based CASB) | ✔ | ✔ | ✔ |
| SaaS 應用程式控制 / 內嵌式 CASB (Inline CASB) | ✔ | ✔ | ✔ |
| FortiGuard 即時 SaaS 應用特徵資料庫更新 | ✔ | ✔ | ✔ |
| 雲端資料惡意軟體偵測 (Malware Detection for Cloud Data) | ✔ | ✔ | ✔ |
| **端點防護平台 (ENDPOINT SECURITY - EPP)** | | | |
| FortiClient 雲端沙箱 (Cloud Sandbox SaaS) | — | ✔ | ✔ |
| FortiSandbox 整合 (PaaS / 公有雲 / 地端設備) | ✔ | ✔ | ✔ |
| 人工智慧 AI 次世代防毒引擎 (Next-Gen Antivirus) | — | ✔ | ✔ |
| 自動化端點隔離 (Automated Endpoint Quarantine) | — | ✔ | ✔ |
| 勒索軟體防護 (Ransomware Protection) | — | ✔ | ✔ |
| FortiGuard 疫情爆發即時防禦 (Outbreak Detection) | — | ✔ | ✔ |
| **原廠專家代管服務 (MANAGED FORTICLIENT SERVICE)** | | | |
| 端點設備上線導入 (Endpoint Onboarding) | — | — | ✔ |
| 初始環境佈署配置 (Initial Provisioning) | — | — | ✔ |
| Fortinet Security Fabric 安全聯防整合設定 | — | — | ✔ |
| 端點弱點狀態持續監控 (Vulnerability Monitoring) | — | — | ✔ |
| 端點資安事件威脅監控 (Endpoint Security Monitoring) | — | — | ✔ |
| **其他與進階支援服務 (ADDITIONAL SERVICES)** | | | |
| 最佳實踐顧問諮詢 (FortiCare BPS Consultation) | 帳戶加購 | 帳戶加購 | ✔ (內含) |
| 端點數位鑑識分析服務 (Endpoint Forensics Analysis)** | 選購 | 選購 | 選購 |
| 7x24 原廠技術支援 (24x7 Support) | ✔ | ✔ | ✔ |
| 地端 / 實體隔離無網環境支援 (On-premise / Air Gap Option) | ✔ | ✔ | — |

*註解說明：*  
*\* FortiClient 授權不包含 FortiToken 權益，需另行選購。*  
*\*\* 此項目必須採購獨立的專用 SKU 組合套件。*  
*說明：Chromebook 亦支援透過 EMS 進行集中管理、FortiGuard 網頁過濾及加值服務。FortiSASE 訂購資訊已獨立移至 FortiSASE 訂購指南，支援由 FortiClient 授權升級為 FortiSASE。*

---

## 3. 訂購資訊：依設備授權 (Device-based)

FortiClient 授權以 **25、500、2000 及 10000 台設備包** 進行訂購。以下為最新標準料號清單：

### (1) 標準授權料號表 (Standard Licenses)

| 部署架構 (Solution) | 設備數量級距 (SKU License) | VPN / ZTNA | EPP / ATP | MANAGED (專家代管) |
| :--- | :--- | :--- | :--- | :--- |
| **雲端代管 (Cloud)** | **25-pack** | `FC1-10-EMS05-428-01-DD` | `FC1-10-EMS05-429-01-DD` | `FC1-10-EMS05-485-01-DD` |
| | **500-pack** | `FC2-10-EMS05-428-01-DD` | `FC2-10-EMS05-429-01-DD` | `FC2-10-EMS05-485-01-DD` |
| | **2000-pack** | `FC3-10-EMS05-428-01-DD` | `FC3-10-EMS05-429-01-DD` | `FC3-10-EMS05-485-01-DD` |
| | **10000-pack** | `FC4-10-EMS05-428-01-DD` | `FC4-10-EMS05-429-01-DD` | `FC4-10-EMS05-485-01-DD` |
| **地端部署 (On-premise)** | **25-pack** | `FC1-10-EMS04-428-01-DD` | `FC1-10-EMS04-429-01-DD` | *不適用 (N/A)* |
| | **500-pack** | `FC2-10-EMS04-428-01-DD` | `FC2-10-EMS04-429-01-DD` | *不適用 (N/A)* |
| | **2000-pack** | `FC3-10-EMS04-428-01-DD` | `FC3-10-EMS04-429-01-DD` | *不適用 (N/A)* |
| | **10000-pack** | `FC4-10-EMS04-428-01-DD` | `FC4-10-EMS04-429-01-DD` | *不適用 (N/A)* |

*(註：料號結尾的 `-DD` 代表訂購年期，例如 `-12` 為 1 年期、`-36` 為 3 年期、`-60` 為 5 年期等)*

---

### (2) 含數位鑑識分析服務料號表 (With Forensics Analysis Service)

| 部署架構 | 設備數量級距 | VPN / ZTNA | VPN/ZTNA + EPP/ATP | MANAGED (代管) |
| :--- | :--- | :--- | :--- | :--- |
| **依設備授權 (Device-based)** | **25-pack** | `FC1-10-EMS05-537-01-DD` | `FC1-10-EMS05-538-01-DD` | `FC1-10-EMS05-539-01-DD` |
| | **500-pack** | `FC2-10-EMS05-537-01-DD` | `FC2-10-EMS05-538-01-DD` | `FC2-10-EMS05-539-01-DD` |
| | **2000-pack** | `FC3-10-EMS05-537-01-DD` | `FC3-10-EMS05-538-01-DD` | `FC3-10-EMS05-539-01-DD` |
| | **10000-pack** | `FC4-10-EMS05-537-01-DD` | `FC4-10-EMS05-538-01-DD` | `FC4-10-EMS05-539-01-DD` |

#### FortiClient 數位鑑識服務搭配 SOCaaS 需求：
使用 FortiClient 數位鑑識服務必須搭配 **FortiAnalyzer 地端設備** 或 **FortiAnalyzer Cloud** 將日誌轉發至 SOCaaS。請務必確保在 FortiAnalyzer Cloud 加購充足的日誌儲存空間，並檢查地端設備有足夠的日誌容量。

---

### (3) 訂單生命週期實例操作指南 (Order Lifecycle Examples)

* **情境一：新訂單 (New Order)**
  * **需求**：採購 500 台 ZTNA 端點設備授權。
  * **下單方式**：直接採購 1 組 500-pack：
    * `FC2-10-EMS05-428-01-12`（以 1 年期為例）
* **情境二：擴充增購端點 (Add More Endpoints)**
  * **需求**：現有環境增購 50 台 ZTNA 端點。
  * **下單方式**：直接增購 2 組 25-pack：
    * `FC1-10-EMS05-428-01-12` x2
* **情境三：全數續約 (Renew All Endpoints)**
  * **需求**：原有 500 台加增購 50 台，共 550 台 ZTNA 進行續約。
  * **下單方式**：於首筆合約到期時，使用 **Co-term（到期日對齊工具）**，將所有合約統一至相同結束日：
    * `FC1Z-15-EMS05-428-02-00` (x2)
    * `FC2Z-15-EMS05-428-02-00` (x1)
* **情境四：功能版本升級 (Upgrade Endpoints)**
  * **需求**：將全部 550 台 ZTNA 升級至更高階的 EPP/ATP 功能。
  * **下單方式**：使用 Co-term 工具將現行端點補差額升級至當前合約到期日，之後再按照標準流程續約：
    * `FC1Z-15-EMS05-429-02-00` (x2)
    * `FC2Z-15-EMS05-429-02-00` (x1)

---

## 4. FortiCare 最佳實踐諮詢服務 (FortiCare Best Practices, BPS)

FortiCare BPS 為企業提供原廠產品專家的預約諮詢，涵蓋架構設計、版本升級路線規劃與 EMS 遷移技術支援。

| 附加服務 (Additional Services) | 涵蓋端點規模 (FortiClient/EMS Services) | 訂購料號 (SKU License) |
| :--- | :--- | :--- |
| **FortiCare 最佳實踐諮詢服務 (BPS Consultation Service)** | 25 ~ 999 台端點 | `FC1-10-FCBPS-310-02-DD` |
| | 1000 ~ 9999 台端點 | `FC2-10-FCBPS-310-02-DD` |
| | 10000+ 台端點 | `FC5-10-FCBPS-310-02-DD` |

### 相關專案注意事項：
* **SASE 方案**：FortiSASE 具備專用擴充 SKU，詳細規範請參閱《FortiSASE 訂購指南》。
* **Chromebook 支援**：Chromebook 專屬版本請參考官方 Datasheet。

---

## 5. 升級路徑矩陣 (Upgrade Matrix)

### 升級原則規範：
1. **嚴禁跨架構直升**：FortiClient **不支援**地端（On-Premise）與雲端（Cloud）SKU 之間的直接升級轉移。若需切換，必須購買全新架構 SKU 並重新建立對應的 EMS 實例（可由 BPS 團隊協助遷移）。
2. **Chromebook 獨立運作**：Chromebook 為獨立架構，不支援升級至其他版本，亦不支援其他版本升級至 Chromebook。
3. **同架構內部升級**：在純雲端（Cloud）或純地端（On-Premise）環境內，可透過 Co-term 工具升級。

### (1) FortiClient 雲端授權升級矩陣 (Cloud Licenses)

| 原有方案 (Upgrade From) | 可升級至：ZTNA/VPN | 可升級至：EPP/ATP | 可升級至：Managed Client | 可升級至：SASE (Agent-based)* | 可升級至：SASE (Agentless)* | 可升級至：Chromebook | 可升級至：Managed + Forensics |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ZTNA / VPN** | 現有方案 | 可升級 | 可升級 | 可升級 | 可升級 | 不支援 | 可升級 |
| **EPP / ATP** | 不支援 | 現有方案 | 可升級 | 可升級 | 可升級 | 不支援 | 可升級 |
| **Managed Client (代管)** | 不支援 | 不支援 | 現有方案 | 不支援 | 不支援 | 不支援 | 可升級 |
| **Chromebook** | 不支援 | 不支援 | 不支援 | 不支援 | 不支援 | 現有方案 | 不支援 |

### (2) FortiClient 地端內部部署授權升級矩陣 (On-Premise)

| 原有方案 (Upgrade From) | 可升級至：ZTNA/VPN | 可升級至：EPP/ATP | 可升級至：ZTNA + Forensics | 可升級至：EPP/ATP + Forensics | 可升級至：Chromebook |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **ZTNA / VPN** | 現有方案 | 可升級 | 可升級 | 可升級 | 不支援 |
| **EPP / ATP** | 不支援 | 現有方案 | 不支援 | 可升級 | 不支援 |
| **Chromebook** | 不支援 | 不支援 | 不支援 | 不支援 | 現有方案 |

---

## 6. 獨立版 FortiClient (Standalone / User-based)

**FortiClient Standalone（DIY 獨立版）**為非集中託管方案，專為**不需要透過 EMS 集中管理**的中小型部署所設計。雖然不含 EMS，但其整合了 **FortiIdentity Cloud** 以達成使用者身分集中認證與每使用者（Per-User）授權驗證。

### 功能清單 (VPN / Remote Access Tier)：
* ✔ IPsec VPN 連線
* ✔ 單一登入行動代理 (Single Sign On Mobility Agent)
* ✔ FortiPAM 代理支援
* ✔ 整合 FortiIdentity Cloud 使用者身分管理
* ✔ 整合 FortiToken 多因子驗證 (MFA)
* ✔ 電子郵件支援服務 (Email Based Support)

### 訂購資訊：依使用者授權 (User-based)
* 最低起訂量 (MOQ)：**50 位使用者**。

| 解決方案 (Solution) | 授權單位 (SKU License) | VPN 料號 |
| :--- | :--- | :--- |
| **Standalone (DIY)** | 50+ (最低起訂量 50) | `FC1-10-FCTST-1284-02-DD (MOQ 50)` |

*(補充：亦可透過 FortiCloud Marketplace 使用 FortiPoints 點數採購，該管道起訂量為 5 個使用者)*

---

## 7. 原廠教育訓練與認證 (Training & Certification)

### FCP - FortiClient EMS 系統管理員訓練與認證
學員將深入學習如何操作 FortiClient EMS 各項管理功能、佈署配置端點軟體、整合 FortiClient EMS Security Fabric 安全織網、設定零信任網路存取 (ZTNA) 代理與端點防護機制。

* **課程詳細資訊**：  
  https://training.fortinet.com/local/staticpage/view.php?page=library_forticlient-ems-administrator
* **採購與開班方式**：  
  https://training.fortinet.com/local/staticpage/view.php?page=purchasing_process

---

## 8. 常見問題集 (Frequently Asked Questions)

#### Q1：什麼是 BPS？為什麼新專案都強烈建議納入？
**答**：BPS（Best Practice Service）可讓客戶隨時預約原廠產品專家，諮詢範圍包括解決方案最佳部署架構、最佳產品升級路徑建議、授權升級指引，以及低資料遺失、對終端使用者完全無感的 EMS 遷移技術協助。強烈建議在每一筆新客戶專案中加入 BPS，以確保上線及日後維運順暢。

#### Q2：最簡單的下單方式是什麼？
**答**：提供 1 到 5 年期的設備數量包。後續增購、續約及升級請參考第 3 節的生命週期操作實例。

#### Q3：FortiClient 是依使用者（Per-User）還是依設備（Per-Device）授權？
**答**：無論是地端內部部署的 FortiClient EMS 還是雲端 FortiClient Cloud，**皆全面採「依設備 / 端點 (Per-device / Endpoint)」計算授權**。（僅 Standalone DIY 版採依使用者計算）。

#### Q4：原本第一、二頁的 SASE 選項去哪了？
**答**：所有 SASE 選項均完整保留。Fortinet 已將 SASE 相關內容整併至獨立的《FortiSASE 訂購指南》，並支援將 FortiClient 升級為 FortiSASE。

#### Q5：如何從現有 FortiClient 授權升級到更高階授權？
**答**：可透過原廠 Co-term（到期日對齊工具）計算差額升級。**請注意：不支援地端 EMS 與雲端 Cloud EMS 之間的直接升級切換。**

#### Q6：EMS 端點管理伺服器有哪些部署選項？
**答**：
1. **地端或公有雲虛擬機**：可安裝於 Linux 伺服器（7.4 版）或 Windows 伺服器（7.2 及更早版本）。
2. **SaaS 服務**：直接採用原廠代管的 FortiClient Cloud 服務。

#### Q7：什麼是 FortiClient Cloud？
**答**：FortiClient Cloud 是由 Fortinet 原廠直接代管維運的 EMS 實例，企業無須自行建置、維護與修補地端 Windows/Linux 伺服器。

#### Q8：FortiClient Cloud 最多可管理多少台端點？
**答**：單一 FortiClient Cloud 實例最高可集中管理高達 **250,000 台端點**。

#### Q9：什麼是 ZTNA？
**答**：ZTNA 指的是 FortiOS 與 FortiClient 內建以反向代理（Proxy-based）為核心的零信任網路存取功能，包含端點設備安全狀態檢查（Posture Checks）、數位憑證生命週期管理，以及安全加密連線至 FortiGate 後方的受信任企業應用系統。

#### Q10：我之前購買的是 EMS01 / EMS03 舊料號，能否直接升級至新的 EMS04 / EMS05 料號？
**答**：由於產品架構與功能有所調整，**無法直接升級**。客戶應於合約到期續約時採購全新 SKU 料號。若以往是使用舊料號的地端部署，建議順勢直接轉換遷移至雲端 FortiClient Cloud 方案。

#### Q11：使用 FortiClient Cloud 是否強制需要 FortiCloud Premium 高級訂閱？
**答**：**不需要**。FortiClient Cloud 不強制綁定 FortiCloud Premium 訂閱。

#### Q12：同一台 EMS 伺服器能否同時混合使用不同的授權類型（如 VPN/ZTNA 與 EPP/ATP 混合）？
**答**：技術上可以支援。

#### Q13：如果 VPN/ZTNA 與 EPP/ATP 的授權到期日不同，同一台 EMS 能否支援混合？
**答**：強烈建議客戶**使用單一授權類型**，盡量避免在同一台 EMS 上混用不同類型與到期日的授權，以免造成授權管理與派送複雜度。

#### Q14：什麼是 FortiClient 數位鑑識分析服務 (Forensics Service)？
**答**：此服務提供遠端端點數位鑑識分析，協助企業應對網路資安事件並快速復原。在每一次鑑識專案中，FortiGuard Labs 原廠資安專家會遠端協助數位證據的收集、分析鑑定與呈現，並產出最終鑑識調查報告。支援 FortiClient Cloud 以及 7.2.2 版以上之地端 EMS。

#### Q15：什麼是 FortiEndpoint？
**答**：FortiEndpoint 是以 FortiClient 為核心的統一端點安全平台，提供單一代理程式 (Agent)、單一授權與單一管理後台，全面融合了安全連線（VPN / ZTNA）與 EPP、EDR、XDR 等全方位威脅偵測回應能力。詳細資訊請參閱《FortiEndpoint 訂購指南》。

---

## 9. 導入與上線服務 (Onboarding)

企業在建置初期與端點設備佈署上線時，可依據內部 IT 能量選擇下列四種模式：

1. **自主手動導入 (Manual / DIY)**：原廠提供完整的官方文件、教學影片、開源工具庫與各類技術資源。
2. **最佳實踐顧問諮詢 (FortiCare BPS)**：採用年度訂閱制的 FortiCare BPS，由原廠專家全程提供建置部屬、架構整合與版本升級遷移的顧問指引，且深度整合於 FortiCare 支援體系。
3. **原廠端點專家代管 (Managed FortiClient)**：直接購買 Managed FortiClient 方案，軟體初始環境設定、安全設定與設備上線皆直接由 Fortinet 原廠專家開箱代管。
4. **專案專業建置服務 (Professional Service, PS)**：對於要求嚴格合約服務等級協定（SLA）的大型或客製化建置專案，PS 專業顧問服務是最高品質的交付選項。

---

### 智慧財產權與法律聲明
*Copyright © 2026 Fortinet, Inc. All rights reserved. Fortinet®、FortiGate®、FortiCare®、FortiGuard® 等標誌均為 Fortinet, Inc. 之註冊商標。文中所載效能及其他數據指標均為理想實驗室環境下測試所得，實際效能可能受網路變數及環境影響。Fortinet 保留隨時修改、更新或修訂本刊物之權利，恕不另行通知。最新資訊請以官方網站公佈為準。*  
*官方網站：[www.fortinet.com](https://www.fortinet.com)*
