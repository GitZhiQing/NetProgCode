# 期末作品

项目要求：

1. 自定义实现一个简单的 HTTP 服务器，能够处理基本的 HTTP 请求（如 GET、POST）。
2. 服务器能够解析请求 URI，根据请求类型读取静态文件或处理动态内容（如使用 Python 生成 HTML 页面）。
3. 实现 HTTP 客户端，能够发送 HTTP 请求到自定义服务器，并显示响应内容。
4. 引入 HTTPS 支持，使用 SSL/TLS 加密通信数据。
5. 支持 HTTP 持久连接（HTTP/1.1 Keep-Alive）和 HTTP/2 协议的部分特性。

加分项：

1. 实现 HTTP 缓存机制，减少不必要的服务器请求。
2. 支持 HTTP 压缩，如 gzip 压缩，减少网络传输数据量。
3. 设计并实现一个 Web 框架，基于自定义的 HTTP 服务器，提供路由、模板渲染等功能。

---

## 项目介绍

项目名称：Aptche

开发思路：参考 WSGI 规范，实现一个 WSGI 服务器，同时参考 Flask 语法，实现一个简单的 Web 框架。

WSGI 服务器和 Web 框架相互配合实现了一个简单的 HTTP 服务器，支持路由、模板渲染等功能。

WSGI 服务器和 Web 框架作为 Aptche 的两个模块（`aptche.server` 和 `aptche.web`），分别实现了 WSGI 服务器和 Web 框架的功能。

---

预期 demo:

```python
from aptche.server import AptcheServer
from aptche.web import Aptche

app = Aptche()

@app.route('/')
def index():
    return 'Hello, Aptche!'

@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}!'

server = AptcheServer(app)
server.run(host='0.0.0.0', port=8080)
```

---

AptcheServer 和 Aptche 的大致实现：

```python
# aptche/server.py
import socket
from aptche.web import Aptche

class AptcheServer:
    def __init__(self, app: Aptche):
        self.app = app

    def start_response(self, status: str, headers: list):
        self.status = status
        self.headers = headers
        status_line = f'HTTP/1.1 {status}\r\n'
        header_lines = [f'{key}: {value}\r\n' for key, value in headers]
        self.response = status_line + ''.join(header_lines) + '\r\n'

    def run(self, host: str, port: int):
        # 启动 WSGI 服务器
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(128)
        while True:
            client_socket, client_address = server_socket.accept()
            request = client_socket.recv(1024).decode('utf-8')
            environ = {
                'REQUEST_METHOD': request.split(' ')[0],
                'PATH_INFO': request.split(' ')[1],
                'SERVER_PROTOCOL': request.split(' ')[2],
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'http',
                'wsgi.input': request,
                'wsgi.errors': None,
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
                'wsgi.run_once': False,
                'SERVER_NAME': host,
                'SERVER_PORT': str(port),
                'REMOTE_ADDR': client_address[0],
                'REMOTE_PORT': str(client_address[1]),
                'SCRIPT_NAME': ''
            }
            content = self.app(environ, self.start_response)
            client_socket.sendall(self.response.encode('utf-8') + content.encode('utf-8'))
            client_socket.close()
```

```python
# aptche/web.py

class Aptche:
    def __init__(self):
        self.routes = {}

    def route(self, path: str):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        func = self.routes.get(path)
        if func is None:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'404 Not Found']
        content = func()
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [content.encode('utf-8')]
```
