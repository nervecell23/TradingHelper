import requests
import os
from datetime import datetime, timedelta
from trading_helper.models import Candle


class CandleCollector:
    def __init__(self, host, version):
        self.host = host
        self.version = version

    def get_today_candle(self, instrument, granularity="D"):
        """ """
        from_time = datetime.now().replace(hour=0, minute=0, second=0)
        to_time = from_time + timedelta(days=1)
        url = f"{self.host}/{self.version}/{instrument}/candles"
        headers = {
            "Authorization": f"Bearer {os.environ['OANDA_TOKEN']}",
            "Accept-Datetime-Format": "RFC3339",
        }
        params = {
            "granularity": granularity,
            "from": from_time.isoformat(),
            "to": to_time.isoformat(),
            "includeFirst": False,
        }
        r = requests.get(url, params=params, headers=headers)

        if r.status_code == 200:
            for x in r.json()["candles"]:
                if x["complete"]:
                    candle = Candle(
                        open=x["mid"]["o"],
                        high=x["mid"]["h"],
                        low=x["mid"]["l"],
                        close=x["mid"]["c"],
                        starting_time=x["time"],
                    )
