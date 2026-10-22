import os
import sys
import time
import logging
import requests
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# -------------------------------------------------------------
# 1. 焦點新聞模組 (Google News TW 即時焦點 RSS)
# -------------------------------------------------------------
def fetch_top_news(limit: int = 3) -> List[str]:
    """
    自 Google News TW RSS 獲取今日前 N 則焦點新聞標題。
    自動過濾媒體出處標記，提供乾淨易讀的標題。
    """
    url = "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            items = root.findall(".//item")[:limit]
            news_titles = []
            for item in items:
                title_elem = item.find("title")
                if title_elem is not None and title_elem.text:
                    # 移除新聞最後面的 ' - 媒體名稱'
                    clean_title = title_elem.text.rsplit(" - ", 1)[0].strip()
                    news_titles.append(clean_title)
            return news_titles
    except Exception as e:
        logger.warning(f"抓取即時焦點新聞失敗: {e}")
    return []

# -------------------------------------------------------------
# 2. YouBike 2.0 即時空車查詢 (TDX API)
# -------------------------------------------------------------
def fetch_youbike_station_status(
    station_keywords: Optional[List[str]] = None,
    city: str = "Taipei",
    token: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    查詢指定站點之 YouBike 2.0 即時可借車輛數與可還車位數。
    若未指定 station_keywords，則嘗試讀取環境變數 YOUBIKE_STATIONS。
    """
    if station_keywords is None:
        raw_env = os.getenv("YOUBIKE_STATIONS", "").strip()
        if not raw_env:
            return []
        station_keywords = [s.strip() for s in raw_env.replace(";", ",").split(",") if s.strip()]

    if not station_keywords:
        return []

    # 取得 TDX Token
    tdx_token = token
    if not tdx_token:
        try:
            from transit_service import TDXClient
            client = TDXClient()
            tdx_token = client.get_token()
        except Exception as e:
            logger.warning(f"獲取 TDX Token 失敗: {e}")
            return []

    if not tdx_token:
        return []

    headers = {
        "authorization": f"Bearer {tdx_token}",
        "Accept": "application/json"
    }

    results = []
    try:
        # 1. 查詢站點基本資料以取得 StationUID 與站點名稱
        station_url = f"https://tdx.transportdata.tw/api/basic/v2/Bike/Station/City/{city}"
        resp_stations = requests.get(station_url, headers=headers, params={"$format": "JSON"}, timeout=10)
        if resp_stations.status_code != 200:
            return []

        all_stations = resp_stations.json()
        target_stations = {}
        for kw in station_keywords:
            for s in all_stations:
                st_name = s.get("StationName", {}).get("Zh_tw", "")
                if kw in st_name:
                    uid = s.get("StationUID")
                    if uid and uid not in target_stations:
                        target_stations[uid] = st_name.replace("YouBike2.0_", "")
                    if len(target_stations) >= len(station_keywords):
                        break

        if not target_stations:
            return []

        # 2. 查詢目標站點的即時借還車狀態 (加入 0.3s 延遲避免 TDX 429 限流)
        time.sleep(0.3)
        avail_url = f"https://tdx.transportdata.tw/api/basic/v2/Bike/Availability/City/{city}"
        resp_avail = requests.get(avail_url, headers=headers, params={"$format": "JSON"}, timeout=10)
        if resp_avail.status_code != 200:
            return []

        avail_data = resp_avail.json()
        for item in avail_data:
            uid = item.get("StationUID")
            if uid in target_stations:
                st_name = target_stations[uid]
                rent_bikes = item.get("AvailableRentBikes", 0)
                return_spaces = item.get("AvailableReturnBikes", 0)
                detail = item.get("AvailableRentBikesDetail", {})
                e_bikes = detail.get("ElectricBikes", 0)
                results.append({
                    "station_uid": uid,
                    "name": st_name,
                    "rent_bikes": rent_bikes,
                    "electric_bikes": e_bikes,
                    "return_spaces": return_spaces
                })

    except Exception as e:
        logger.warning(f"查詢 YouBike 站點狀態失敗: {e}")

    return results

# -------------------------------------------------------------
# 3. 雷達回波圖 (中央氣象署最新公開圖資網址)
# -------------------------------------------------------------
def get_cwa_radar_image_url() -> str:
    """提供中央氣象署官方最新即時雷達回波圖 (每 10 分鐘更新之高解析度圖資)"""
    return "https://www.cwa.gov.tw/Data/radar/CV1_3600.png"

# -------------------------------------------------------------
# 4. Gemini AI 早安/傍晚溫暖金句與生活短語
# -------------------------------------------------------------
def generate_gemini_brief_quote(
    weather_desc: str,
    temp_range: str,
    rain_prob: int,
    meeting_summary: str,
    mode: str = "morning",
    gemini_api_key: Optional[str] = None
) -> str:
    """
    使用 Google Gemini 模型生成 30~45 字以內的貼心生活問候短語。
    若 API 失敗或未提供金鑰，則以內建規則庫優雅降級。
    """
    if gemini_api_key is not None:
        api_key = gemini_api_key
    else:
        api_key = os.getenv("GEMINI_API_KEY", "")

    # 規則降級庫
    if not api_key or api_key.startswith("your_"):
        if mode == "evening":
            if rain_prob >= 50:
                return "傍晚下班雨天路滑，通勤路上請放慢腳步、注意安全，回家好好放鬆休息！🍲"
            else:
                return "辛苦奮鬥了一整天！把工作的繁瑣放下，今晚給自己一個溫馨悠閒的個人時光！🌙"
        else:
            if rain_prob >= 50:
                return "出門雨天路滑，別忘了攜帶雨具，放慢腳步喝杯咖啡，展開充實的一天！☕"
            elif "會議" in meeting_summary or "報告" in meeting_summary:
                return "今天有重要行程與會議，深呼吸保持自信，展現你最專業耀眼的一面！💪"
            else:
                return "晨光熹微，今天是充滿機會的一天，願你元氣滿滿、事事稱心如意！☀️"

    # 呼叫 Gemini 3.8 / 2.5 API
    for model_name in ["gemini-3.8-flash", "gemini-2.5-flash"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key.strip()}"
            time_label = "晨間" if mode == "morning" else "傍晚下班"
            prompt = f"""你是一位溫暖又貼心的私人生活秘書。請根據今日資訊寫一句約 30~45 字的{time_label}問候與激勵短語（繁體中文），語氣親切自然，包含適當 emoji：
- 今日天氣：{weather_desc}，氣溫 {temp_range}，降雨機率 {rain_prob}%
- 今日行程：{meeting_summary}
直接輸出這句話，不要有其他引言或前後標點引號。"""

            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(url, json=payload, timeout=8)
            if resp.status_code == 200:
                res_data = resp.json()
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        text = parts[0]["text"].strip().replace('"', '').replace('「', '').replace('」', '')
                        if text:
                            return text
        except Exception as e:
            logger.debug(f"Gemini API 呼叫嘗試失敗 ({model_name}): {e}")

    # Fallback to rule
    if mode == "evening":
        return "辛苦了一整天！下班路上注意安全，回家給自己一個溫馨放鬆的夜晚！🌙"
    return "晨光熹微，今天是充滿機會的一天，願你元氣滿滿、事事順遂！☀️"
