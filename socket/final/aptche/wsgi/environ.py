from io import BytesIO

from aptche.wsgi import settings, logging


def get_environ(request):
    environ = {
        "REQUEST_METHOD": "",
        "SCRIPT_NAME": "",
        "PATH_INFO": "",
        "QUERY_STRING": "",
        "CONTENT_TYPE": "",
        "CONTENT_LENGTH": "",
        "SERVER_NAME": settings.get("SERVER_NAME", "Aptche HTTP Server"),
        "SERVER_PORT": settings.get("HTTP_PORT", "80"),
        "HTTPS_PORT": settings.get("HTTPS_PORT", "443"),
        "SERVER_PROTOCOL": "HTTP/1.1",
        "REMOTE_ADDR": "",
        "REMOTE_PORT": "",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "https" if settings.get("HTTPS") else "http",
        "wsgi.input": BytesIO(request),
        "wsgi.errors": BytesIO(),
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
    }

    try:
        header, body = request.split(b"\r\n\r\n", 1)
        header = header.decode("latin1")
        request_line, headers_alone = header.split("\r\n", 1)
        method, path, _ = request_line.split()
        environ["REQUEST_METHOD"] = method
        environ["PATH_INFO"] = path.split("?")[0]
        environ["QUERY_STRING"] = path.split("?")[1] if "?" in path else ""
        environ["wsgi.input"] = BytesIO(body)

        headers = headers_alone.split("\r\n")
        for header in headers:
            if ":" in header:
                key, value = header.split(":", 1)
                key = key.strip().upper().replace("-", "_")
                value = value.strip()
                if key == "CONTENT_TYPE":
                    environ["CONTENT_TYPE"] = value
                elif key == "CONTENT_LENGTH":
                    environ["CONTENT_LENGTH"] = value
                elif key == "HOST":
                    environ["SERVER_NAME"], environ["SERVER_PORT"] = value.split(":")
                else:
                    environ[f"HTTP_{key}"] = value
            else:
                logging.error(f"无效的头格式: {header}")
    except ValueError as e:
        logging.error(f"请求格式错误: {e}")

    return environ
