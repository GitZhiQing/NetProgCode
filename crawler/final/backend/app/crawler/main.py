import logging
from typing import Optional

import requests
from sqlalchemy.orm import Session

from app import deps, settings
from app.crawler import get_soup, target_list, APP_UA
from app.crawler.utils import get_first_100_words, get_latest_article_id
from app.database import crud


def crawl_one_id(article_id: int, target_id: int):
    """
    爬取指定 id 的文章
    """
    url_prefix = target_list[target_id]["article_url_prefix"]
    url = url_prefix + str(article_id)

    db: Session = next(deps.get_db())
    if crud.get_odoc_by_url(db, url):
        logging.info(
            f"文章 ID: {article_id} 在 {target_list[target_id]['name']} 已爬取."
        )
        return

    headers = {
        "User-Agent": APP_UA,
        "Referer": f"{target_list[target_id]['url']}",
    }
    resp = requests.get(url, headers=headers)

    if resp.status_code == 404:
        logging.info(
            f"文章 ID: {article_id} 在 {target_list[target_id]['name']} 不存在."
        )
        return

    if "404 Not Found" in resp.text:
        logging.info(
            f"文章 ID: {article_id} 在 {target_list[target_id]['name']} 不存在."
        )
        return

    logging.info(f"开始爬取文章 URL: {url}...")
    soup = get_soup(url)
    title = soup.title.string
    site = target_list[target_id]["name"]
    first_100_words = get_first_100_words(soup, target_id)
    odoc = crud.create_odoc(db, url, title, site, first_100_words)
    logging.info("Done.")
    with open(f"{settings.ODOC_DIR}/{odoc.odid}.html", "w", encoding="utf-8") as file:
        file.write(resp.text)


def crawl_range_id(
    start_id: Optional[int] = None, end_id: Optional[int] = None, target_id: int = 0
):
    """
    爬取指定范围 id 的文章
    """
    logging.info(
        f"开始爬取 {target_list[target_id]['name']} 的文章范围 ID: {start_id} - {end_id}..."
    )
    if end_id is None:
        end_id = get_latest_article_id(target_id)
    if start_id is None:
        start_id = end_id - 100
    for article_id in range(start_id, end_id + 1):
        crawl_one_id(article_id, target_id)
    logging.info("Done.")


def crawl_range_count(count: int = 100, target_id: int = 0):
    """
    爬取指定数量的文章
    """
    logging.info(f"开始爬取 {target_list[target_id]['name']} 的最新 {count} 篇文章...")
    latest_article_id = get_latest_article_id(target_id)
    start_id = latest_article_id - count + 1
    crawl_range_id(start_id, latest_article_id, target_id)
    logging.info("Done.")
