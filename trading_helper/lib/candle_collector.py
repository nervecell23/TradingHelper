import requests
import os
from datetime import datetime, timedelta
from trading_helper.models import Candle
from typing import List


class CandleCollector:
    def __init__(self, host, version):
        self.host = host
        self.version = version

    def get_daily_candles(
        self, instrument: str, from_date: datetime, days: int
    ) -> List[Candle]:
        """ """
        from_dt = from_date.replace(hour=0, minute=0, second=0)
        to_dt = from_dt + timedelta(days=days)

        if to_dt.date() >= datetime.today().date():
            to_dt = datetime.now()

        url = f"{self.host}/{self.version}/instruments/{instrument}/candles"

        headers = {
            "Authorization": f"Bearer {os.environ['OANDA_TOKEN']}",
            "Accept-Datetime-Format": "RFC3339",
        }
        params = {
            "granularity": "D",
            "from": from_dt.isoformat(),
            "to": to_dt.isoformat(),
            "includeFirst": False,
        }
        r = requests.get(url, params=params, headers=headers)

        if r.status_code == 200:
            res_list = []
            for candle in r.json()["candles"]:
                candle = Candle(
                    open=candle["mid"]["o"],
                    high=candle["mid"]["h"],
                    low=candle["mid"]["l"],
                    close=candle["mid"]["c"],
                    starting_time=candle["time"],
                )
                res_list.append(candle)
            return res_list
        else:
            raise Exception(f"ERROR status: {r.status_code}\ndetail: {r.text}")

    def get_today_candle(self, instrument: str, granularity: str = "D") -> Candle:
        """ """
        from_time = datetime.now().replace(hour=0, minute=0, second=0)
        to_time = from_time + timedelta(days=1)
        url = f"{self.host}/{self.version}/instruments/{instrument}/candles"
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
            candle = r.json()["candles"][0]
            if candle["complete"]:
                return Candle(
                    open=candle["mid"]["o"],
                    high=candle["mid"]["h"],
                    low=candle["mid"]["l"],
                    close=candle["mid"]["c"],
                    starting_time=candle["time"],
                )
            else:
                raise Exception("Did not find complete candle")
        else:
            raise Exception(f"ERROR status: {r.status_code}\ndetail: {r.text}")
