# 实验五

基于 TCP 的网页请求。需模拟一个 TCP Client，完成基于 https 的网页请求。要求能够正确构造请求，并能够解析网页，最后以 html 的形式保存 (目标网站不少于三个)。

---

**成果**：一个 socket 实现的简单的 requests 库。

**示例**：

```python
import my_requests
import json as json_lib


url = "https://example.com/"

response = my_requests.get(url)
print(response.url)
print(response.status_code)
print(response.reason)
print(response.headers)
print(response.apparent_encoding)
print(response.encoding)
print(response.content)
print(response.text)
try:
    json_data = response.json()
    print(json_data)
except json_lib.JSONDecodeError:
    print("响应内容不是有效的 JSON 数据")
```
