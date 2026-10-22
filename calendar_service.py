import os
import sys
import logging
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

try:
    import icalendar
    import recurring_ical_events
    import dateutil.tz
    ICAL_AVAILABLE = True
except ImportError:
    ICAL_AVAILABLE = False
    logger.warning("未安裝 icalendar 或 recurring_ical_events，日曆功能將啟用模擬模式。")

def parse_calendar_configs(raw_input: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    解析多個日曆設定。
    支援以逗號、分號或換行分隔：
    - '工作:https://.../basic.ics, 個人:https://.../basic.ics'
    - 'https://.../basic.ics' (自動命名為 日曆1, 日曆2)
    """
    if raw_input is None:
        raw = os.getenv("GOOGLE_CALENDAR_ICAL_URLS") or os.getenv("GOOGLE_CALENDAR_ICAL_URL", "")
    else:
        raw = raw_input
    if not raw or not raw.strip():
        return []

    entries = []
    # 支援以逗號、分號或換行分割
    chunks = [c.strip() for c in raw.replace(";", "\n").replace(",", "\n").splitlines() if c.strip()]
    for idx, chunk in enumerate(chunks, 1):
        if ":" in chunk and ("http://" in chunk or "https://" in chunk):
            parts = chunk.split("http", 1)
            tag_part = parts[0].strip().rstrip(":")
            url_part = "http" + parts[1].strip()
            tag = tag_part if tag_part else f"日曆{idx}"
            entries.append((tag, url_part))
        else:
            entries.append((f"日曆{idx}", chunk))
    return entries

def fetch_events_from_ical(url: str, start_dt: datetime.datetime, end_dt: datetime.datetime) -> List[Dict[str, Any]]:
    """自單一 iCal 網址抓取指定時間區間內的事件"""
    if not ICAL_AVAILABLE:
        return []

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        cal = icalendar.Calendar.from_ical(resp.text)
        raw_events = recurring_ical_events.of(cal).between(start_dt, end_dt)
        
        events = []
        for ev in raw_events:
            summary = str(ev.get("SUMMARY", "未命名行程")).strip()
            dtstart = ev.get("DTSTART").dt
            
            # 判斷是否為全天事件 (全天事件型別為 datetime.date 而非 datetime.datetime)
            is_all_day = not isinstance(dtstart, datetime.datetime)
            
            events.append({
                "summary": summary,
                "start": dtstart,
                "is_all_day": is_all_day
            })
        return events
    except Exception as e:
        logger.warning(f"抓取日曆事件失敗 ({url[:45]}...): {e}")
        return []

def get_today_first_meeting(calendar_configs: Optional[List[Tuple[str, str]]] = None) -> Dict[str, Any]:
    """
    跨多信箱整合今日行程，並挑出最早開始的一場會議提醒。
    """
    configs = calendar_configs or parse_calendar_configs()

    if not configs or not ICAL_AVAILABLE:
        return {
            "has_events": False,
            "status_text": "今日早晨無安排會議，祝你專注享受充實的一天！",
            "first_event": None,
            "total_count": 0,
            "source": "本地預設/未設定日曆"
        }

    taipei_tz = dateutil.tz.gettz("Asia/Taipei")
    now = datetime.datetime.now(taipei_tz)
    start_of_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=taipei_tz)
    end_of_day = datetime.datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=taipei_tz)

    all_timed_events = []
    all_day_events = []

    for tag, url in configs:
        evs = fetch_events_from_ical(url, start_of_day, end_of_day)
        for ev in evs:
            ev["tag"] = tag
            if ev["is_all_day"]:
                all_day_events.append(ev)
            else:
                # 確保時區為台北時區
                start_time = ev["start"]
                if hasattr(start_time, "astimezone"):
                    start_time = start_time.astimezone(taipei_tz)
                    ev["start"] = start_time
                all_timed_events.append(ev)

    # 排序定時會議（依開始時間早至晚）
    all_timed_events.sort(key=lambda x: x["start"])

    total_count = len(all_timed_events) + len(all_day_events)

    if not total_count:
        return {
            "has_events": False,
            "status_text": "今日早晨無安排會議，祝你專注享受充實的一天！",
            "first_event": None,
            "total_count": 0,
            "source": "Google 日曆"
        }

    if all_timed_events:
        first = all_timed_events[0]
        time_str = first["start"].strftime("%H:%M")
        tag_str = f"({first['tag']})" if first["tag"] else ""
        first_title = f"{time_str} {first['summary']} {tag_str}".strip()

        extra_info = f"，今日共安排 {total_count} 場行程" if total_count > 1 else ""
        status_text = f"首場會議：{first_title}{extra_info}。"
        return {
            "has_events": True,
            "status_text": status_text,
            "first_event": {
                "time_str": time_str,
                "summary": first["summary"],
                "tag": first["tag"]
            },
            "total_count": total_count,
            "source": "Google 日曆"
        }
    else:
        # 僅有全天事件
        first_all_day = all_day_events[0]
        tag_str = f"({first_all_day['tag']})" if first_all_day['tag'] else ""
        status_text = f"全天行程：{first_all_day['summary']} {tag_str}。"
        return {
            "has_events": True,
            "status_text": status_text,
            "first_event": {
                "time_str": "全天",
                "summary": first_all_day["summary"],
                "tag": first_all_day["tag"]
            },
            "total_count": total_count,
            "source": "Google 日曆"
        }

if __name__ == "__main__":
    res = get_today_first_meeting()
    print("日曆檢查結果：")
    print(res["status_text"])
    print("來源：", res["source"])
