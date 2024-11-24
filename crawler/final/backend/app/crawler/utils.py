import logging
import time

import requests
from bs4 import BeautifulSoup

from app.crawler import target_list


def get_first_100_words(soup, target_id: int) -> str:
    """
    提取文章的前 100 个字
    """
    content_extractors = {
        0: lambda s: s.find("meta", {"name": "description"})["content"],
        1: lambda s: s.find("div", {"class": "content"}).get_text(
            separator=" ", strip=True
        ),
        2: lambda s: s.find("textarea", {"id": "md_view_content"}).get_text(
            separator=" ", strip=True
        ),
    }

    try:
        content = content_extractors[target_id](soup)
        return " ".join(content.split())[:100]
    except Exception as e:
        logging.error(f"获取 {target_list[target_id]['name']} 的文章简介时出错: {e}")
        return ""


def get_latest_article_id(target_id: int) -> int:
    """
    获取最新文章的 id
    """
    try:
        if target_id == 0:
            return fetch_latest_article_id_secrss()
        elif target_id == 1:
            return fetch_latest_article_id_anquanke()
        elif target_id == 2:
            return fetch_latest_article_id_butian()
    except Exception as e:
        logging.error(
            f"获取 {target_list[target_id]['name']} 的最新文章 ID 时出错: {e}"
        )
    return 0


def fetch_latest_article_id_secrss() -> int:
    """
    获取安全内参最新文章的 id
    """
    url_prefix = "https://www.secrss.com/api/articles"
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    response = requests.get(
        url_prefix, params={"lastPublishedAt": datetime, "referer": "web"}
    )
    response.raise_for_status()
    return int(response.json()["data"][0]["id"])


def fetch_latest_article_id_anquanke() -> int:
    """
    获取安全客最新文章的 id
    """
    url_prefix = "https://www.anquanke.com/webapi/api/home/articles"
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    timestamp = int(time.time() * 1000)
    response = requests.get(
        url_prefix,
        params={"category": "", "postDate": datetime, "pageSize": 50, "_": timestamp},
    )
    response.raise_for_status()
    return int(response.json()["data"][0]["postId"])


def fetch_latest_article_id_butian() -> int:
    """
    获取奇安信攻防社区最新文章的 id
    """
    url = "https://forum.butian.net/Rss"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "xml")
    return int(soup.find_all("item")[0].guid.string.split("/")[-1])
