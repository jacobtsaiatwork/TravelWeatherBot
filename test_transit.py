import os
import unittest
from unittest.mock import patch, MagicMock
from transit_service import (
    is_normal_alert,
    TDXClient,
    get_commute_transit_status
)

class TestTransitService(unittest.TestCase):
    def test_is_normal_alert(self):
        self.assertTrue(is_normal_alert("全線營運正常"))
        self.assertTrue(is_normal_alert("營運正常", "各路線運作順暢"))
        self.assertTrue(is_normal_alert("目前無異常"))
        self.assertFalse(is_normal_alert("號誌異常班距拉長"))
        self.assertFalse(is_normal_alert("淡水信義線延誤", "列車設備異常"))

    @patch.dict(os.environ, {"TDX_CLIENT_ID": "", "TDX_CLIENT_SECRET": ""}, clear=False)
    @patch("transit_service.TDXClient._load_cached_token", return_value=False)
    def test_fallback_when_no_credentials(self, mock_load):
        status = get_commute_transit_status(location="臺北市", client_id="", client_secret="")
        self.assertFalse(status["has_alert"])
        self.assertIn("大眾運輸", status["status_text"])
        self.assertIn("模擬", status["source"])

    @patch("transit_service.TDXClient.get_token")
    @patch("transit_service.fetch_metro_alerts")
    @patch("transit_service.fetch_tra_alerts")
    def test_normal_operations_status(self, mock_tra, mock_metro, mock_token):
        mock_token.return_value = "fake-token"
        mock_metro.return_value = []
        mock_tra.return_value = []

        status = get_commute_transit_status(location="臺北市", client_id="test", client_secret="test")
        self.assertFalse(status["has_alert"])
        self.assertIn("全線正常營運", status["status_text"])
        self.assertIn("TDX", status["source"])

    @patch("transit_service.TDXClient.get_token")
    @patch("transit_service.fetch_metro_alerts")
    @patch("transit_service.fetch_tra_alerts")
    def test_alert_detected_status(self, mock_tra, mock_metro, mock_token):
        mock_token.return_value = "fake-token"
        mock_metro.return_value = [{
            "system": "台北捷運",
            "title": "板南線列車設備異常",
            "description": "忠孝新生站班距調整為 8 分鐘"
        }]
        mock_tra.return_value = []

        status = get_commute_transit_status(location="臺北市", client_id="test", client_secret="test")
        self.assertTrue(status["has_alert"])
        self.assertIn("板南線列車設備異常", status["status_text"])
        self.assertIn("忠孝新生站", status["status_text"])

if __name__ == "__main__":
    unittest.main()
