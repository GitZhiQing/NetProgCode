import socket
import mimetypes
import os
import datetime
import threading
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] - %(message)s")

HOST = "127.0.0.1"
PORT = 9999
WEB_ROOT = os.path.join(os.path.dirname(__file__), "html")
CRLF = "\r\n"
SERVER_NAME = "Seeker dev"


def get_content_type(file_path):
    """
    根据文件路径获取文件的 MIME 类型
    """
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or "application/octet-stream"


def get_gmt_date():
    """
    获取当前时间的 GMT 格式
    """
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )


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
    while True:
        data = conn.recv(1024)
        raw_request += data
        if len(data) < 1024:
            break
    raw_request = raw_request.decode("utf-8")
    request = {"line": {}, "headers": {}}
    request_lines = raw_request.split(CRLF)
    (
        request["line"]["method"],
        request["line"]["uri"],
        request["line"]["version"],
    ) = request_lines[0].split(" ")
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
    response.append(CRLF)
    response = CRLF.join(response)  # 将列表中的每个元素用 CRLF 连接起来

    # 回复体均为字节类型
    if isinstance(body, str):
        body = body.encode("utf-8")

    return response.encode("utf-8") + body


def handle_client(conn, addr):
    with conn:
        status = 200
        request = make_request(conn)
        uri = request["line"]["uri"]
        if uri == "/":
            uri = "/index.html"
        file_path = os.path.join(WEB_ROOT, uri[1:])
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file = f.read()
                content_type = get_content_type(file_path)
                headers = {
                    "Server": SERVER_NAME,
                    "Date": get_gmt_date(),
                    "Content-Type": content_type,
                    "Content-Length": len(file),
                    "Connection": "close",
                }
                response = make_response(status, headers, file)
        else:
            headers = {
                "Server": SERVER_NAME,
                "Date": get_gmt_date(),
                "Connection": "close",
            }
            status = 404
            response = make_response(status, headers, "404 Not Found")

        # 打印 HTTP 请求日志
        logging.info(
            f'{addr[0]}:{addr[1]} - "{request["line"]["method"]} {request["line"]["uri"]} {request["line"]["version"]}" {status} - "{request["headers"].get("user-agent", "")}"'
        )

        conn.sendall(response)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(
            f"[*] 服务已启动: http://{HOST}:{PORT}\n[*] 站点根目录: {WEB_ROOT}\n[*] 服务器名称: {SERVER_NAME}"
        )
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    main()
