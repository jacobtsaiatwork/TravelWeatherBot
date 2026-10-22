import unittest
from flex_template import build_weather_commute_flex_message

class TestFlexTemplate(unittest.TestCase):
    def setUp(self):
        self.weather_data = {
            "location": "臺北市",
            "temperature": 26.5,
            "temp_min": 23.0,
            "temp_max": 30.0,
            "rain_prob_commute": 60,
            "weather_status": "午後短暫陣雨",
            "clothing_tip": "短袖舒適，備薄外套",
            "source": "CWA"
        }
        self.transit_data = {
            "has_alert": False,
            "status_text": "台北捷運全線營運正常無通報",
            "source": "TDX"
        }
        self.calendar_data = {
            "has_events": True,
            "status_text": "首場會議：09:30 每週晨會",
            "source": "Google 日曆"
        }

    def test_build_morning_flex_message(self):
        bubble = build_weather_commute_flex_message(
            user_name="夥伴",
            weather_data=self.weather_data,
            transit_data=self.transit_data,
            calendar_data=self.calendar_data,
            ai_quote="祝你今天元氣滿滿！☀️",
            news_list=["最新重大交通法規通過", "AI 技術最新進展分享"],
            youbike_list=[{"name": "捷運科技大樓站", "rent_bikes": 10, "electric_bikes": 2, "return_spaces": 12}],
            mode="morning"
        )
        self.assertEqual(bubble["type"], "bubble")
        self.assertEqual(bubble["header"]["backgroundColor"], "#0284c7")
        self.assertIn("晨間通勤與天氣快報", bubble["header"]["contents"][0]["text"])

    def test_build_evening_flex_message(self):
        bubble = build_weather_commute_flex_message(
            user_name="夥伴",
            weather_data=self.weather_data,
            transit_data=self.transit_data,
            calendar_data=self.calendar_data,
            ai_quote="辛苦了一整天，回家好好休息！🌙",
            mode="evening"
        )
        self.assertEqual(bubble["type"], "bubble")
        self.assertEqual(bubble["header"]["backgroundColor"], "#ea580c")
        self.assertIn("傍晚下班與交通快報", bubble["header"]["contents"][0]["text"])

if __name__ == "__main__":
    unittest.main()
