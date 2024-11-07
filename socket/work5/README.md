# 实验五

基于 TCP 的网页请求。需模拟一个 TCP Client，完成基于 https 的网页请求。要求能够正确构造请求，并能够解析网页，最后以 html 的形式保存 (目标网站不少于三个)。

---

`-X`: 指定请求方法，支持 GET 和 POST
`-F`: 指定二进制文件（eg: `-F 'file=@/path/to/file'` or `-F '@/path/to/file'`）
`-O`: 指定保存文件名（eg: `-O /path/to/file`），默认为 URL 的最后一部分
`-d`: 指定请求体（eg: `-d 'key=value'` or `-d 'value'`）

支持 HTTP & HTTPS 请求，支持 GET & POST 请求，能够根据 MIME 类型将响应体保存为对应的文件。

---

请求体格式：

```http
GET {uri} HTTP/1.1
Host: {host}
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36
Accept: */*
Connection: close


```
