import socket

from aptche.wsgi import settings


def get_host():
    """
    获取 socket 的主机地址
    """
    hostname = socket.gethostname()
    addr_infos = socket.getaddrinfo(hostname, None)
    return addr_infos[-1][4][0]


def print_banner(host):
    if host == "0.0.0.0":
        loopback_host = "127.0.0.1"
        real_host = get_host()
        banner = f"{'=' * 16}* {settings.get("APP_NAME", "HTTP_SERVER")} *{'=' * 16}"
        if settings.get("HTTPS", "False"):
            print(banner)
            print(f"请访问 https://{loopback_host}:{settings.get("HTTPS_PORT")}/")
            print(f"请访问 https://{real_host}:{settings.get("HTTPS_PORT")}/")
            print("=" * len(banner))
        else:
            print(banner)
            print(f"请访问 http://{loopback_host}:{settings.get("HTTP_PORT")}/")
            print(f"请访问 http://{real_host}:{settings.get("HTTP_PORT")}/")
            print("=" * len(banner))
