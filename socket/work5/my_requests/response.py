import json as json_lib
import chardet


class Response:
    def __init__(self, url, status_code, reason, headers, content):
        self.url = url
        self.status_code = status_code
        self.reason = reason
        self.headers = headers
        self._content = content  # 响应体的原始字节数据
        self.encoding = (
            self._get_encoding_from_headers()
        )  # 从响应头中提取的编码，可由用户指定，将被用于 text 属性的解码

    def _get_encoding_from_headers(self):
        content_type = self.headers.get("Content-Type", "")
        if "charset=" in content_type:
            return content_type.split("charset=")[1]
        return None

    @property
    def apparent_encoding(self):
        """
        返回响应体的编码，由 chardet 模块检测得到
        """
        return chardet.detect(self._content)["encoding"]

    @property
    def text(self):
        return self._content.decode(self.encoding or "utf-8", errors="replace")

    @property
    def content(self):
        return self._content

    def json(self):
        return json_lib.loads(self.text)
