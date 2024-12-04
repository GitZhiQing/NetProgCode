import os
import my_requests
import time


targets = [
    "https://www.bing.com/",
    "https://www.baidu.com/",
    "https://www.google.com/",
]

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}


for target in targets:
    my_resp = my_requests.get(
        target, proxies=proxies, headers={"User-Agent": "Mozilla/5.0"}
    )
    if my_resp.status_code == 200:
        print(f"成功访问 {target}")
        if not my_resp.encoding:
            my_resp.encoding = my_resp.apparent_encoding
        file_name = target.split(".")[1].split(".")[0] + ".html"
        # 确认 data 目录存在
        if not os.path.exists("./data"):
            os.makedirs("./data")
        file_path = f"./data/{file_name}"
        with open(file_path, "w", encoding=my_resp.encoding) as f:
            f.write(my_resp.text)
    else:
        print(f"访问 {target} 失败")
        print(f"状态码: {my_resp.status_code}")
        print(f"原因: {my_resp.reason}")
        print(f"响应头: {my_resp.headers}")
        print(f"响应体: {my_resp.content}")
    time.sleep(0.2)
