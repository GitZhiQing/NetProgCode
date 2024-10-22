import re
import json
import time
import urllib3

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁用安全请求警告


def get_soup(url, proxy=False):
    """
    获取 soup 对象
    默认不使用代理，从 headers.json 中加载必要请求头
    """
    try:
        proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
        with open("headers.json", "r", encoding="utf-8") as f:
            headers = json.load(f)
        response = requests.get(
            url, headers=headers, proxies=proxies if proxy else None, verify=False
        )
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None


def get_url_title(url, retries=3):
    """
    获取 URL 的标题，带有重试机制
    """
    for _ in range(retries):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            if soup is None or soup.title is None or soup.title.string is None:
                return "No title found"
            return soup.title.string
        except requests.RequestException as e:
            print(f"请求错误: {e}")
            time.sleep(1)
    return "No title found"


def get_url_suburl(url):
    """
    获取 url 的页面子链接
    """
    soup = get_soup(url)
    if soup is None:
        return None
    suburls = set()  # 使用集合去重
    for a in soup.find_all("a", href=True):
        suburl = a["href"]
        if re.match(r"^https?://", suburl):
            suburls.add(suburl)
    suburls.discard(url)
    return suburls


def get_url_suburl_data(url, depth, max_depth, pbar=None):
    """
    获取 url 的页面子链接数据，带有深度控制
    """
    if depth > max_depth:
        return []

    suburls = get_url_suburl(url)
    data = []
    for suburl in suburls:
        if pbar is not None:
            pbar.set_description(f"Processing {suburl}")
        suburl_data = {
            "depth": depth + 1,
            "url": suburl,
            "title": get_url_title(suburl),
            "suburls": get_url_suburl_data(suburl, depth + 1, max_depth),
        }
        data.append(suburl_data)
        if pbar is not None:
            pbar.update(1)
    return data


def main():
    url = "https://sqlmap.highlight.ink/"
    max_depth = 1
    with tqdm(total=len(get_url_suburl(url))) as pbar:
        pbar.set_description("Processing")
        data = {
            "depth": 0,
            "url": url,
            "title": get_url_title(url),
            "suburls": get_url_suburl_data(url, 0, max_depth, pbar),
        }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
