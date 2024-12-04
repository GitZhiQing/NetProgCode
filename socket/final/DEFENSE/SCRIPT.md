## 项目介绍

项目名称：Aptche

开发思路：

- 参考 WSGI 规范，实现一个 WSGI 服务器（Aptche HTTP Server）。
- 参考 Flask 语法，实现一个简单的 Web 框架（Aptche Web Framework）。

再基于 Aptche Web 框架，实现一个简单的 TODO List。

![demo.png](imgs/demo.png)

---

答辩文档：

项目介绍：

- 项目名称：Aptche
- 项目模块：
  - Aptche HTTP Server: 基于 asyncio 实现的 WSGI 服务器
  - Aptche Web Framework: 基于 Aptche HTTP Server 实现的 Web 框架
  - Aptche TODO List: 基于 Aptche Web Framework 实现的 TODO List

### 开发思路 - Aptche HTTP Server

参考 WSGI 规范，实现一个 WSGI 服务器（Aptche HTTP Server）。

Aptche HTTP Server 基于 asyncio 实现，支持 HTTP/1.1 协议，实现了 HTTP 请求解析、HTTP 响应构造、支持基于 SSL/TLS 的 HTTPS 加密通信。得益于其异步 IO （AIO 模型）特性，Aptche HTTP Server 能够支持高并发的 HTTP 请求处理。

WSGI(Web Server Gateway Interface)，即 Web 服务器网关接口，是 Python 语言中定义的 Web 服务器和 Web 应用程序或框架之间的一种简单而通用的接口，在 [PEP 3333](https://www.python.org/dev/peps/pep-3333/) 中提出。WSGI 的目的是为了提供一种简单的方式，使得 Web 服务器和 Web 应用程序能够通过统一的接口进行通信。

WSGI 在运行时，会调用应用程序提供的一个可调用对象，即 Web 应用程序对象，该对象接收两个参数，分别是一个字典 `environ`（包含请求头信息）和一个可调用对象 `start_response`（用于发送响应数据）。

在本项目中，Aptche HTTP Server 会调用 Aptche Web Framework 提供的 Aptche 类的实例对象（app），将请求信息传递给 app，app 返回响应数据，然后 Aptche HTTP Server 将响应数据发送给客户端。

### 基于 SSL/TLS 的 HTTPS 加密连接

使用 mkcert(https://github.com/FiloSottile/mkcert) 工具生成自签名证书，并在本机安装证书。

然后在 Aptche HTTP Server 中加载密钥和证书证书文件，通过 ssl 模块的 `create_default_context` 方法创建 SSL 上下文，传入 asyncio 的 `start_server` 方法，即可实现 HTTPS 加密连接。

### 开发思路 - Aptche Web Framework

参考 Flask 语法，实现一个简单的 Web 框架（Aptche Web Framework）。

Aptche Web Framework 基于 Aptche HTTP Server 实现，提供路由、模板渲染等功能。Aptche Web Framework 的核心是 Aptche 类，Aptche 类的实例对象（app）是一个 WSGI 应用程序对象，接收请求信息，返回响应数据。

通过 Aptche HTTP Server 提供的 environ 字典，Aptche Web Framework 能够构造一个 request 对象，这个对象是处理后的便于使用的请求信息。

通过构造 route 装饰器，并创建一个 routes 列表来存储 URL 与处理函数的映射关系，Aptche Web Framework 能够根据请求 URL 找到对应的处理函数。

端点函数返回的数据会被传递给 response 对象，response 对象会根据数据类型自动构造响应数据，然后返回给 Aptche HTTP Server。

### 开发思路 - Aptche TODO List

再基于 Aptche Web 框架，实现一个简单的 TODO List。

基本同 Flask 的语法，通过 Aptche Web Framework 提供的路由功能，实现了一个简单的 TODO List，支持添加、删除、完成/未完成等基本功能。

### 参考文献

1. Python 软件基金会. PEP 3333 – Python Web Server Gateway Interface v1.0.1 [EB/OL]. (2010-09-26)[2024-12-03]. https://peps.python.org/pep-3333/.
2. 廖雪峰. WSGI 接口 - Python 教程 - 廖雪峰的官方网站[EB/OL]. [2024-12-03]. https://liaoxuefeng.com/books/python/web/wsgi/index.html.
3. Python 软件基金会. asyncio — Asynchronous I/O[EB/OL]. (2019)[2024-12-03]. https://docs.python.org/3/library/asyncio.html.
4. Flask 团队. Welcome to Flask — Flask Documentation (3.1.x)[EB/OL]. [2024-12-03]. https://flask.palletsprojects.com/en/stable/.
