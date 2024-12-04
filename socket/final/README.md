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

- 项目名称：Aptche
- 项目模块：
  - Aptche HTTP Server: 基于 asyncio 实现的 WSGI 服务器
  - Aptche Web Framework: 基于 Aptche HTTP Server 实现的 Web 框架
  - Aptche TODO List: 基于 Aptche Web Framework 实现的 TODO List

## 运行项目

Aptche.wsgi 模块的 [`__init__`](./aptche/wsgi/__init__.py) 文件中的 settings 字典，可自行修改配置。

若设置 `settings.HTTPS` 为 `True`，则需要在 `certs` 目录下提供**私钥&证书文件**，建议使用项目 [FiloSottile/mkcert](https://github.com/FiloSottile/mkcert) 生成自签名证书。

```bash
# 生成证书，该证书适用于 localhost、127.0.0.1、::1、<主机实际上网网卡 IP>
.\mkcert-v1.4.4-windows-amd64.exe localhost 127.0.0.1 ::1 <主机实际上网网卡 IP>
# 安装证书，执行这一步后，浏览器会信任生成的证书
.\mkcert-v1.4.4-windows-amd64.exe -install
```

Aptche TODO List 可以直接运行。

```bash
python demo.py
```

## 项目答辩

[演示](./DEFENSE/Aptche.pdf) [文稿](./DEFENSE/SCRIPT.md)
