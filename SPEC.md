# 晨間通勤與天氣預警秘書 (Commute & Weather Brief Assistant) - 規格書

本專案供開發者與後續接續的 AI Assistant 掌握專案全貌、架構與開發進度。

* **起源對話**：[3f5143d8-ac7b-47ea-b95f-5df412357150](conversation://3f5143d8-ac7b-47ea-b95f-5df412357150)
* **當前狀態**：Phase 2 完成（中央氣象署 CWA API 串接、自動正規化、動態穿搭指南與優雅降級已上線）

---

## 1. 業務邏輯與需求目標
* **痛點**：早上起床時間緊湊，常出門後才發現下大雨沒帶傘、或者到了捷運/公車站才發現班次異常甚至停駛。一般的氣象 App 只會寫全天降雨機率，沒有針對「上班通勤時段（例如 08:00 ~ 09:00）」的精確預報。
* **目標功能**：
  1. **定時自動觸發**：每個工作日早上 07:40 自動啟動（避開假日與國定放假日）。
  2. **通勤時段精準氣象**：
     - 整合中央氣象署（CWA）Open Data API (F-C0032-001) 或公共開放資料。
     - 取得指定縣市的「氣溫區間、體感舒適度、通勤時段降雨機率、天氣現象」。
     - 判斷是否需要「帶摺疊傘、穿防風外套、洋蔥式穿搭或防曬涼爽短袖」。
     - 具備未配置 API Key 或網路異常時的優雅降級 (Fallback) 機制。
  3. **交通即時路況/大眾運輸異常通報**：檢查台北捷運/台鐵/主要幹道是否有事故或班次延誤 (Phase 3)。
  4. **主動推播**：將溫暖精簡晨報透過 LINE Messaging API 發送到手機，未配置時於終端機格式化呈現。

---

## 2. 系統架構與關鍵檔案
* **`SPEC.md`**：本規格書與架構指引。
* **`README.md`**：詳細部署、設定與使用說明。
* **`weather_service.py`**：氣象資料抓取與降雨機率分析模組，支援 CWA API (F-C0032-001) 與自動降級。
* **`commute_brief.py`**：主要執行腳本。負責組裝晨報內容、支援 CLI 參數 (`--force`, `--location`) 與 LINE 推播。
* **`transit_service.py`**：交通部 TDX 大眾運輸（北捷、新北捷、桃捷、中捷、高捷、台鐵）即時警訊查詢模組，具備 OAuth Token 本地快取與速率保護。
* **`test_transit.py`**：交通模組單元測試套件，涵蓋 Token 快取、正常狀態判定、異常警訊組織與無金鑰降級。
* **`test_weather.py`**：氣象單元測試套件，涵蓋 API 解析、穿著建議、縣市名稱正規化與 Fallback 機制。
* **`scheduler.ps1`**：Windows 排程器（Task Scheduler）自動安裝腳本（設定平日早上 07:40 執行）。
* **`requirements.txt`**：專案相依套件 (`requests`, `line-bot-sdk`, `python-dotenv`)。
* **`.env.example`**：環境變數設定範例。

---

## 3. 開發進度與 Roadmap
- [x] **Phase 1: 天氣簡報產生與排程腳本**（已完成）
- [x] **Phase 2: 串接中央氣象署 CWA 官方 API 授權碼**（已完成）
  - [x] 串接 CWA Open Data API (F-C0032-001)
  - [x] 縣市名稱正體字正規化轉換（例如「台北市」轉為「臺北市」）
  - [x] 動態穿搭與帶傘建議判斷
  - [x] 優雅降級容錯機制 (Fallback to Mock)
  - [x] 單元測試套件覆蓋 (test_weather.py)
- [x] **Phase 3: 串接交通部 TDX 捷運/台鐵即時事件 API**（已完成）
  - [x] OAuth 2.0 Client Credentials 授權與 Token 自動快取
  - [x] 台北捷運、新北捷運、桃園捷運、台中捷運、高雄捷運與台鐵即時營運通報
  - [x] 正常狀態自動過濾與異常事件警告摘要
  - [x] 單元測試套件覆蓋 (test_transit.py)
- [x] **Phase 4: 整合 Google Calendar 抓取今天第一個會議時間提醒**（已完成）
  - [x] 支援多信箱 iCal 私人網址（工作、個人等多日曆同步聚合）
  - [x] 自動過濾全天行程與定時會議，精準挑選今日最早會議提醒
  - [x] 跨信箱時間軸自動排序與今日總行程數統計
  - [x] 單元測試套件覆蓋 (test_calendar.py)
- [x] **Phase 5: 全方位智慧秘書升級（視覺化、雷達圖、新聞、YouBike、Gemini AI 與下班模式）**（已完成）
  - [x] LINE Flex Message 視覺化 Bubble 圖文卡片 UI（晨間活力藍 / 傍晚夕陽橙雙模式）
  - [x] 中央氣象署 (CWA) 最新即時雷達回波圖（高降雨率自動附加圖資）
  - [x] Google News 即時焦點快訊 Top 3
  - [x] 交通部 TDX YouBike 2.0 即時空車與可還車位查詢（支援電輔車資訊）
  - [x] Google Gemini AI 溫暖生活激勵短語（30~45 字客製化溫暖關懷，內建規則優雅降級）
  - [x] 傍晚下班推播模式（下班返家路況、夜間天氣預報與身心放鬆提醒）
  - [x] GitHub Actions 自動排程擴充（晨間 07:40 AM + 傍晚 17:40 PM 雙自動推播）
  - [x] 全套單元測試覆蓋 (test_smart_assistant.py, test_flex_template.py)

---

## 4. 未來規劃與整合備忘 (Future Integration Notes)
* **LINE 頻道整合備忘（與「投資小幫手」合併）**：
  - **背景**：使用者目前擁有另一組「投資小幫手」LINE 官方帳號。
  - **需求**：未來若使用者希望將通知集中於單一聊天室，可將本專案的通勤天氣推播與「投資小幫手」整合至同一個 LINE Bot，打造成專屬的全能生活與工作特助。
  - **執行方式**：只需將 GitHub Actions 的 `DOTENV` 中的 `LINE_CHANNEL_ACCESS_TOKEN` 與 `LINE_USER_ID` 替換為「投資小幫手」的金鑰即可，程式碼與排程核心完全相容、無需重寫。
