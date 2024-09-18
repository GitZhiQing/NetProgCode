"""
f: 论坛 p: 主贴 rp: 回帖 cp: 评论
"""

import json
import os
import re
import sys
import time

from bs4 import BeautifulSoup
import requests

session = requests.Session()


def get_soup(url, headers):
    """
    获取 soup 对象
    """
    try:
        response = session.get(url, headers=headers)  # 使用session
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None


def get_image(url, path):
    """
    下载图片
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print(f"下载图片：{url}")
        with session.get(url) as response:
            if response.status_code == 200:
                with open(path, "wb") as f:
                    f.write(response.content)
    except requests.RequestException as e:
        print(f"图片下载错误: {e}")


def get_p_meta(p_id, headers):
    """
    获取主帖元数据
    """
    url = f"https://tieba.baidu.com/p/{p_id}"
    print(f"获取主帖元数据：{url}")
    soup = get_soup(url, headers)

    p_ele = soup.find("div", class_="content")
    f_id = re.search(r'"forum_id":(\d+)', str(soup)).group(1)
    f_name = (
        p_ele.find("a", class_="card_title_fname").text.strip()
        if p_ele.find("a", class_="card_title_fname")
        else ""
    )
    p_title = (
        p_ele.find(["h1", "h2", "h3"], class_="core_title_txt").text.strip()
        if p_ele.find(["h1", "h2", "h3"], class_="core_title_txt")
        else ""
    )
    p_author_username = (
        p_ele.find("div", class_="louzhubiaoshi").get("author")
        if p_ele.find("div", class_="louzhubiaoshi")
        else ""
    )
    p_author_nickname = (
        p_ele.find("a", class_="p_author_name").text.strip()
        if p_ele.find("a", class_="p_author_name")
        else ""
    )
    p_r_num_ele = (
        p_ele.find("li", class_="l_reply_num")
        if p_ele.find("li", class_="l_reply_num")
        else ""
    )
    p_rp_num, p_rp_page_num = [
        span.text.strip() for span in p_r_num_ele.find_all("span", class_="red")
    ]

    return {
        "f_id": f_id,
        "f_name": f_name,
        "p_id": p_id,
        "p_title": p_title,
        "p_author_username": p_author_username,
        "p_author_nickname": p_author_nickname,
        "p_rp_num": p_rp_num,
        "p_rp_page_num": p_rp_page_num,
    }


def get_rp_list(f_id, p_id, pn, headers):
    """
    获取回帖列表
    """
    rp_list = []

    for page in range(1, int(pn) + 1):
        url = f"https://tieba.baidu.com/p/{p_id}?pn={page}"
        print(f"获取第 {page} 页回帖：{url}")
        soup = get_soup(url, headers)
        rp_ele_list = soup.find_all("div", class_="l_post")
        for rp_ele in rp_ele_list:
            rp_data = json.loads(rp_ele.get("data-field", "{}").replace("&quot;", '"'))
            rp_id = rp_data.get("content", {}).get("post_id", "")
            rp_author_id = rp_data.get("author", {}).get("user_id", "")
            rp_author_username = rp_data.get("author", {}).get("user_name", "")
            rp_author_nickname = (
                rp_ele.find("a", class_="p_author_name").text.strip()
                if rp_ele.find("a", class_="p_author_name")
                else ""
            )
            rp_author_ip_addr = rp_data.get("content", {}).get("ip_address", "")
            rp_comment_num = rp_data.get("content", {}).get("comment_num", 0)
            rp_no = rp_data.get("content", {}).get("post_no", 0)
            rp_date = rp_data.get("content", {}).get("date", 0)
            rp_content = (
                rp_ele.find("div", class_="d_post_content")
                .decode_contents(formatter="html")
                .strip()
                if rp_ele.find("div", class_="d_post_content")
                else ""
            )
            rp_content_img_url_list = [
                img.get("src") for img in rp_ele.find_all("img", class_="BDE_Image")
            ]
            rp_content_img_path_list = [
                f"./data/img/{p_id}/{rp_id}_{rp_no}/{img_url.split('/')[-1].split('?')[0]}"
                for img_url in rp_content_img_url_list
            ]
            for img_url in rp_content_img_url_list:
                img_path = f"./data/img/{p_id}/{rp_id}_{rp_no}/{img_url.split('/')[-1].split('?')[0]}"
                get_image(img_url, img_path)
                rp_content = rp_content.replace(img_url, img_path)

            if rp_comment_num > 0:
                rp_comment_page_num = (rp_comment_num - 1) // 10 + 1
                rp_comment_list = get_cp_list(
                    f_id, p_id, rp_id, rp_comment_page_num, headers
                )
            else:
                rp_comment_list = []

            rp_list.append(
                {
                    "rp_id": rp_id,
                    "rp_author_id": rp_author_id,
                    "rp_author_username": rp_author_username,
                    "rp_author_nickname": rp_author_nickname,
                    "rp_author_ip_addr": rp_author_ip_addr,
                    "rp_content": rp_content,
                    "rp_content_img_url_list": rp_content_img_url_list,
                    "rp_content_img_path_list": rp_content_img_path_list,
                    "rp_comment_num": rp_comment_num,
                    "rp_comment_list": rp_comment_list,
                    "rp_no": rp_no,
                    "rp_date": rp_date,
                }
            )

    return rp_list


def get_cp_list(f_id, p_id, rp_id, pn, headers):
    """
    获取评论列表
    """
    cp_list = []

    for page in range(1, int(pn) + 1):
        url = f"https://tieba.baidu.com/p/comment?tid={p_id}&pid={rp_id}&pn={page}&fid={f_id}&t={int(time.time()*1000)}"
        print(f"获取回帖 {rp_id} 第 {page} 页评论：{url}")
        soup = get_soup(url, headers)
        cp_ele_list = soup.find_all("li", class_="lzl_single_post")
        for cp_ele in cp_ele_list:
            cp_data = json.loads(cp_ele.get("data-field", "{}"))
            cp_author_username = cp_data.get("user_name", "")
            cp_author_nickname = cp_data.get("showname", "")
            cp_author_icon_url = cp_ele.find("img").get("src")
            cp_content = (
                cp_ele.find("span", class_="lzl_content_main").text.strip()
                if cp_ele.find("span", class_="lzl_content_main")
                else ""
            )
            if cp_content.startswith("回复"):
                cp_to_username = (
                    cp_ele.find("a", class_="at").text.strip()
                    if cp_ele.find("a", class_="at")
                    else ""
                )
            else:
                cp_to_username = ""

            cp_date = (
                cp_ele.find("span", class_="lzl_time").text.strip()
                if cp_ele.find("span", class_="lzl_time")
                else ""
            )

            cp_list.append(
                {
                    "cp_author_username": cp_author_username,
                    "cp_author_nickname": cp_author_nickname,
                    "cp_author_icon_url": cp_author_icon_url,
                    "cp_content": cp_content,
                    "cp_to_username": cp_to_username,
                    "cp_date": cp_date,
                }
            )

    return cp_list


def main(url):
    if not url:
        sys.exit("请输入帖子 URL！")

    p_id = url.split("/")[-1]

    with open("./data/headers.json", "r", encoding="utf-8") as f:
        headers = json.load(f)

    p_data = {}

    # 获取主贴元数据
    p_meta = get_p_meta(p_id, headers)
    p_data["p_meta"] = p_meta

    # 获取回帖
    rp_list = []
    rp_list.extend(get_rp_list(p_meta["f_id"], p_id, p_meta["p_rp_page_num"], headers))
    p_data["rp_list"] = rp_list

    # 写文件
    with open(f"./data/{p_id}.json", "w", encoding="utf-8") as f:
        json.dump(p_data, f, ensure_ascii=False, indent=4)

    print("All Done!")
    return p_data


if __name__ == "__main__":
    # main(url="https://tieba.baidu.com/p/xxxxxxxxxx")
    main(url=input("请输入帖子 URL："))
