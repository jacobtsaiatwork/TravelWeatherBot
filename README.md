# 晨間通勤與天氣預警秘書 (Commute & Weather Brief Assistant)

晨間通勤與天氣預報秘書專為上班族與學生量身打造，在每個工作日早晨（07:40 AM）主動將當日通勤時段的天氣資訊、降雨機率、動態穿搭建議、出門帶傘提醒與大眾運輸（捷運、台鐵）即時路況推播至手機 LINE，讓出門不再手忙腳亂。

---

## 🌟 核心特色

1. **中央氣象署 (CWA) 官方 API 串接**：
   - 整合 CWA Open Data API (`F-C0032-001`) 36小時天氣預報。
   - 支援台灣全台 22 縣市查詢，並自動將「台北市」等異體字正規化為「臺北市」。
2. **交通部 TDX 大眾運輸即時事件串接**：
   - 整合交通部 TDX 運輸資料流通服務 OAuth 2.0 官方 API。
   - 涵蓋台北捷運、新北捷運、桃園捷運、台中捷運、高雄捷運與台鐵即時營運事件通報。
   - 內建 OAuth Token 本地快取與速率保護，避免頻繁發送重複憑證請求。
3. **智慧通勤與穿搭提醒**：
   - 提取通勤時段降雨機率（PoP），若 $\ge 30\%$ 或有雨現象自動標註攜帶雨具提醒。
   - 依據最高溫、最低溫與體感指數動態產生穿衣指南（涼爽、炎熱、防風、保暖等）。
4. **優雅降級 (Graceful Fallback)**：
   - 若尚未取得或未設定 CWA / TDX 金鑰，或網路連線異常，系統將自動無縫退回模擬模式，絕不發生當機中斷。
5. **工作日專屬與自動排程**：
   - 內建週末（週六/週日）自動跳過功能，不打擾假日休息。
   - 提供 `scheduler.ps1` PowerShell 腳本，一鍵將任務登錄至 Windows 工作排程器（Task Scheduler）。
6. **LINE 即時推播**：
   - 支援 LINE Messaging API 推播至個人帳號。
   - 開發/本機環境未設定 Token 時自動以格式化文字印於終端機，方便即時檢測。

---

## 📁 專案架構

```text
├── SPEC.md             # 專案規格書與 Roadmap
├── README.md           # 專案說明與操作指南
├── weather_service.py  # 氣象資料取得、CWA API 串接、穿搭建議與容錯降級模組
├── transit_service.py  # 交通部 TDX 捷運/台鐵即時通報、OAuth Token 快取模組
├── commute_brief.py    # 晨報組裝主程式、CLI 參數解析與 LINE 推播模組
├── test_weather.py     # 氣象模組單元測試套件
├── test_transit.py     # 交通模組單元測試套件
├── scheduler.ps1       # Windows 工作排程器註冊自動化腳本
├── requirements.txt    # Python 依賴清單
├── .env.example        # 環境變數設定範本
└── .gitignore          # Git 忽略設定
```

---

## 🚀 快速開始

### 1. 安裝環境與套件

```powershell
pip install -r requirements.txt
```

### 2. 設定環境變數

複製 `.env.example` 為 `.env`：

```powershell
Copy-Item .env.example .env
```

在 `.env` 中填寫設定（選填，若未填寫會以模擬資料在終端機運作）：

```env
USER_NAME=通勤夥伴
LOCATION=臺北市
CWA_API_KEY=你的中央氣象署授權碼
TDX_CLIENT_ID=你的TDX_Client_ID
TDX_CLIENT_SECRET=你的TDX_Client_Secret
LINE_CHANNEL_ACCESS_TOKEN=你的LINE_Channel_Access_Token
LINE_USER_ID=你的LINE個人_User_ID
```

### 3. 立即手動測試

```powershell
# 立即強制執行晨報（忽略週末限制）
python commute_brief.py --force

# 指定查詢特定縣市
python commute_brief.py --force --location 高雄市
```

### 4. 執行單元測試

```powershell
python test_weather.py
python test_transit.py
```

### 5. 註冊 Windows 工作排程器（平日 07:40 自動執行）

以 PowerShell 執行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scheduler.ps1
```

可在 Windows 工作排程器中看到名為 `CommuteWeatherBrief` 的任務。

---

## 🗺️ 開發進度與 Roadmap

- [x] **Phase 1: 天氣簡報產生與排程腳本**
- [x] **Phase 2: 串接中央氣象署 CWA 官方 API 授權碼**
- [x] **Phase 3: 串接交通部 TDX 捷運/台鐵即時事件 API**
- [ ] **Phase 4: 整合 Google Calendar 抓取今天第一個會議時間提醒**
