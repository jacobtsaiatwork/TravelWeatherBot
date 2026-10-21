import os
import unittest
from unittest.mock import patch, MagicMock
from weather_service import (
    normalize_location_name,
    generate_clothing_tip,
    fetch_cwa_weather,
    get_commute_weather_mock,
    get_commute_weather,
    build_morning_brief_text
)

class TestWeatherService(unittest.TestCase):
    def test_normalize_location_name(self):
        self.assertEqual(normalize_location_name("台北市"), "臺北市")
        self.assertEqual(normalize_location_name("台中市"), "臺中市")
        self.assertEqual(normalize_location_name("台南市"), "臺南市")
        self.assertEqual(normalize_location_name("高雄市"), "高雄市")
        self.assertEqual(normalize_location_name(" 台北市 "), "臺北市")

    def test_generate_clothing_tip(self):
        hot_tip = generate_clothing_tip(28.0, 34.0)
        self.assertIn("炎熱", hot_tip)
        
        warm_tip = generate_clothing_tip(23.0, 29.0)
        self.assertIn("偏熱舒適", warm_tip)
        
        pleasant_tip = generate_clothing_tip(21.0, 26.0)
        self.assertIn("舒適", pleasant_tip)

        cool_tip = generate_clothing_tip(16.0, 19.0)
        self.assertIn("偏涼", cool_tip)

        cold_tip = generate_clothing_tip(11.0, 14.0)
        self.assertIn("寒冷", cold_tip)

    def test_get_commute_weather_mock(self):
        mock_data = get_commute_weather_mock("台北市")
        self.assertEqual(mock_data["location"], "臺北市")
        self.assertIn("temperature", mock_data)
        self.assertIn("rain_prob_commute", mock_data)
        self.assertTrue(mock_data["umbrella_needed"])

    @patch("weather_service.requests.get")
    def test_fetch_cwa_weather_success(self, mock_get):
        fake_cwa_json = {
            "success": "true",
            "records": {
                "datasetDescription": "三十六小時天氣預報",
                "location": [
                    {
                        "locationName": "臺北市",
                        "weatherElement": [
                            {
                                "elementName": "Wx",
                                "time": [{"parameter": {"parameterName": "午後短暫雷陣雨", "parameterValue": "22"}}]
                            },
                            {
                                "elementName": "PoP",
                                "time": [{"parameter": {"parameterName": "70", "parameterUnit": "百分比"}}]
                            },
                            {
                                "elementName": "MinT",
                                "time": [{"parameter": {"parameterName": "25", "parameterUnit": "C"}}]
                            },
                            {
                                "elementName": "MaxT",
                                "time": [{"parameter": {"parameterName": "33", "parameterUnit": "C"}}]
                            },
                            {
                                "elementName": "CI",
                                "time": [{"parameter": {"parameterName": "悶熱"}}]
                            }
                        ]
                    }
                ]
            }
        }
        mock_resp = MagicMock()
        mock_resp.json.return_value = fake_cwa_json
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = fetch_cwa_weather(api_key="CWA-TEST-KEY", location="台北市")
        self.assertEqual(result["location"], "臺北市")
        self.assertEqual(result["temperature"], 29.0)
        self.assertEqual(result["temp_min"], 25.0)
        self.assertEqual(result["temp_max"], 33.0)
        self.assertEqual(result["rain_prob_commute"], 70)
        self.assertEqual(result["weather_status"], "午後短暫雷陣雨")
        self.assertTrue(result["umbrella_needed"])
        self.assertIn("炎熱", result["clothing_tip"])

    @patch.dict(os.environ, {"CWA_API_KEY": ""}, clear=False)
    def test_get_commute_weather_fallback_when_no_key(self):
        result = get_commute_weather(location="新北市", api_key="")
        self.assertEqual(result["location"], "新北市")
        self.assertIn("Mock", result["source"])

    @patch("weather_service.fetch_cwa_weather")
    def test_get_commute_weather_fallback_on_api_error(self, mock_fetch):
        mock_fetch.side_effect = Exception("API Connection Timeout")
        result = get_commute_weather(location="臺北市", api_key="CWA-INVALID-KEY")
        self.assertEqual(result["location"], "臺北市")
        self.assertIn("Mock", result["source"])

    @patch("transit_service.get_commute_transit_status")
    def test_build_morning_brief_text(self, mock_transit):
        mock_transit.return_value = {
            "has_alert": False,
            "status_text": "全線營運正常",
            "source": "TDX"
        }
        weather_mock = get_commute_weather_mock("臺北市")
        brief = build_morning_brief_text(user_name="小華", weather_data=weather_mock)
        self.assertIn("小華", brief)
        self.assertIn("晨間通勤與天氣快報", brief)
        self.assertIn("氣溫", brief)
        self.assertIn("穿著指南", brief)
        self.assertIn("交通狀況", brief)

if __name__ == "__main__":
    unittest.main()
