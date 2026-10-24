import os
import sys
import json
import argparse
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# 載入同目錄下的 .env
load_dotenv(Path(__file__).parent / ".env")

from weather_service import build_commute_brief_text, get_commute_weather
from transit_service import get_commute_transit_status
from calendar_service import get_today_first_meeting
from smart_assistant_service import (
    fetch_top_news,
    fetch_youbike_station_status,
    get_cwa_radar_image_url,
    generate_gemini_brief_quote
)
from flex_template import build_weather_commute_flex_message

def send_line_push_message(
    flex_bubble: Optional[Dict[str, Any]] = None,
    text_fallback: str = "",
    radar_image_url: Optional[str] = None,
    mode: str = "morning"
) -> bool:
    """
    透過 LINE Messaging API 發送高質感圖文卡片 (Flex Message) 與即時氣象雷達圖。
    若未設定 LINE 變數則輸出至 Console。
    若 Flex Message 或圖資傳送異常，會自動優雅降級為純文字訊息，確保服務不中斷。
    """
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")

    alt_text = "☀️ 晨間通勤與天氣快報" if mode == "morning" else "🌆 傍晚下班與交通快報"

    if not channel_access_token or not user_id or channel_access_token.startswith("your_") or user_id.startswith("your_"):
        print("\n⚠️ 未偵測到有效的 LINE 權限變數 (LINE_CHANNEL_ACCESS_TOKEN / LINE_USER_ID)，改以本地 Console 輸出：")
        print("=" * 60)
        print(text_fallback)
        print("=" * 60)
        if radar_image_url:
            print(f"📡 附帶雷達回波圖: {radar_image_url}")
        print("💡 提示：若需在 LINE 接收視覺化 Flex 圖文卡片，請在 .env 中填寫您的 LINE Token 與 User ID。\n")
        return False

    try:
        from linebot.v3.messaging import (
            Configuration,
            ApiClient,
            MessagingApi,
            PushMessageRequest,
            TextMessage,
            FlexMessage,
            FlexContainer,
            ImageMessage
        )
        config = Configuration(access_token=channel_access_token)
        with ApiClient(config) as api_client:
            line_bot_api = MessagingApi(api_client)

            # 優先嘗試發送 Flex 卡片與雷達圖
            if flex_bubble:
                try:
                    container = FlexContainer.from_json(json.dumps(flex_bubble, ensure_ascii=False))
                    messages: List[Any] = [FlexMessage(alt_text=alt_text, contents=container)]

                    # 若有雷達圖 (降雨機率高時) 則一併發送圖資
                    if radar_image_url:
                        messages.append(
                            ImageMessage(
                                original_content_url=radar_image_url,
                                preview_image_url=radar_image_url
                            )
                        )

                    push_req = PushMessageRequest(to=user_id, messages=messages)
                    line_bot_api.push_message(push_req)
                    mode_name = "晨間" if mode == "morning" else "傍晚"
                    radar_tag = "（含雷達回波圖）" if radar_image_url else ""
                    print(f"✅ {mode_name}通勤快報 (Flex 圖文卡片{radar_tag}) 已成功推播至 LINE！")
                    return True

                except Exception as flex_err:
                    print(f"⚠️ FlexMessage 傳送異常 ({flex_err})，嘗試以純文字降級推播...")

            # 優雅降級：若無 Flex 或發送失敗，使用純文字 TextMessage
            push_req = PushMessageRequest(
                to=user_id,
                messages=[TextMessage(text=text_fallback)]
            )
            line_bot_api.push_message(push_req)
            print("✅ 通勤快報 (純文字降級) 已成功推播至 LINE！")
            return True

    except Exception as e:
        print(f"❌ 推播失敗：{e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="晨間/傍晚通勤與天氣預報秘書 (Commute Weather Assistant)")
    parser.add_argument("--force", action="store_true", help="強制執行，忽略週末/非工作日限制")
    parser.add_argument("--location", type=str, default=None, help="指定查詢縣市 (例如: 臺北市, 新北市)")
    parser.add_argument("--mode", type=str, choices=["auto", "morning", "evening"], default="auto", help="執行模式: auto (依台北時間自動判定), morning (晨間通勤) 或 evening (傍晚下班)")
    args = parser.parse_args()

    location = args.location or os.getenv("LOCATION", "臺北市")
    user_name = os.getenv("USER_NAME", "通勤夥伴")

    taipei_tz = datetime.timezone(datetime.timedelta(hours=8))
    now_taipei = datetime.datetime.now(taipei_tz)

    # 若為 auto，則依台北時間 (UTC+8) 小時自動判定
    if args.mode == "auto":
        current_hour = now_taipei.hour
        mode = "evening" if 15 <= current_hour <= 23 else "morning"
    else:
        mode = args.mode

    # 每日皆執行推播 (含平日與週末)
    mode_name = "☀️ 晨間出門" if mode == "morning" else "🌆 傍晚下班"
    print(f"⏰ 啟動【{mode_name}】通勤快報任務: {now_taipei.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)")
    print(f"📍 目標地區: {location}")

    # 1. 天氣資料
    weather_data = get_commute_weather(location=location, mode=mode)
    rain_prob = weather_data.get("rain_prob_commute", 0)

    # 2. 交通路況
    transit_data = get_commute_transit_status(location=location)

    # 3. 日曆行程
    calendar_data = get_today_first_meeting()

    # 4. Gemini AI 早安/晚安金句
    temp_range = f"{weather_data.get('temp_min', 20)}~{weather_data.get('temp_max', 26)}°C"
    ai_quote = generate_gemini_brief_quote(
        weather_desc=weather_data.get("weather_status", "多雲"),
        temp_range=temp_range,
        rain_prob=rain_prob,
        meeting_summary=calendar_data.get("status_text", ""),
        mode=mode
    )

    # 5. 今日焦點新聞 (晨間通勤時擷取前 3 則)
    news_list = fetch_top_news(limit=3) if mode == "morning" else []

    # 6. YouBike 2.0 即時空車 (若有設定 YOUBIKE_STATIONS 則查詢)
    youbike_list = fetch_youbike_station_status()

    # 7. 雷達回波圖判斷 (降雨機率 >= 50% 或雨天現象時附帶圖資)
    radar_image_url = None
    if rain_prob >= 50 or any(k in weather_data.get("weather_status", "") for k in ["雨", "陣雨", "雷雨"]):
        radar_image_url = get_cwa_radar_image_url()

    # 8. 組裝 Flex Message 卡片與文字降級內容
    flex_bubble = build_weather_commute_flex_message(
        user_name=user_name,
        weather_data=weather_data,
        transit_data=transit_data,
        calendar_data=calendar_data,
        ai_quote=ai_quote,
        news_list=news_list,
        youbike_list=youbike_list,
        mode=mode
    )

    text_brief = build_commute_brief_text(
        user_name=user_name,
        weather_data=weather_data,
        transit_data=transit_data,
        calendar_data=calendar_data,
        location=location,
        mode=mode,
        ai_quote=ai_quote,
        news_list=news_list,
        youbike_list=youbike_list
    )

    success = send_line_push_message(
        flex_bubble=flex_bubble,
        text_fallback=text_brief,
        radar_image_url=radar_image_url,
        mode=mode
    )

    if not success and os.getenv("CI"):
        print("❌ 執行失敗：在雲端 CI 環境下未能成功發送 LINE 推播，請檢查 Secrets 與 Token 設定。")
        sys.exit(1)

if __name__ == "__main__":
    main()
