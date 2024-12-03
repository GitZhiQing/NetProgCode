import json
import os

import requests
from bs4 import BeautifulSoup

from app import settings

with open(
    os.path.join(settings.DATA_DIR, "target_list.json"), "r", encoding="utf-8"
) as f:
    target_list = json.load(f)

APP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
    "Safari/537.36 Edg/131.0.0.0"
)


def get_soup(url, headers=None) -> BeautifulSoup or None:
    """
    获取 soup 对象
    """
    try:
        response = requests.get(url, headers)
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None


from app.crawler.main import (  # noqa: E402
    crawl_one_id,
    crawl_range_id,
    crawl_range_count,
    get_first_100_words,
    get_latest_article_id,
)

__all__ = [
    "crawl_one_id",
    "crawl_range_id",
    "crawl_range_count",
    "get_first_100_words",
    "get_latest_article_id",
]
