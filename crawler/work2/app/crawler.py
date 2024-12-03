import html
import json
import os
import re

from bs4 import BeautifulSoup
import requests

session = requests.Session()


def get_soup(url, proxy=False):
    """
    获取 soup 对象
    默认不使用代理，从 headers.json 中加载必要请求头
    """
    try:
        proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
        with open("headers.json", "r", encoding="utf-8") as f:
            headers = json.load(f)
        response = session.get(url, headers=headers, proxies=proxies if proxy else None)
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None


def get_b_info(b_id):
    """
    获取书籍信息
    保存到字典中返回
    """
    url = f"https://www.3bqg.cc/book/{b_id}/"
    print(f"获取书籍信息：{url}")

    soup = get_soup(url)
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

    # 保存封面
    cover_path = f"./app/static/book/{b_id}/cover.jpg"
    os.makedirs(os.path.dirname(cover_path), exist_ok=True)
    with open(cover_path, "wb") as f:
        # 使用 session 会被拦截，所以直接使用 requests
        f.write(requests.get(b_cover).content)

    # 保存书籍信息
    info_path = f"./app/static/book/{b_id}/info.json"
    os.makedirs(os.path.dirname(info_path), exist_ok=True)

    b_info = {
        "b_id": b_id,
        "b_name": b_name,
        "b_author": b_author,
        "b_status": b_status,
        "b_utime": b_utime,
        "b_cnum": b_cnum,
        "b_intro": b_intro,
        "b_cover": b_cover,
    }

    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(b_info, f, ensure_ascii=False, indent=4)

    return b_info


def get_b_chapter(b_id, c_start, c_end):
    """
    获取书籍章节数据
    将 c_id & c_name 保存到列表中返回
    """
    chapters = []
    for c in range(int(c_start), int(c_end) + 1):
        url = f"https://www.3bqg.cc/book/{b_id}/{c}.html"
        print(f"获取章节数据：{url}")

        soup = get_soup(url)
        name = soup.find("h1").text.strip()
        chapter_div = soup.find("div", id="chaptercontent")
        if chapter_div is None:
            print(f"未找到章节内容：{url}")
            continue
        content = chapter_div.decode_contents(formatter="html")
        parts = content.split("<br/><br/>")
        # 去除最后两个无用部分（广告等）
        content = "<br/><br/>".join(parts[:-2])
        # 转换换行符
        content = re.sub(r"<br/><br/>", "\n", content)
        # 转换 HTML 实体字符
        content = html.unescape(content)

        # 保存章节数据
        path = f"./app/static/book/{b_id}/chapter/{c}.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{name}\n{content}\n\n")

        chapters.append({"c_id": c, "c_name": name})

    return chapters
