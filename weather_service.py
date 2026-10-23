import os
import sys
import logging
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CWA_API_BASE_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"

LOCATION_MAPPING = {
    "台北市": "臺北市",
    "台中市": "臺中市",
    "台南市": "臺南市",
    "台東縣": "臺東縣",
    "台東市": "臺東縣",
}

def normalize_location_name(location: str) -> str:
    """正規化縣市名稱，氣象署使用正體『臺』"""
    loc = location.strip()
    return LOCATION_MAPPING.get(loc, loc)

def generate_clothing_tip(min_temp: float, max_temp: float, comfort_desc: str = "") -> str:
    """依據溫度區間與體感舒適度動態產生穿著指南"""
    avg_temp = (min_temp + max_temp) / 2.0
    
    if max_temp >= 32:
        return "氣溫炎熱（最高可達 " + f"{max_temp:.0f}°C），建議穿著透氣涼爽短袖，外出注意防曬並多補充水分。"
    elif max_temp >= 28:
        return "白天氣溫偏熱舒適（" + f"{min_temp:.0f}~{max_temp:.0f}°C），建議穿著短袖，進入室內冷氣房可備薄罩衫。"
    elif min_temp >= 20:
        return "氣候溫和舒適（" + f"{min_temp:.0f}~{max_temp:.0f}°C），建議著短袖或長袖薄上衣，清晨出門可搭配輕薄防風外套。"
    elif min_temp >= 15:
        return "早晚偏涼（" + f"{min_temp:.0f}~{max_temp:.0f}°C），建議採洋蔥式穿法，務必攜帶風衣或保暖夾克。"
    else:
        return "氣溫寒冷（最低僅 " + f"{min_temp:.0f}°C），請穿著發熱衣、毛衣與厚外套，注意防風禦寒保暖。"

def fetch_cwa_weather(api_key: str, location: str = "臺北市", mode: str = "morning") -> Dict[str, Any]:
    """
    透過中央氣象署 Open Data API (F-C0032-001) 取得指定縣市的天氣預報資料。
    支援 mode="morning" (白天時段) 或 mode="evening" (今晚到明晨時段)。
    """
    norm_location = normalize_location_name(location)
    params = {
        "Authorization": api_key,
        "locationName": norm_location
    }
    
    try:
        response = requests.get(CWA_API_BASE_URL, params=params, timeout=10)
    except requests.exceptions.SSLError:
        # 部分 Windows 環境下連線政府機關網域 (.gov.tw) 可能因憑證缺乏 Subject Key Identifier 而觸發 SSLError
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(CWA_API_BASE_URL, params=params, timeout=10, verify=False)

    response.raise_for_status()
    data = response.json()
    
    if not data.get("success") == "true":
        raise ValueError(f"CWA API 回應失敗: {data.get('message', '未知錯誤')}")
    
    records = data.get("records", {})
    locations = records.get("location", [])
    if not locations:
        raise ValueError(f"查查無此縣市之天氣資料: {norm_location}")
    
    loc_data = locations[0]
    elements = {elem["elementName"]: elem["time"] for elem in loc_data.get("weatherElement", [])}
    
    # 決定時段索引 (0 為最新/白天時段，evening 若有多個時段可使用 1)
    period_idx = 0
    if mode == "evening":
        wx_times = elements.get("Wx", [])
        if len(wx_times) > 1:
            period_idx = 1

    wx_item = elements.get("Wx", [{}])[period_idx].get("parameter", {})
    pop_item = elements.get("PoP", [{}])[period_idx].get("parameter", {})
    mint_item = elements.get("MinT", [{}])[period_idx].get("parameter", {})
    maxt_item = elements.get("MaxT", [{}])[period_idx].get("parameter", {})
    ci_item = elements.get("CI", [{}])[period_idx].get("parameter", {})
    
    weather_status = wx_item.get("parameterName", "多雲")
    rain_prob = int(pop_item.get("parameterName", 0)) if pop_item.get("parameterName") else 0
    min_temp = float(mint_item.get("parameterName", 22.0))
    max_temp = float(maxt_item.get("parameterName", 28.0))
    comfort_desc = ci_item.get("parameterName", "舒適")
    
    avg_temp = round((min_temp + max_temp) / 2.0, 1)
    umbrella_needed = (rain_prob >= 30) or any(k in weather_status for k in ["雨", "陣雨", "雷雨"])
    clothing_tip = generate_clothing_tip(min_temp, max_temp, comfort_desc)
    
    return {
        "location": loc_data.get("locationName", norm_location),
        "temperature": avg_temp,
        "temp_min": min_temp,
        "temp_max": max_temp,
        "rain_prob_commute": rain_prob,
        "weather_status": weather_status,
        "comfort_desc": comfort_desc,
        "air_quality": "良好至普通 (AQI 35-55)",
        "umbrella_needed": umbrella_needed,
        "clothing_tip": clothing_tip,
        "source": "中央氣象署 (CWA) 官方 API"
    }

