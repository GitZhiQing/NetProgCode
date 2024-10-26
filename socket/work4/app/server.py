import socket
import os
import threading


from app import Config, logging, indexes, deps


def get_status_line(status):
    """
    根据状态码获取状态行
    """
    status_code = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error",
    }
    return f"HTTP/1.1 {status} {status_code[status]}"


def make_request(conn):
    """
    解析请求报文
    """
    raw_request = b""
    # 借助缓冲区，循环接收数据
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
    构造响应报文
    """
    response = [get_status_line(status)]
    response.extend([f"{k}: {v}" for k, v in headers.items()])
    response.append("\r\n")
    response = "\r\n".join(response)

    # 回复体均为字节类型
    if isinstance(body, str):
        body = body.encode("utf-8")

    return response.encode("utf-8") + body


def handle_client(conn, addr):
    status = 200
    request = None  # 初始化 request 变量
    response = b""  # 初始化 response 变量
    try:
        request = make_request(conn)
        uri = request["line"]["uri"]
        if uri == "/":
            # 判断 Config.DEFAULT_INDEX 是否存在，不存在则列目录
            if not os.path.exists(os.path.join(Config.WEB_ROOT, Config.DEFAULT_INDEX)):
                dir_path = Config.WEB_ROOT
                file = indexes.get_index_html(dir_path).encode("utf-8")
                content_type = "text/html"
                headers = {
                    "Server": Config.SERVER_NAME,
                    "Date": deps.get_gmt_date(),
                    "Content-Type": content_type,
                    "Content-Length": len(file),
                    "Connection": "close",
                }
                response = make_response(status, headers, file)
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
                    response = make_response(status, headers, file)
        # 如果路径以 “/” 结尾且不等于 “/” 则列目录
        elif uri.endswith("/") and uri != "/":
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
            response = make_response(status, headers, file)
        else:
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
                    response = make_response(status, headers, file)
            else:
                status = 404
                headers = {
                    "Server": Config.SERVER_NAME,
                    "Date": deps.get_gmt_date(),
                    "Connection": "close",
                }
                response = make_response(404, headers, "404 Not Found")
    except Exception as e:
        status = 500
        # 捕获异常并返回 500 状态码
        headers = {
            "Server": Config.SERVER_NAME,
            "Date": deps.get_gmt_date(),
            "Connection": "close",
        }
        response = make_response(status, headers, "500 Internal Server Error")
        logging.error(f"服务器错误: {e}")

    # 打印 HTTP 请求日志
    if request:
        logging.info(
            f'{addr[0]}:{addr[1]} - "{request["line"]["method"]} {request["line"]["uri"]} {request["line"]["version"]}" {status} - "{request["headers"].get("user-agent", "")}"'
        )
    else:
        logging.info(f"{addr[0]}:{addr[1]} - 请求解析失败，状态码: {status}")

    try:
        conn.sendall(response)
    except OSError as e:
        logging.error(f"发送响应时出错: {e}")
    finally:
        conn.close()


def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((Config.HOST, Config.PORT))
        s.listen()
        print(
            f"[*] 服务已启动: http://{Config.HOST}:{Config.PORT}\n[*] 站点根目录: {Config.WEB_ROOT}\n[*] 服务器名称: {Config.SERVER_NAME}"
        )
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
