import socket
import socks
import json as json_lib
from urllib.parse import urlencode
from .response import Response
import uuid
import logging

logging.basicConfig(level=logging.INFO)


class HttpClient:
    def __init__(self, host, port=80, proxy=None):
        self.host = host
        self.port = port
        self.socket = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
        if proxy:
            proxy_type, proxy_addr, proxy_port = proxy
            self.socket.set_proxy(proxy_type, proxy_addr, proxy_port)
        try:
            self.socket.connect((host, port))
            self.socket.settimeout(10)
        except (socket.error, socks.ProxyError) as e:
            logging.error(f"Error connecting to {host}:{port} - {e}")
            raise

    def build_request_line(self, method, path):
        return f"{method} {path} HTTP/1.1\r\n"

    def build_header_lines(self, headers, data):
        header_lines = f"Host: {self.host}\r\n"
        if headers:
            for key, value in headers.items():
                header_lines += f"{key}: {value}\r\n"
        if data:
            header_lines += f"Content-Length: {len(data)}\r\n"
        header_lines += "Connection: keep-alive\r\n"
        header_lines += "\r\n"
        return header_lines

    def parse_response(self, response):
        try:
            header, body = response.split(b"\r\n\r\n", 1)
            header_lines = header.split(b"\r\n")
            status_line = header_lines[0].decode("iso-8859-1")
            status_code = int(status_line.split(" ")[1])
            reason = status_line.split(" ", 2)[2]
            headers = {}
            for line in header_lines[1:]:
                key, value = line.decode("iso-8859-1").split(": ", 1)
                headers[key] = value

            if headers.get("Transfer-Encoding") == "chunked":
                body = self._decode_chunked_body(body)

            return Response(self.host, status_code, reason, headers, body)
        except Exception as e:
            logging.error(f"Error parsing response - {e}")
            raise

    def _decode_chunked_body(self, body):
        decoded_body = b""
        while body:
            chunk_size_str, body = body.split(b"\r\n", 1)
            chunk_size = int(chunk_size_str, 16)
            if chunk_size == 0:
                break
            chunk, body = body[:chunk_size], body[chunk_size + 2 :]
            decoded_body += chunk
        return decoded_body

    def receive_response(self):
        response = b""
        self.socket.settimeout(10)  # 设置接收数据的超时时间
        try:
            while True:
                try:
                    data = self.socket.recv(1024)
                    if not data:
                        break
                    response += data

                    # Check if we have received the headers
                    if b"\r\n\r\n" in response:
                        headers, _ = response.split(b"\r\n\r\n", 1)
                        header_lines = headers.split(b"\r\n")
                        headers_dict = {}
                        for line in header_lines[1:]:
                            key, value = line.decode("iso-8859-1").split(": ", 1)
                            headers_dict[key] = value

                        # Check for Content-Length header
                        if "Content-Length" in headers_dict:
                            content_length = int(headers_dict["Content-Length"])
                            if len(response) >= len(headers) + 4 + content_length:
                                break

                        # Check for Transfer-Encoding: chunked
                        if headers_dict.get("Transfer-Encoding") == "chunked":
                            if response.endswith(b"0\r\n\r\n"):
                                break
                except socket.timeout:
                    logging.error("Receiving data timed out")
                    break

            return response
        except socket.error as e:
            logging.error(f"Error receiving response - {e}")
            raise

    def send_request(
        self, method, path, params=None, data=None, json=None, headers=None
    ):
        if params:
            path += "?" + urlencode(params)

        if json:
            data = json_lib.dumps(json)
            if not headers:
                headers = {}
            headers["Content-Type"] = "application/json"

        request_line = self.build_request_line(method, path)
        header_lines = self.build_header_lines(headers, data)

        request_message = request_line + header_lines
        if data:
            if isinstance(data, str):
                request_message += data
            else:
                request_message = request_message.encode() + data

        try:
            self.socket.sendall(
                request_message.encode()
                if isinstance(request_message, str)
                else request_message
            )
            response = self.receive_response()
            return self.parse_response(response)
        except (socket.error, socks.ProxyError) as e:
            logging.error(f"Error sending request - {e}")
            raise

    def get(self, path, params=None, headers=None):
        return self.send_request("GET", path, params=params, headers=headers)

    def post(self, path, data=None, json=None, files=None, headers=None):
        if json:
            data = json_lib.dumps(json)
            if not headers:
                headers = {}
            headers["Content-Type"] = "application/json"

        if files:
            boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
            body = b""
            for key, file in files.items():
                file_content = file.read()
                body += (
                    (
                        f"--{boundary}\r\n"
                        f'Content-Disposition: form-data; name="{key}"; filename="{file.name}"\r\n'
                        f"Content-Type: application/octet-stream\r\n\r\n"
                    ).encode()
                    + file_content
                    + b"\r\n"
                )
            body += f"--{boundary}--\r\n".encode()

            if not headers:
                headers = {}
            headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
            data = body

        return self.send_request("POST", path, data=data, headers=headers)

    def close(self):
        try:
            self.socket.close()
        except socket.error as e:
            logging.error(f"Error closing socket - {e}")
            raise
