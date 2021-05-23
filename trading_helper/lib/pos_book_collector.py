import requests
import os
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from typing import List, Optional


class PosBookCollInterface:
    @abstractmethod
    def get_today_book(self) -> dict:
        pass


class PosBookCollector(PosBookCollInterface):
    def __init__(self, host, version):
        self.host = host
        self.version = version

    def get_sentiments(
        self, instrument: str, from_dt: datetime, days: int
    ) -> List[dict]:
        dt_range = []

        for i in range(days):
            dt = from_dt + timedelta(days=i)
            if dt >= datetime.now():
                break
            else:
                dt_range.append(dt)

        res_list = []

        for dt in dt_range:
            book = self.get_book(instrument="EUR_USD", dt=dt)
            res_list.append(self.cal_global_perc(book))

        return res_list

    def cal_global_perc(self, book: dict) -> dict:
        dt = datetime.strptime(book["time"], "%Y-%m-%dT%H:%M:%SZ")
        bucket_list = book["buckets"]
        num_buckets = len(bucket_list)
        short = sum([float(x["shortCountPercent"]) for x in bucket_list])
        long = sum([float(x["longCountPercent"]) for x in bucket_list])
        return {"time": dt, "long": long, "short": short}

    def get_book(self, instrument: str, dt: Optional[datetime] = None) -> dict:
        url = f"{self.host}/{self.version}/instruments/{instrument}/positionBook"
        headers = {
            "Authorization": f"Bearer {os.environ['OANDA_TOKEN']}",
            "Accept-Datetime-Format": "RFC3339",
        }

        if dt:
            params = {"time": dt.isoformat() + ".000000Z"}
            r = requests.get(url, params=params, headers=headers)
        else:
            r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return r.json()["positionBook"]
        else:
            return {}
