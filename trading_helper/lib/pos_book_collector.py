import requests
import os
from abc import ABC, abstractmethod
from typing import List


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

    def get_today_book(self, instrument: str) -> dict:
        url = f"{self.host}/{self.version}/instruments/{instrument}/positionBook"
        headers = {
            "Authorization": f"Bearer {os.environ['OANDA_TOKEN']}",
            "Accept-Datetime-Format": "RFC3339",
        }
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return r.json()["positionBook"]
        else:
            return {}
