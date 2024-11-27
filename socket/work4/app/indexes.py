import os


def get_dir_list(dir_path):
    """
    获取指定目录下的文件列表
    文件名，大小，类型（文件或文件夹）
    """
    dir_list = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isdir(file_path):
            dir_list.append((file_name, "dir"))
        else:
            file_size = os.path.getsize(file_path)
            dir_list.append((file_name, file_size))
    return dir_list


def get_index_html(dir_path):
    """
    生成目录页面的 HTML
    """
    dir_list = get_dir_list(dir_path)
    head = f"""
    <head>
    <meta charset="utf-8">
    <title>Index of {dir_path}</title>
    <style>
        table {{
            width: 80%;
            border-collapse: collapse;
        }}

        th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }}

        th {{
            background-color: #f2f2f2;
        }}
    </style>
    </head>
    """

    rows = ""
    # 添加返回上一级目录的链接
    rows += "<tr><td><a href='../'>../</a></td><td> - </td><td></td></tr>"

    for file_name, file_info in dir_list:
        if file_info == "dir":
            rows += f"<tr><td><a href='{file_name}/'>{file_name}/</a></td><td> - </td><td></td></tr>"
        else:
            rows += f"<tr><td><a href='{file_name}'>{file_name}</a></td><td>{file_info} bytes</td><td><a href='{file_name}' download>下载</a></td></tr>"

    return f"""
    <html>
    {head}
    <body>
        <h1>Index of {dir_path}</h1>
        <table>
        <tr><th>Name</th><th>Size</th><th style="width: 100px;">Download</th></tr>
        {rows}
        </table>
    </body>
    </html>"""


if __name__ == "__main__":
    from app import Config

    print(get_index_html(Config.WEB_ROOT))
