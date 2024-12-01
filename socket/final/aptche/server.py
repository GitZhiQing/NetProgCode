# aptche/server.py
import socket

from aptche import utils, logging
from aptche.web import Aptche


class AptcheServer:
    def __init__(self, app: Aptche):
        self.app = app
        self.request = None
        self.response = None

    def start_response(self, status: str, headers: list):
        self.status = status
        self.headers = headers
        status_line = f"HTTP/1.1 {status}\r\n"
        header_lines = [f"{key}: {value}\r\n" for key, value in headers]
        self.response = status_line + "".join(header_lines) + "\r\n"

    def make_request(self, request_raw: bytes) -> dict:
        """
        根据 request_raw 构造 request 对象
        """
        request = request_raw.decode("iso-8859-1")
        request_line, headers, body = request.split("\r\n", 2)
        method, path, version = request_line.split(" ")
        headers = [
            {"key": header.split(": ")[0], "value": header.split(": ")[1]}
            for header in headers.split("\r\n")
        ]
        return {
            "request_line": {
                "method": method,
                "path": path,
                "version": version,
            },
            "request_headers": headers,
            "request_body": body,
        }

    def run(self, schema: str = "http", host: str = "0.0.0.0", port: int = 80):
        """
        启动 WSGI 服务器
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(128)

        if host == "0.0.0.0":
            host = socket.gethostbyname(socket.gethostname())
            logging.info("* 服务运行在所有地址 (0.0.0.0)")
            logging.info(f"* 访问地址: {schema}://{host}:{port}")
            logging.info(f"* 访问地址: {schema}://127.0.0.1:{port}")
        else:
            logging.info(f"* 服务运行在 {host}")
            logging.info(f"* 访问地址: {schema}://{host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            try:
                request_raw = b""
                while True:
                    chunk = client_socket.recv(1024)
                    request_raw += chunk
                    if len(chunk) < 1024:
                        break
                request = self.make_request(request_raw)
                environ = {
                    "REQUEST_METHOD": request["request_line"]["method"],
                    "PATH_INFO": request["request_line"]["path"],
                    "SERVER_PROTOCOL": request["request_line"]["version"],
                    "wsgi.version": (1, 0),
                    "wsgi.url_scheme": "http",
                    "wsgi.input": request["request_body"],
                    "wsgi.errors": None,
                    "wsgi.multithread": False,  # 单线程
                    "wsgi.multiprocess": False,  # 单进程
                    "wsgi.run_once": False,  # 长连接
                    "SERVER_NAME": "Aptche",
                    "SERVER_PORT": str(port),
                    "REMOTE_ADDR": client_address[0],
                    "REMOTE_PORT": str(client_address[1]),
                    "SCRIPT_NAME": "",
                }
                content = self.app(environ, self.start_response)
                response_body = b"".join(
                    chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
                    for chunk in content
                )
                content_length = len(response_body)
                content_type = utils.get_content_type_by_content(response_body)
                headers = [
                    ("Date", utils.get_gmt_date()),
                    ("Content-Length", str(content_length)),
                    ("Content-Type", content_type),
                ]
                headers.extend(self.headers)
                self.start_response(self.status, headers)
                client_socket.sendall(self.response.encode("utf-8") + response_body)
            except Exception as e:
                logging.error(e)
                client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
            finally:
                client_socket.close()
