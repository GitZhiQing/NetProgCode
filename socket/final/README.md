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

其中，
---

预期 demo:

```python
from aptche.web import Aptche, render_template

app = Aptche()


@app.route("/<name>")
def index(name):
    if name:
        return render_template("index.html", name=name, app="Aptche")


@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    app.run()
```

---