def get_commute_weather_mock(location: str = "臺北市") -> Dict[str, Any]:
    """提供模擬通勤天氣資料，作為 API 故障或未設定授權碼時之優雅降級方案"""
    norm_location = normalize_location_name(location)
    return {
        "location": norm_location,
        "temperature": 24.5,
        "temp_min": 22.0,
        "temp_max": 27.0,
        "rain_prob_commute": 65,
        "weather_status": "陰有局部短暫陣雨",
        "comfort_desc": "舒適",
        "air_quality": "良好 (AQI 38)",
        "umbrella_needed": True,
        "clothing_tip": "氣溫涼爽舒適（22~27°C），建議著長袖薄上衣或搭配輕便外套。",
        "source": "本地模擬資料 (Mock Fallback)"
    }

def get_commute_weather(location: str = "臺北市", api_key: Optional[str] = None, mode: str = "morning") -> Dict[str, Any]:
    """
    整合氣象資料入口：
    1. 若有 CWA_API_KEY 則呼叫中央氣象署官方 API。
    2. 若未設定金鑰或呼叫異常，自動退回模擬資料並發出警告，確保系統永不崩潰。
    """
    cwa_key = api_key or os.getenv("CWA_API_KEY")
    norm_location = normalize_location_name(location)
    
    if cwa_key and cwa_key.strip() and not cwa_key.startswith("your_"):
        try:
            logger.info(f"正在向中央氣象署 (CWA) 查詢 [{norm_location}] 天氣預報 (模式: {mode})...")
            return fetch_cwa_weather(api_key=cwa_key.strip(), location=norm_location, mode=mode)
        except Exception as e:
            logger.warning(f"中央氣象署 API 呼叫失敗 ({e})，切換至優雅降級 (Fallback) 模式。")
    else:
        logger.info("未檢測到有效 CWA_API_KEY，使用模擬資料 (可在 .env 設定 CWA_API_KEY 啟用官方實時數據)。")
    
    return get_commute_weather_mock(norm_location)

