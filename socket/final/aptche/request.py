from urllib.parse import parse_qs


class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]
        self.query_string = environ["QUERY_STRING"]
        self.headers = self._parse_headers(environ)
        self.body = environ["wsgi.input"].read().decode("utf-8")
        self.params = self._parse_query_string()
        self.data = self._parse_form()

    def _parse_headers(self, environ):
        headers = {}
        for key, value in environ.items():
            if key.startswith("HTTP_"):
                headers[key[5:].replace("_", "-").title()] = value
        return headers

    def _parse_query_string(self):
        return parse_qs(self.query_string)

    def _parse_form(self):
        if self.method == "POST":
            return parse_qs(self.body)
        return {}
