import socket
import os
import threading

from app import Config, logging, indexes, deps


def get_status_line(status):
    """
    根据状态码返回状态行
    """
    status_code = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error",
    }
    return f"HTTP/1.1 {status} {status_code[status]}"


def make_request(conn):
    """
    将 socket 连接接收的数据进行解析为 HTTP 请求体字典
    """
    raw_request = b""
    while True:
        data = conn.recv(1024)
        raw_request += data
        if len(data) < 1024:
            break
    raw_request = raw_request.decode("utf-8")
    request = {"line": {}, "headers": {}}
    request_lines = raw_request.split("\r\n")

    request_line_parts = request_lines[0].split(" ")
    request["line"]["method"], request["line"]["uri"], request["line"]["version"] = (
        request_line_parts
    )
    for line in request_lines[1:]:
        if line == "":
            break
        key, value = line.split(": ")
        request["headers"][key.lower()] = value
    return request


def make_response(status, headers, body):
    """
    根据状态码、响应头和响应体生成 HTTP 响应
    """
    response = [get_status_line(status)]
    response.extend([f"{k}: {v}" for k, v in headers.items()])
    response.append("\r\n")
    response = "\r\n".join(response)

    if isinstance(body, str):
        body = body.encode("utf-8")

    return response.encode("utf-8") + body


def handle_root_request():
    """
    处理根目录请求
    """
    # 如果根目录下没有默认索引文件，则显示目录列表
    if not os.path.exists(os.path.join(Config.WEB_ROOT, Config.DEFAULT_INDEX)):
        dir_path = Config.WEB_ROOT
        file = indexes.get_index_html(dir_path).encode("utf-8")
        content_type = "text/html"
    # 否则返回默认索引文件
    else:
        file_path = os.path.join(Config.WEB_ROOT, Config.DEFAULT_INDEX)
        with open(file_path, "rb") as f:
            file = f.read()
            content_type = deps.get_content_type(file_path)
    headers = {
        "Server": Config.SERVER_NAME,
        "Date": deps.get_gmt_date(),
        "Content-Type": content_type,
        "Content-Length": len(file),
        "Connection": "close",
    }
    return make_response(200, headers, file)


def handle_directory_request(uri):
    """
    处理目录请求
    """
    dir_path = os.path.join(Config.WEB_ROOT, uri[1:])
    file = indexes.get_index_html(dir_path).encode("utf-8")
    content_type = "text/html"
    headers = {
        "Server": Config.SERVER_NAME,
        "Date": deps.get_gmt_date(),
        "Content-Type": content_type,
        "Content-Length": len(file),
        "Connection": "close",
    }
    return make_response(200, headers, file)


def handle_file_request(uri):
    """
    处理文件请求
    """
    file_path = os.path.join(Config.WEB_ROOT, uri[1:])
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            file = f.read()
            content_type = deps.get_content_type(file_path)
        headers = {
            "Server": Config.SERVER_NAME,
            "Date": deps.get_gmt_date(),
            "Content-Type": content_type,
            "Content-Length": len(file),
            "Connection": "close",
        }
        return make_response(200, headers, file)
    else:
        headers = {
            "Server": Config.SERVER_NAME,
            "Date": deps.get_gmt_date(),
            "Connection": "close",
        }
        return make_response(404, headers, "404 Not Found")


def handle_client(conn, addr):
    """
    处理 socket 客户端请求
    """
    status = 200
    request = None
    response = b""
    try:
        request = make_request(conn)
        uri = request["line"]["uri"]
        if uri == "/":
            response = handle_root_request()
        elif uri.endswith("/") and uri != "/":
            response = handle_directory_request(uri)
        else:
            response = handle_file_request(uri)
    except Exception as e:
        status = 500
        headers = {
            "Server": Config.SERVER_NAME,
            "Date": deps.get_gmt_date(),
            "Connection": "close",
        }
        response = make_response(status, headers, "500 Internal Server Error")
        logging.error(f"服务器错误: {e}")

    if request:
        logging.info(
            f'{addr[0]}:{addr[1]} - "{request["line"]["method"]} {request["line"]["uri"]} {request["line"]["version"]}" {status} - "{request["headers"].get("user-agent", "")}"'
        )
    else:
        logging.info(f"{addr[0]}:{addr[1]} - 请求解析失败，状态码: {status}")

    # 文件写更详细的日志
    with open("access.log", "a", encoding="utf-8") as f:
        if request:
            f.write(
                f'{addr[0]}:{addr[1]} - "{request["line"]["method"]} {request["line"]["uri"]} {request["line"]["version"]}" {status} - "{request["headers"].get("user-agent", "")}"\n'
            )
            f.write("请求头信息:\n")
            for key, value in request["headers"].items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
        else:
            f.write(f"{addr[0]}:{addr[1]} - 请求解析失败，状态码: {status}\n")

        f.write("响应头信息:\n")
        response_headers = (
            response.split(b"\r\n\r\n")[0].decode("utf-8").split("\r\n")[1:]
        )
        for header in response_headers:
            f.write(f"{header}\n")
        f.write("\n")

    try:
        conn.sendall(response)
    except OSError as e:
        logging.error(f"发送响应时出错: {e}")
    finally:
        conn.close()


def start():
    # 检查 WEB_ROOT 是否存在，不存在则创建
    if not os.path.exists(Config.WEB_ROOT):
        logging.info(f"[!] 站点根目录不存在: {Config.WEB_ROOT}")
        os.makedirs(Config.WEB_ROOT)
        logging.info(f"[+] 创建站点根目录: {Config.WEB_ROOT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((Config.HOST, Config.PORT))
        s.listen()
        print(
            f"[*] 服务已启动: http://{Config.HOST}:{Config.PORT}\n[*] 站点根目录: {Config.WEB_ROOT}\n[*] 服务器名称: {Config.SERVER_NAME}"
        )
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
