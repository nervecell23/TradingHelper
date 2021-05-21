import requests
import os
from datetime import datetime
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

    def cal_global_perc(self, book: dict) -> dict:
        bucket_list = book["buckets"]
        num_buckets = len(bucket_list)
        short = sum([float(x["shortCountPercent"]) for x in bucket_list]) / num_buckets
        long = sum([float(x["longCountPercent"]) for x in bucket_list]) / num_buckets
        return {"long": long, "short": short}

    def get_book(self, instrument: str, dt: Optional[datetime]) -> dict:
        url = f"{self.host}/{self.version}/instruments/{instrument}/positionBook"
        headers = {
            "Authorization": f"Bearer {os.environ['OANDA_TOKEN']}",
            "Accept-Datetime-Format": "RFC3339",
        }

        if dt:
            params = {"time": dt.isoformat()}
            r = requests.get(url, params=params, headers=headers)
        else:
            r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return r.json()["positionBook"]
        else:
            return {}
