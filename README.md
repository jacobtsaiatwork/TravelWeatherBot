# 晨間與傍晚通勤天氣預警秘書 (Commute & Weather Brief Assistant)

晨間與傍晚通勤預報秘書專為上班族與學生量身打造，在每個工作日出門前（07:40 AM）與下班前（17:40 PM）主動將當季通勤時段的天氣資訊、降雨機率、動態穿搭建議、出門帶傘提醒、大眾運輸（捷運、台鐵）即時路況、YouBike 2.0 即時空車、Google 日曆首要行程、焦點快訊與 Gemini AI 溫暖問候，以高質感的 **LINE Flex Message 圖文卡片** 推播至手機 LINE，讓上下班通勤隨時胸有成竹。

---

## 🌟 核心特色

1. **視覺化排版 (LINE Flex Message 圖文卡片 UI)**：
   - 全面告別生硬的長串文字，採用高質感 Bubble 卡片排版。
   - 晨間出門（活力天藍風格）與傍晚下班（溫馨夕陽橙風格）雙色調自動切換。
   - 遇到雨天（降雨機率 $\ge 50\%$）自動額外附加中央氣象署最新即時雷達回波圖。
2. **中央氣象署 (CWA) 官方 API 與雷達回波圖**：
   - 整合 CWA Open Data API (`F-C0032-001`) 36 小時精細天氣預報。
   - 支援全台 22 縣市查詢與「台北市」異體字正體自動正規化。
   - 降雨機率過高時自動發送最新雷達回波圖資（每 10 分鐘即時更新）。
3. **交通部 TDX 大眾運輸即時事件與 YouBike 2.0 查詢**：
   - 整合 TDX OAuth 2.0 官方 API，涵蓋北捷、新北捷、桃捷、中捷、高捷與台鐵即時事故通報。
   - 支援 YouBike 2.0 即時站點可借車輛（含電輔車數量）與可還車位數查詢。
   - 內建 OAuth Token 快取與請求頻率間隔保護，避免觸發 429 限流。
4. **Google 日曆多信箱聚合與行程提醒**：
   - 支援同時訂閱多個 Google 日曆（例如工作與個人私人 iCal 網址）。
   - 挑選今日最早會議並計算當日行程總數。
5. **Google News 即時焦點新聞快訊**：
   - 晨間自動擷取 Google News 即時頭條新聞 Top 3。
6. **Gemini AI 個人化生活問候與激勵短語**：
   - 串接 Google Gemini 模型，結合當日天氣、降雨與行程動態生成 30~45 字溫暖親切短語。
   - 未設定 API Key 時內建精美規則庫優雅降級，永不中斷推播。
7. **全自動雲端排程 (GitHub Actions 免開電腦)**：
   - 設定平日早晨 07:40 AM (UTC 23:40) 與傍晚 17:40 PM (UTC 09:40) 自動定時推播。
   - 本地電腦無需保持開機，雲端環境純靜態運作。

---

## 📁 專案架構

```text
├── .github/workflows/
│   └── daily_brief.yml        # GitHub Actions 自動排程設定 (早晚雙定時)
├── weather_service.py         # 氣象署 CWA API、時段預報、穿搭建議
├── transit_service.py         # 交通部 TDX 捷運/台鐵即時事件通報
├── calendar_service.py        # Google 日曆多信箱聚合、首場會議提醒
├── smart_assistant_service.py # 焦點新聞、YouBike 2.0、雷達回波圖、Gemini 悄悄話
├── flex_template.py           # LINE Flex Message 視覺化圖文卡片組裝器
├── commute_brief.py           # 執行入口、CLI 參數解析與 LINE 推播
├── test_weather.py            # 氣象模組單元測試
├── test_transit.py            # 交通模組單元測試
├── test_calendar.py           # 日曆模組單元測試
├── test_smart_assistant.py    # 智慧秘書模組單元測試
├── test_flex_template.py      # Flex 卡片排版單元測試
├── requirements.txt          # Python 依賴清單
├── .env.example              # 環境變數設定範本
└── README.md                 # 專案說明文件
```

---

## 🚀 快速開始

### 1. 安裝環境與套件

```powershell
pip install -r requirements.txt
```

### 2. 設定環境變數

複製 `.env.example` 為 `.env`，並填入您的各項 API 金鑰：

```env
USER_NAME=通勤夥伴
LOCATION=臺北市
CWA_API_KEY=你的中央氣象署授權碼
TDX_CLIENT_ID=你的TDX_Client_ID
TDX_CLIENT_SECRET=你的TDX_Client_Secret
LINE_CHANNEL_ACCESS_TOKEN=你的LINE_Channel_Access_Token
LINE_USER_ID=你的LINE個人_User_ID
GOOGLE_CALENDAR_ICAL_URLS=工作:https://.../basic.ics,個人:https://.../basic.ics
GEMINI_API_KEY=你的Gemini_API_Key
YOUBIKE_STATIONS=捷運科技大樓站,捷運台北車站
```

### 3. 本地手動執行測試

```powershell
# 測試晨間模式 (強制執行忽略週末)
python commute_brief.py --force --mode morning

# 測試傍晚下班模式
python commute_brief.py --force --mode evening

# 執行所有單元測試
python -m unittest discover -s . -p "test_*.py"
```

### 4. 雲端 GitHub Actions 免開電腦自動推播

將專案推送到 GitHub，並至 Repository 的 **Settings -> Secrets and variables -> Actions** 中新增 Secret `DOTENV`，將您的完整 `.env` 內容貼入即可。
排程將於平日週一至週五：
- ☀️ 晨間出門：台灣時間 07:40 AM
- 🌆 傍晚下班：台灣時間 17:40 PM
自動在 GitHub 雲端 runner 執行並推播至您的 LINE！
