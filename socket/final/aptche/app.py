import os

from jinja2 import Environment, FileSystemLoader

from . import utils
from .request import Request
from .response import Response
from .router import Router


class Aptche:
    def __init__(self, template_folder="templates", static_folder="static"):
        self.router = Router(self)
        self.template_folder = template_folder
        self.static_folder = static_folder
        self.jinja_env = Environment(loader=FileSystemLoader(self.template_folder))

    def route(self, path, methods=None):
        if methods is None:
            methods = ["GET"]

        def decorator(func):
            self.router.add_route(path, func, methods)
            return func

        return decorator

    def render_template(self, template_name, **context):
        template = self.jinja_env.get_template(template_name)
        return template.render(context)

    def send_static_file(self, filename):
        file_path = os.path.join(self.static_folder, filename)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            return Response(
                content,
                headers=[
                    ("Content-Type", utils.get_content_type_by_file_path(file_path))
                ],
            )
        return Response("File Not Found", status="404 Not Found")

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.router.handle_request(request)
        return response(environ, start_response)
