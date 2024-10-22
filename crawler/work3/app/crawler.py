import json
import os
import re
import time
import urllib3
import warnings

import requests
from bs4 import BeautifulSoup
from rich.progress import Progress
from urllib3.exceptions import InsecureRequestWarning
from bs4 import XMLParsedAsHTMLWarning

# 过滤警告
warnings.filterwarnings("ignore", category=InsecureRequestWarning)
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def get_soup(url, proxy=False):
    """
    获取 soup 对象
    默认不使用代理，从 headers.json 中加载必要请求头
    """
    try:
        proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
        current_dir = os.path.dirname(os.path.abspath(__file__))
        headers_file_path = os.path.join(current_dir, "data", "headers.json")
        with open(headers_file_path, "r", encoding="utf-8") as f:
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
    获取 URL 的标题
    带有重试机制
    """
    for _ in range(retries):
        try:
            soup = get_soup(url, proxy=True)
            if soup is None or soup.title is None or soup.title.string is None:
                return "获取标题失败"
            return soup.title.string
        except requests.RequestException as e:
            print(f"请求错误: {e}")
            time.sleep(1)
    return "获取标题失败"


def get_url_suburl(url):
    """
    获取 url 的页面子链接
    使用集合去重
    """
    soup = get_soup(url, proxy=True)
    if soup is None:
        return None
    suburls = set()  # 使用集合去重
    for a in soup.find_all("a", href=True):
        suburl = a["href"]
        if re.match(r"^https?://", suburl):
            suburls.add(suburl)
    suburls.discard(url)
    return suburls


def get_url_suburl_data(url, depth, max_depth, progress=None, task_id=None):
    """
    获取 url 的页面子链接数据
    带有深度控制
    """
    if depth > max_depth:
        return []

    suburls = get_url_suburl(url)
    data = []

    for p, suburl in enumerate(suburls, 1):
        suburl_data = {
            "depth": depth + 1,
            "url": suburl,
            "title": get_url_title(suburl),
            "suburls": get_url_suburl_data(suburl, depth + 1, max_depth),
        }
        data.append(suburl_data)
        if progress is not None and task_id is not None:
            description = f"[green]正在处理子链接 ({p}/{len(suburls)}): {suburl} "
            progress.update(task_id, completed=p, description=description)

    return data


def main(url="https://sqlmap.highlight.ink/"):
    print(f"爬取目标: {url}")
    max_depth = 1
    suburls = get_url_suburl(url)
    if suburls is None:
        print("无法获取子链接")
        return

    with Progress() as progress:
        p, total = 0, len(suburls)
        description = f"[green]正在处理原始链接 ({url}) "
        task_id = progress.add_task(description.format(), total=total)
        data = {
            "depth": 0,
            "url": url,
            "title": get_url_title(url),
            "suburls": get_url_suburl_data(url, 0, max_depth, progress, task_id),
        }

    # 获取当前脚本文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 data.json 的绝对路径
    data_file_path = os.path.join(current_dir, "data", "data.json")
    with open(data_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main(url=input("请输入 URL: "))
