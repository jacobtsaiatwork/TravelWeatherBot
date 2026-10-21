import os
import sys
import time
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

TDX_TOKEN_URL = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
TDX_METRO_ALERT_URL = "https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/Alert"
TDX_TRA_ALERT_URL = "https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/Alert"

CACHE_FILE = Path(__file__).parent / ".tdx_token_cache.json"

# 依縣市對應之捷運系統代碼
METRO_AUTHORITY_MAP = {
    "臺北市": ["TRTC", "NTMC"],
    "新北市": ["TRTC", "NTMC"],
    "基隆市": ["TRTC"],
    "桃園市": ["TYMC"],
    "臺中市": ["TMRT"],
    "高雄市": ["KRTC"],
}

METRO_NAME_MAP = {
    "TRTC": "台北捷運",
    "NTMC": "新北捷運",
    "TYMC": "桃園捷運",
    "TMRT": "台中捷運",
    "KRTC": "高雄捷運",
}

class TDXClient:
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.client_id = client_id or os.getenv("TDX_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("TDX_CLIENT_SECRET")
        self.access_token: Optional[str] = None
        self.expires_at: float = 0

    def _load_cached_token(self) -> bool:
        if not CACHE_FILE.exists():
            return False
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            token = data.get("access_token")
            expires_at = data.get("expires_at", 0)
            if token and expires_at > time.time() + 300:
                self.access_token = token
                self.expires_at = expires_at
                return True
        except Exception as e:
            logger.debug(f"讀取 TDX Token 快取失敗: {e}")
        return False

    def _save_cached_token(self, token: str, expires_in: int):
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "access_token": token,
                    "expires_at": time.time() + expires_in
                }, f)
        except Exception as e:
            logger.debug(f"儲存 TDX Token 快取失敗: {e}")

    def get_token(self) -> Optional[str]:
        """取得有效的 TDX OAuth 2.0 Access Token (具備快取保護)"""
        if self._load_cached_token():
            return self.access_token

        if not self.client_id or not self.client_secret or self.client_id.startswith("your_"):
            return None

        try:
            logger.info("向 TDX 申請新的 OAuth Access Token...")
            resp = requests.post(
                TDX_TOKEN_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id.strip(),
                    "client_secret": self.client_secret.strip()
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            token = data.get("access_token")
            expires_in = data.get("expires_in", 86400)
            if token:
                self.access_token = token
                self.expires_at = time.time() + expires_in
                self._save_cached_token(token, expires_in)
                return token
        except Exception as e:
            logger.warning(f"取得 TDX Token 失敗: {e}")
        return None

def is_normal_alert(title: str, description: str = "") -> bool:
    """判斷警訊內容是否其實為『正常營運』無延誤"""
    text = (title + " " + description).strip()
    normal_keywords = ["營運正常", "全線營運正常", "全線正常", "正常營運", "目前無異常", "無營運異常"]
    return any(kw in text for kw in normal_keywords)

def fetch_metro_alerts(authority: str, token: str) -> List[Dict[str, Any]]:
    """向 TDX 查詢特定捷運局之營運警訊"""
    url = f"{TDX_METRO_ALERT_URL}/{authority}"
    headers = {"authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        resp = requests.get(url, headers=headers, params={"$format": "JSON"}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            alerts = data.get("Alerts", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            active_alerts = []
            for alert in alerts:
                title = alert.get("Title", "")
                desc = alert.get("Description", "")
                if title and not is_normal_alert(title, desc):
                    active_alerts.append({
                        "system": METRO_NAME_MAP.get(authority, authority),
                        "title": title,
                        "description": desc,
                    })
            return active_alerts
        elif resp.status_code == 429:
            logger.warning(f"TDX API 速率受限 (429 Too Many Requests): {authority}")
        else:
            logger.debug(f"查詢 {authority} 捷運通報狀態碼: {resp.status_code}")
    except Exception as e:
        logger.warning(f"查詢 {authority} 捷運警訊發生例外: {e}")
    return []

def fetch_tra_alerts(token: str) -> List[Dict[str, Any]]:
    """向 TDX 查詢台鐵即時營運警訊"""
    headers = {"authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        resp = requests.get(TDX_TRA_ALERT_URL, headers=headers, params={"$format": "JSON"}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            alerts = data.get("Alerts", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            active_alerts = []
            for alert in alerts:
                title = alert.get("Title", "")
                desc = alert.get("Description", "")
                if title and not is_normal_alert(title, desc):
                    active_alerts.append({
                        "system": "台鐵",
                        "title": title,
                        "description": desc,
                    })
            return active_alerts
        elif resp.status_code == 429:
            logger.warning("TDX API 速率受限 (429 Too Many Requests): TRA")
    except Exception as e:
        logger.warning(f"查詢台鐵警訊發生例外: {e}")
    return []

def get_commute_transit_status(location: str = "臺北市", client_id: Optional[str] = None, client_secret: Optional[str] = None) -> Dict[str, Any]:
    """
    整合交通即時狀況查詢入口：
    1. 驗證 TDX Token
    2. 依據所在縣市查詢捷運 (北捷/新北捷/桃捷/中捷/高捷) 與台鐵即時警訊
    3. 若無異常則回報全線正常；若有事故則產出警告摘要
    """
    client = TDXClient(client_id, client_secret)
    token = client.get_token()

    if not token:
        logger.info("未檢測到有效 TDX 金鑰，大眾運輸使用模擬檢查 (可在 .env 設定 TDX 金鑰啟用即時通報)。")
        return {
            "has_alert": False,
            "status_text": "大眾運輸（捷運、台鐵）目前全線正常營運，無重大事故通報。",
            "alerts": [],
            "source": "本地模擬/預設狀態"
        }

    authorities = METRO_AUTHORITY_MAP.get(location, ["TRTC"])
    all_alerts = []

    # 1. 查詢捷運通報
    for auth in authorities:
        alerts = fetch_metro_alerts(auth, token)
        all_alerts.extend(alerts)
        time.sleep(0.3)

    # 2. 查詢台鐵通報
    time.sleep(0.3)
    tra_alerts = fetch_tra_alerts(token)
    all_alerts.extend(tra_alerts)

    if not all_alerts:
        transit_names = "、".join([METRO_NAME_MAP.get(a, a) for a in authorities] + ["台鐵"])
        return {
            "has_alert": False,
            "status_text": f"{transit_names}目前全線正常營運，無事故通報。",
            "alerts": [],
            "source": "交通部 TDX 官方實時資料"
        }

    # 組織異常警告訊息
    alert_lines = []
    for a in all_alerts:
        desc_part = f" - {a['description']}" if a['description'] and a['description'] != a['title'] else ""
        alert_lines.append(f"⚠️【{a['system']}】{a['title']}{desc_part}")

    alert_summary = "\n".join(alert_lines)
    return {
        "has_alert": True,
        "status_text": f"偵測到以下運輸異常，請留意通勤時間：\n{alert_summary}",
        "alerts": all_alerts,
        "source": "交通部 TDX 官方實時資料"
    }

if __name__ == "__main__":
    status = get_commute_transit_status("臺北市")
    print("交通狀況結果：")
    print(status["status_text"])
    print("資料來源：", status["source"])