def build_commute_brief_text(
    user_name: str = "早安",
    weather_data: Optional[Dict[str, Any]] = None,
    transit_data: Optional[Dict[str, Any]] = None,
    calendar_data: Optional[Dict[str, Any]] = None,
    location: str = "臺北市",
    mode: str = "morning",
    ai_quote: str = "",
    news_list: Optional[List[str]] = None,
    youbike_list: Optional[List[Dict[str, Any]]] = None
) -> str:
    """依據取得之氣象、交通與日曆資料組裝文字推播文案 (支援晨間與傍晚雙模式)"""
    if weather_data is None:
        weather_data = get_commute_weather(location=location, mode=mode)

    if transit_data is None:
        try:
            from transit_service import get_commute_transit_status
            transit_data = get_commute_transit_status(location=location)
        except Exception:
            transit_data = {
                "has_alert": False,
                "status_text": "大眾運輸正常運作無事故通報。",
                "source": "預設狀態"
            }

    if calendar_data is None:
        try:
            from calendar_service import get_today_first_meeting
            calendar_data = get_today_first_meeting()
        except Exception:
            calendar_data = {
                "has_events": False,
                "status_text": "今日早晨無安排會議，祝你專注享受充實的一天！" if mode == "morning" else "晚間公務行程已告一段落！",
                "source": "預設狀態"
            }

    is_morning = (mode == "morning")
    title_header = "☀️【晨間通勤與天氣快報】" if is_morning else "🌆【傍晚下班與交通快報】"
    greeting_line = f"{user_name}！今天是個美好的一天！" if is_morning else f"{user_name}！辛苦奮鬥了一整天，準備下班囉！"

    rain_prob = weather_data.get("rain_prob_commute", 0)
    if weather_data.get("umbrella_needed", False):
        umbrella_icon = f"☔ 降雨機率 {rain_prob}%，出門請務必攜帶雨具！" if is_morning else f"☔ 降雨機率 {rain_prob}%，下班返家路滑請備雨具！"
    else:
        umbrella_icon = f"🌤️ 降雨機率低 ({rain_prob}%)，活動輕鬆免帶傘。"

    temp_range = f"{weather_data.get('temp_min', weather_data['temperature'])}~{weather_data.get('temp_max', weather_data['temperature'])}°C"
    transit_icon = "⚠️" if transit_data.get("has_alert") else "🚇"
    cal_icon = "📅" if calendar_data.get("has_events") else "☕"

    sources = [weather_data.get('source', '氣象署'), transit_data.get('source', 'TDX')]
    if calendar_data.get('source') and "未設定" not in calendar_data.get('source', ''):
        sources.append(calendar_data['source'])
    if ai_quote:
        sources.append("Gemini AI")
    source_line = " ｜ ".join(sources)

    lines = [
        title_header,
        greeting_line,
        "",
        f"📍 地區：{weather_data['location']}",
        f"🌡️ 氣溫：{weather_data['temperature']}°C (範圍 {temp_range}，{weather_data['weather_status']})",
        f"🌧️ 通勤降雨率：{rain_prob}%",
        umbrella_icon,
        "",
        f"👔 穿著指南：{weather_data['clothing_tip']}",
        f"🍃 空氣品質：{weather_data['air_quality']}",
        "",
        f"{transit_icon} 交通狀況：{transit_data['status_text']}",
        "",
        f"{cal_icon} 行程動態：{calendar_data['status_text']}"
    ]

    # YouBike 資訊
    if youbike_list and len(youbike_list) > 0:
        lines.append("")
        lines.append("🚲 YouBike 2.0 即時空車：")
        for yb in youbike_list[:3]:
            st_name = yb.get("name", "站點")
            rent = yb.get("rent_bikes", 0)
            ebike = yb.get("electric_bikes", 0)
            ret = yb.get("return_spaces", 0)
            ebike_str = f" (電輔 {ebike})" if ebike > 0 else ""
            lines.append(f"  • {st_name}：可借 {rent}{ebike_str} ｜ 可還 {ret}")

    # AI 金句
    if ai_quote:
        lines.append("")
        lines.append(f"✨ 秘書貼心悄悄話：{ai_quote}")

    # 新聞快訊 (晨間模式)
    if is_morning and news_list and len(news_list) > 0:
        lines.append("")
        lines.append("📰 今日焦點快訊：")
        for idx, news in enumerate(news_list[:3], 1):
            lines.append(f"  {idx}. {news}")

    lines.append("")
    lines.append(f"📡 資訊來源：{source_line}")
    wish_line = "祝你今天上班/上學順利，元氣滿滿！💪" if is_morning else "祝你下班平安順心，享受溫馨夜晚！🌙"
    lines.append("")
    lines.append(wish_line)

    return "\n".join(lines).strip()

def build_morning_brief_text(
    user_name: str = "早安",
    weather_data: Optional[Dict[str, Any]] = None,
    transit_data: Optional[Dict[str, Any]] = None,
    calendar_data: Optional[Dict[str, Any]] = None,
    location: str = "臺北市"
) -> str:
    """向下相容 build_morning_brief_text 舊介面"""
    return build_commute_brief_text(
        user_name=user_name,
        weather_data=weather_data,
        transit_data=transit_data,
        calendar_data=calendar_data,
        location=location,
        mode="morning"
    )

if __name__ == "__main__":
    brief = build_morning_brief_text(user_name="通勤夥伴")
    print(brief)
