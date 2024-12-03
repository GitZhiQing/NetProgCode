from .response import Response


class Router:
    def __init__(self, app):
        self.routes = {}
        self.app = app

    def add_route(self, path, func, methods):
        self.routes[path] = {"func": func, "methods": methods}

    def handle_request(self, request):
        route = self.routes.get(request.path)
        if route:
            if request.method in route["methods"]:
                response = route["func"](request)
                if isinstance(response, str):
                    return Response(response)
                elif isinstance(response, dict):
                    return Response(
                        self.app.render_template(
                            response["template"], **response["context"]
                        )
                    )
                return response
            else:
                return Response("Method Not Allowed", status="405 Method Not Allowed")
        elif request.path.startswith("/static/"):
            return self.app.send_static_file(request.path[len("/static/") :])
        return Response("Not Found", status="404 Not Found")
