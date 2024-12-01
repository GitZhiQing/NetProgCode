# aptche/web.py
import re
import os

from aptche import utils


class Aptche:
    def __init__(self):
        self.routes = {}

    def route(self, path: str):
        def decorator(func):
            self.routes[path] = func
            return func

        return decorator

    def __call__(self, environ, start_response):
        """
        __call__ 方法是 WSGI 应用程序的入口，当有请求到达时，WSGI 服务器会调用这个方法。
        """
        path = environ["PATH_INFO"]
        for route, func in self.routes.items():
            match = re.fullmatch(
                route.replace("<", "(?P<").replace(">", ">[^/]+)"), path
            )
            if match:
                start_response("200 OK", [("Content-Type", "text/html")])
                return [func(**match.groupdict()).encode("utf-8")]
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"404 Not Found"]


def render_template(template_name: str, **context):
    template_path = os.path.join(os.path.dirname(__file__), "templates")
    with open(os.path.join(template_path, template_name), "r", encoding="utf-8") as f:
        template = f.read()
    for key, value in context.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template
