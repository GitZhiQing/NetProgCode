from .utils import get_content_type_by_content, get_gmt_date

class Response:
    def __init__(self, body, status="200 OK", headers=None):
        self.body = body
        self.status = status
        self.headers = headers or []
        self._set_default_headers()

    def _set_default_headers(self):
        if isinstance(self.body, str):
            self.headers.append(("Content-Type", "text/html; charset=utf-8"))
        elif isinstance(self.body, bytes):
            self.headers.append(
                ("Content-Type", get_content_type_by_content(self.body))
            )
        self.headers.append(("Date", get_gmt_date()))

    def __call__(self, environ, start_response):
        start_response(self.status, self.headers)
        if isinstance(self.body, str):
            return [self.body.encode("utf-8")]
        elif isinstance(self.body, bytes):
            return [self.body]
        return [self.body]