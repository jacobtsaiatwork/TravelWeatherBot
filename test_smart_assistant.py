import os
import unittest
from unittest.mock import patch, MagicMock
from smart_assistant_service import (
    fetch_top_news,
    get_cwa_radar_image_url,
    generate_gemini_brief_quote,
    fetch_youbike_station_status
)

class TestSmartAssistantService(unittest.TestCase):
    def test_get_cwa_radar_image_url(self):
        url = get_cwa_radar_image_url()
        self.assertTrue(url.startswith("https://"))
        self.assertIn("CV1_3600.png", url)

    @patch("smart_assistant_service.requests.get")
    def test_fetch_top_news_success(self, mock_get):
        sample_rss = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>捷運信義線東延段年底完工 - 中央社</title>
                </item>
                <item>
                    <title>全台氣溫回升高溫達30度 - 自由時報</title>
                </item>
            </channel>
        </rss>"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = sample_rss.encode("utf-8")
        mock_get.return_value = mock_resp

        news = fetch_top_news(limit=2)
        self.assertEqual(len(news), 2)
        self.assertEqual(news[0], "捷運信義線東延段年底完工")
        self.assertEqual(news[1], "全台氣溫回升高溫達30度")

    @patch("smart_assistant_service.requests.get")
    def test_fetch_top_news_network_error(self, mock_get):
        mock_get.side_effect = Exception("Network down")
        news = fetch_top_news(limit=3)
        self.assertEqual(news, [])

    def test_generate_gemini_brief_quote_rule_fallback(self):
        # 測試未提供 API Key 時之規則降級
        quote_rain = generate_gemini_brief_quote(
            weather_desc="陰短暫陣雨",
            temp_range="22~26°C",
            rain_prob=70,
            meeting_summary="今日早晨無安排會議",
            mode="morning",
            gemini_api_key=""
        )
        self.assertIn("雨", quote_rain)

        quote_evening = generate_gemini_brief_quote(
            weather_desc="多雲",
            temp_range="24~27°C",
            rain_prob=10,
            meeting_summary="",
            mode="evening",
            gemini_api_key=""
        )
        self.assertIn("辛苦", quote_evening)

    @patch("smart_assistant_service.requests.post")
    def test_generate_gemini_brief_quote_api_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "早安！今天微風舒適，帶著微笑啟程，迎接美好充實的一天！✨"}]
                    }
                }
            ]
        }
        mock_post.return_value = mock_resp

        quote = generate_gemini_brief_quote(
            weather_desc="晴天",
            temp_range="24~28°C",
            rain_prob=10,
            meeting_summary="",
            mode="morning",
            gemini_api_key="FAKE_KEY"
        )
        self.assertIn("早安", quote)

    def test_fetch_youbike_without_stations(self):
        result = fetch_youbike_station_status(station_keywords=[])
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
