import os
import unittest
import datetime
from unittest.mock import patch, MagicMock
from calendar_service import (
    parse_calendar_configs,
    get_today_first_meeting
)

class TestCalendarService(unittest.TestCase):
    def test_parse_calendar_configs(self):
        raw = "工作:https://calendar.google.com/test1.ics, 個人:https://calendar.google.com/test2.ics"
        configs = parse_calendar_configs(raw)
        self.assertEqual(len(configs), 2)
        self.assertEqual(configs[0][0], "工作")
        self.assertEqual(configs[0][1], "https://calendar.google.com/test1.ics")
        self.assertEqual(configs[1][0], "個人")
        self.assertEqual(configs[1][1], "https://calendar.google.com/test2.ics")

    def test_parse_calendar_configs_empty(self):
        configs = parse_calendar_configs("")
        self.assertEqual(configs, [])

    @patch("calendar_service.fetch_events_from_ical")
    def test_get_today_first_meeting_with_events(self, mock_fetch):
        # 模擬兩個信箱回傳定時事件
        taipei_tz = datetime.timezone(datetime.timedelta(hours=8))
        now = datetime.datetime.now(taipei_tz)
        
        meeting_10am = datetime.datetime(now.year, now.month, now.day, 10, 0, tzinfo=taipei_tz)
        meeting_9am = datetime.datetime(now.year, now.month, now.day, 9, 0, tzinfo=taipei_tz)

        # 第一次呼叫 (工作日曆)
        mock_fetch.side_effect = [
            [{"summary": "部門週會", "start": meeting_10am, "is_all_day": False}],
            [{"summary": "看牙醫", "start": meeting_9am, "is_all_day": False}]
        ]

        test_configs = [("工作", "https://mock.url/1"), ("個人", "https://mock.url/2")]
        res = get_today_first_meeting(calendar_configs=test_configs)

        self.assertTrue(res["has_events"])
        self.assertEqual(res["total_count"], 2)
        # 應挑出較早的 09:00 看牙醫
        self.assertIn("09:00", res["status_text"])
        self.assertIn("看牙醫", res["status_text"])
        self.assertIn("個人", res["status_text"])
        self.assertIn("2 場行程", res["status_text"])

    @patch("calendar_service.fetch_events_from_ical")
    def test_get_today_first_meeting_empty(self, mock_fetch):
        mock_fetch.return_value = []
        test_configs = [("工作", "https://mock.url/1")]
        res = get_today_first_meeting(calendar_configs=test_configs)

        self.assertFalse(res["has_events"])
        self.assertIn("今日早晨無安排會議", res["status_text"])

if __name__ == "__main__":
    unittest.main()
