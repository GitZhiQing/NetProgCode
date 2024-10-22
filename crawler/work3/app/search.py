import json
import os


def search(keyword):
    # 获取当前脚本文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 data.json 的绝对路径
    data_file_path = os.path.join(current_dir, "data", "data.json")

    with open(data_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def search_data(data):
        result = []
        if keyword in data["title"]:
            result.append({"url": data["url"], "title": data["title"]})
        for suburl in data.get("suburls", []):
            result.extend(search_data(suburl))
        return result

    return search_data(data)
