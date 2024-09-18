import html
import json
import os
import re
import sys
import time

from bs4 import BeautifulSoup
import requests

session = requests.Session()


def get_soup(url, headers, proxy=False):
    """
    获取 soup 对象
    """
    proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
    try:
        # 默认不使用代理
        response = session.get(url, headers=headers, proxies=proxies if proxy else None)
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None


def get_b_info(b_id, headers):
    """
    获取书籍信息
    """
    url = f"https://www.3bqg.cc/book/{b_id}/"
    print(f"获取书籍信息：{url}")
    soup = get_soup(url, headers)

    b_info_ele = soup.find("div", class_="info")
    b_name = b_info_ele.find("h1").text.strip()
    b_author = b_info_ele.find_all("span")[0].text.strip()
    b_status = b_info_ele.find_all("span")[1].text.strip()
    b_utime = b_info_ele.find_all("span")[2].text.strip()
    b_cnum = int(
        b_info_ele.find_all("span")[3]
        .find("a")
        .get("href")
        .split("/")[-1]
        .split(".")[0]
    )
    b_intro = b_info_ele.find("dd").text.strip()
    b_cover = b_info_ele.find("img").get("src")

    cover_path = f"../data/{b_id}/cover.jpg"
    os.makedirs(os.path.dirname(cover_path), exist_ok=True)
    with open(cover_path, "wb") as f:
        f.write(requests.get(b_cover).content)

    info_path = f"../data/{b_id}/info.json"
    os.makedirs(os.path.dirname(info_path), exist_ok=True)
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "b_id": b_id,
                "b_name": b_name,
                "b_author": b_author,
                "b_status": b_status,
                "b_utime": b_utime,
                "b_cnum": b_cnum,
                "b_intro": b_intro,
                "b_cover": b_cover,
            },
            f,
            ensure_ascii=False,
            indent=4,
        )

    return {
        "b_id": b_id,
        "b_name": b_name,
        "b_author": b_author,
        "b_status": b_status,
        "b_utime": b_utime,
        "b_cnum": b_cnum,
        "b_intro": b_intro,
        "b_cover": b_cover,
    }


def get_b_chapter_data(b_id, cnum, headers):
    """
    获取书籍章节数据
    """
    for c in range(1, int(cnum) + 1):
        url = f"https://www.3bqg.cc/book/{b_id}/{c}.html"
        print(f"获取章节数据：{url}")
        soup = get_soup(url, headers)

        name = soup.find("h1").text.strip()
        content = soup.find("div", id="chaptercontent").decode_contents(
            formatter="html"
        )
        parts = content.split("<br/><br/>")
        content = "<br/><br/>".join(parts[:-2])  # 去除最后两个无用部分（广告等）
        content = re.sub(r"<br/><br/>", "\n", content)  # 转换换行符
        content = html.unescape(content)  # 转换 HTML 实体字符

        # 保存章节数据
        path = f"../data/{b_id}/chapters/{c}.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{name}\n{content}\n\n")


def main(url):
    if not url:
        print("请输入书籍 URL！")
        sys.exit(1)

    b_id = url.split("/")[-2]

    with open("../data/headers.json", "r", encoding="utf-8") as f:
        headers = json.load(f)

    b_info = get_b_info(b_id, headers)

    if not b_info:
        print("获取书籍信息失败！")
        sys.exit(1)

    b_chapter_start_num = int(input("请输入开始章节序号（默认值：1）：") or 1)
    b_chapter_end_num = int(
        input(f"请输入结束章节序号（默认值：{b_info['b_cnum']}）：") or b_info["b_cnum"]
    )

    get_b_chapter_data(b_id, b_info["b_cnum"], headers)


if __name__ == "__main__":
    main(str(input("请输入小说主页 URL：") or "https://www.3bqg.cc/book/11906/"))
