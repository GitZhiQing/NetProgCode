import socket
import json as json_lib
from urllib.parse import urlencode
from .response import Response
import uuid


class HttpClient:
    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.settimeout(10)

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
        header, body = response.split("\r\n\r\n", 1)
        header_lines = header.split("\r\n")
        status_line = header_lines[0]
        status_code = int(status_line.split(" ")[1])
        reason = status_line.split(" ", 2)[2]
        headers = {}
        for line in header_lines[1:]:
            key, value = line.split(": ", 1)
            headers[key] = value
        return Response(self.host, status_code, reason, headers, body.encode())

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
            request_message += data

        self.socket.sendall(request_message.encode())
        response = b""
        while True:
            try:
                recv = self.socket.recv(4096)
                if not recv:
                    break
                response += recv
            except socket.timeout:
                break

        return self.parse_response(response.decode())

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
            data = ""
            for key, value in files.items():
                data += f"--{boundary}\r\n"
                data += f'Content-Disposition: form-data; name="{key}"; filename="{key}"\r\n'
                data += "Content-Type: application/octet-stream\r\n\r\n"
                data += value + "\r\n"
            data += f"--{boundary}--\r\n"

            if not headers:
                headers = {}
            headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"

        return self.send_request("POST", path, data=data, headers=headers)

    def close(self):
        self.socket.close()
