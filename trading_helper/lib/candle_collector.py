import requests
import os
from datetime import datetime, timedelta
from trading_helper.models import Candle
from typing import List


class CandleCollector:
    def __init__(self, host, version):
        self.host = host
        self.version = version
        self.headers = {
            "Authorization": f"Bearer {os.environ['OANDA_TOKEN']}",
            "Accept-Datetime-Format": "RFC3339",
        }

    def _compose_candle(self, candle):
        return {
            "Open": float(candle["mid"]["o"]),
            "High": float(candle["mid"]["h"]),
            "Low": float(candle["mid"]["l"]),
            "Close": float(candle["mid"]["c"]),
            "starting_time": candle["time"],
            "Date": datetime.strptime(candle["time"], "%Y-%m-%dT%H:%M:%S.%f000Z")
            + timedelta(days=1),
        }

    def get_daily_candles(
        self, instrument: str, from_date: datetime, days: int
    ) -> List[dict]:
        from_dt = from_date.replace(hour=0, minute=0, second=0)
        to_dt = from_dt + timedelta(days=days)

        if to_dt.date() >= datetime.today().date():
            to_dt = datetime.now() - timedelta(days=1)

        url = f"{self.host}/{self.version}/instruments/{instrument}/candles"
        params = {
            "granularity": "D",
            "from": from_dt.isoformat(),
            "to": to_dt.isoformat(),
            "includeFirst": False,
        }
        r = requests.get(url, params=params, headers=self.headers)

        def map_helper(candle):
            return self._compose_candle(candle)

        if r.status_code == 200:
            return list(map(map_helper, r.json()["candles"]))
        else:
            raise Exception(f"ERROR status: {r.status_code}\ndetail: {r.text}")

    def get_today_candle(self, instrument: str, granularity: str = "D") -> dict:
        from_time = datetime.now().replace(hour=0, minute=0, second=0)
        url = f"{self.host}/{self.version}/instruments/{instrument}/candles"
        params = {
            "granularity": granularity,
            "from": from_time.isoformat(),
            "to": (from_time + timedelta(days=1)).isoformat(),
            "includeFirst": False,
        }
        r = requests.get(url, params=params, headers=self.headers)

        if r.status_code == 200:
            candle = r.json()["candles"][0]
            if candle["complete"]:
                return self._compose_candle(candle)
            else:
                raise Exception("Did not find complete candle")
        else:
            raise Exception(f"ERROR status: {r.status_code}\ndetail: {r.text}")
