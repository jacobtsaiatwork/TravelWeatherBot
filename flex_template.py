import json
from typing import Dict, Any, List, Optional

def build_weather_commute_flex_message(
    user_name: str,
    weather_data: Dict[str, Any],
    transit_data: Dict[str, Any],
    calendar_data: Dict[str, Any],
    ai_quote: str,
    news_list: Optional[List[str]] = None,
    youbike_list: Optional[List[Dict[str, Any]]] = None,
    mode: str = "morning"  # morning 或 evening
) -> Dict[str, Any]:
    """
    組裝高質感的 LINE Flex Message JSON 卡片 (支援晨間出門與傍晚下班雙模式)
    """
    location = weather_data.get("location", "臺北市")
    temp = weather_data.get("temperature", 25.0)
    temp_min = weather_data.get("temp_min", temp)
    temp_max = weather_data.get("temp_max", temp)
    status = weather_data.get("weather_status", "晴時多雲")
    rain_prob = weather_data.get("rain_prob_commute", 0)
    clothing_tip = weather_data.get("clothing_tip", "穿搭舒適即可")
    transit_text = transit_data.get("status_text", "交通狀況正常")
    calendar_text = calendar_data.get("status_text", "今日早晨無安排會議")
    
    is_morning = (mode == "morning")
    header_title = "☀️ 晨間通勤與天氣快報" if is_morning else "🌆 傍晚下班與交通快報"
    header_color = "#0284c7" if is_morning else "#ea580c"
    greeting_prefix = f"{user_name}！早安" if is_morning else f"{user_name}！辛苦了"

    rain_color = "#e11d48" if rain_prob >= 50 else "#16a34a"
    umbrella_hint = "出門請攜帶雨具" if rain_prob >= 30 else "降雨機率低，免帶傘"
    if not is_morning and rain_prob >= 30:
        umbrella_hint = "下班返家注意路滑備傘"

    body_contents = [
        # 1. 稱呼與地點
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": greeting_prefix, "weight": "bold", "size": "md", "color": "#475569"},
                {"type": "text", "text": f"📍 {location}", "align": "end", "weight": "bold", "size": "md", "color": "#0f172a"}
            ]
        },
        # 2. 氣溫大字與天氣現象
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
                {"type": "text", "text": f"{temp}°C", "size": "4xl", "weight": "bold", "color": "#1e293b"},
                {"type": "text", "text": f"({temp_min}~{temp_max}°C，{status})", "size": "sm", "color": "#64748b", "margin": "md"}
            ]
        },
        # 3. 降雨率與雨具
        {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
                {"type": "text", "text": f"🌧️ 降雨機率 {rain_prob}%", "size": "sm", "weight": "bold", "color": rain_color},
                {"type": "text", "text": f"｜ {umbrella_hint}", "size": "sm", "color": "#475569"}
            ]
        },
        {"type": "separator", "margin": "lg"},
        # 4. 穿衣指南
        {
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
                {"type": "text", "text": "👔 穿著指南", "size": "xs", "weight": "bold", "color": "#64748b"},
                {"type": "text", "text": clothing_tip, "size": "sm", "color": "#334155", "wrap": True}
            ]
        },
        # 5. 交通路況
        {
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
                {"type": "text", "text": "🚇 捷運與台鐵即時路況", "size": "xs", "weight": "bold", "color": "#64748b"},
                {"type": "text", "text": transit_text, "size": "sm", "color": "#dc2626" if transit_data.get("has_alert") else "#16a34a", "wrap": True}
            ]
        },
        # 6. 行事曆行程
        {
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
                {"type": "text", "text": "📅 今日首要行程" if is_morning else "📅 晚間行程動態", "size": "xs", "weight": "bold", "color": "#64748b"},
                {"type": "text", "text": calendar_text, "size": "sm", "color": "#0284c7", "wrap": True}
            ]
        }
    ]

    # 7. YouBike 2.0 即時空車站點 (若有查詢結果)
    if youbike_list and len(youbike_list) > 0:
        body_contents.append({"type": "separator", "margin": "lg"})
        yb_boxes = [{"type": "text", "text": "🚲 YouBike 2.0 即時空車", "size": "xs", "weight": "bold", "color": "#64748b"}]
        for yb in youbike_list[:3]:
            st_name = yb.get("name", "站點")
            rent = yb.get("rent_bikes", 0)
            ebike = yb.get("electric_bikes", 0)
            ret = yb.get("return_spaces", 0)
            ebike_str = f" (電輔 {ebike})" if ebike > 0 else ""
            yb_boxes.append({
                "type": "text",
                "text": f"• {st_name}：可借 {rent} 車{ebike_str} ｜ 可還 {ret} 位",
                "size": "xs",
                "color": "#334155",
                "wrap": True,
                "margin": "xs"
            })
        body_contents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": yb_boxes
        })

    # 8. AI 溫暖問候短語
    if ai_quote:
        body_contents.append({"type": "separator", "margin": "lg"})
        body_contents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
                {"type": "text", "text": "✨ 秘書貼心悄悄話", "size": "xs", "weight": "bold", "color": "#8b5cf6"},
                {"type": "text", "text": ai_quote, "size": "sm", "color": "#7c3aed", "wrap": True, "style": "italic"}
            ]
        })

    # 9. 今日新聞焦點快訊 (晨間推播時顯示)
    if is_morning and news_list and len(news_list) > 0:
        body_contents.append({"type": "separator", "margin": "lg"})
        news_boxes = [{"type": "text", "text": "📰 今日焦點快訊", "size": "xs", "weight": "bold", "color": "#64748b"}]
        for idx, news in enumerate(news_list[:3], 1):
            news_boxes.append({
                "type": "text",
                "text": f"{idx}. {news}",
                "size": "xs",
                "color": "#475569",
                "wrap": True,
                "margin": "xs"
            })
        body_contents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": news_boxes
        })

    flex_bubble = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": header_color,
            "contents": [
                {"type": "text", "text": header_title, "weight": "bold", "size": "lg", "color": "#ffffff"}
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": body_contents
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "📡 CWA 氣象 ｜ TDX 交通 ｜ Google 日曆 ｜ Gemini AI", "size": "xxs", "color": "#94a3b8", "align": "center"}
            ]
        }
    }
    return flex_bubble
