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
