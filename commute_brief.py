import os
import sys
import argparse
import datetime
from pathlib import Path
from dotenv import load_dotenv

# 載入同目錄下的 .env
load_dotenv(Path(__file__).parent / ".env")

from weather_service import build_morning_brief_text, get_commute_weather
from transit_service import get_commute_transit_status

def send_line_push_message(message: str) -> bool:
    """
    透過 LINE Messaging API 發送 Push 訊息給指定的 LINE_USER_ID。
    若未設定則輸出至 Console。
    """
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")

    if not channel_access_token or not user_id or channel_access_token.startswith("your_") or user_id.startswith("your_"):
        print("\n⚠️ 未偵測到有效的 LINE 權限變數 (LINE_CHANNEL_ACCESS_TOKEN / LINE_USER_ID)，改以本地 Console 輸出：")
        print("=" * 50)
        print(message)
        print("=" * 50)
        print("💡 提示：若需收到 LINE 推播通知，請在 .env 中填寫您的 LINE Token 與 User ID。\n")
        return False

    try:
        from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, PushMessageRequest, TextMessage
        config = Configuration(access_token=channel_access_token)
        with ApiClient(config) as api_client:
            line_bot_api = MessagingApi(api_client)
            push_req = PushMessageRequest(
                to=user_id,
                messages=[TextMessage(text=message)]
            )
            line_bot_api.push_message(push_req)
            print("✅ 晨間通勤快報已成功推播至 LINE！")
            return True
    except Exception as e:
        print(f"❌ 推播失敗：{e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="晨間通勤與天氣預報秘書 (Commute Weather Brief Assistant)")
    parser.add_argument("--force", action="store_true", help="強制執行，忽略週末/非工作日限制")
    parser.add_argument("--location", type=str, default=None, help="指定查詢縣市 (例如: 臺北市, 新北市)")
    args = parser.parse_args()

    location = args.location or os.getenv("LOCATION", "臺北市")
    user_name = os.getenv("USER_NAME", "通勤夥伴")

    # 檢查是否為工作日 (0=Mon, 4=Fri, 5=Sat, 6=Sun)
    today = datetime.date.today()
    if today.weekday() >= 5 and not args.force:
        print(f"🏖️ 今天是週末 ({today})，跳過晨間工作通勤推播。(若欲立即測試請加上 --force 參數)")
        return

    print(f"⏰ 啟動晨間通勤快報任務: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📍 目標地區: {location}")
    
    weather_data = get_commute_weather(location=location)
    transit_data = get_commute_transit_status(location=location)
    brief = build_morning_brief_text(user_name=user_name, weather_data=weather_data, transit_data=transit_data, location=location)
    
    success = send_line_push_message(brief)
    if not success and os.getenv("CI"):
        print("❌ 執行失敗：在雲端 CI 環境下未能成功發送 LINE 推播，請檢查 Secrets 與 Token 設定。")
        sys.exit(1)

if __name__ == "__main__":
    main()
