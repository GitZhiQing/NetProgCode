import html, json, os, re, sys, time, re


from bs4 import BeautifulSoup
import requests

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


session = requests.Session()


def get_soup(url, headers=None, proxy=False):
    """
    获取 soup 对象
    """
    proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
    try:
        response = session.get(
            url, headers=headers, proxies=proxies if proxy else None, verify=False
        )
        # 检查是否发送重定向，如有，跟随重定向并重新获取 soup 对象
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None


def remove_useless_url(url_list):
    """
    删除无效的 url
    """
    useful_url_list = []
    useless_url_list = ["javascript:void(0)", "javascript:;", "/", "#"]
    for url in url_list:
        if url is not None and url not in useless_url_list:
            # "//" 开头的 url，补全协议
            if url.startswith("//"):
                url = "http:" + url
            useful_url_list.append(url.strip())
    return useful_url_list


if __name__ == "__main__":
    with open("base_headers.json", "r", encoding="utf-8") as f:
        base_headers = json.load(f)
    url = "https://www.baidu.com"
    soup = get_soup(url, base_headers)
    hyperlink_ele_list = soup.find_all("a")
    hyperlink_list = remove_useless_url([ele.get("href") for ele in hyperlink_ele_list])
    # 写入 json 文件
    with open("hyperlink_list.json", "w", encoding="utf-8") as f:
        json.dump(hyperlink_list, f, ensure_ascii=False, indent=4)
    for url in hyperlink_list:
        print(url, end="\t")
        soup = get_soup(url)
        if soup is None:
            print(f"请求 URL {url} 失败")
            continue  # 如果 soup 是 None，跳过当前迭代
        print(soup.title.text.strip() if soup.title else "无标题")
