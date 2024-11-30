from .http_client import HttpClient
from urllib.parse import urlparse
import socks


def get(url, params=None, headers=None, proxies=None):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 80
    path = parsed_url.path
    if parsed_url.query:
        path += "?" + parsed_url.query

    proxy = None
    if proxies:
        proxy_url = proxies.get(parsed_url.scheme)
        if proxy_url:
            proxy_parsed = urlparse(proxy_url)
            if proxy_parsed.scheme == "http":
                proxy = (socks.HTTP, proxy_parsed.hostname, proxy_parsed.port)
            elif proxy_parsed.scheme == "https":
                proxy = (socks.SOCKS5, proxy_parsed.hostname, proxy_parsed.port)

    client = HttpClient(host, port, proxy=proxy)
    response = client.get(path, params=params, headers=headers)
    client.close()
    return response


def post(url, data=None, json=None, files=None, headers=None, proxies=None):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 80
    path = parsed_url.path
    if parsed_url.query:
        path += "?" + parsed_url.query

    proxy = None
    if proxies:
        proxy_url = proxies.get(parsed_url.scheme)
        if proxy_url:
            proxy_parsed = urlparse(proxy_url)
            if proxy_parsed.scheme == "http":
                proxy = (socks.HTTP, proxy_parsed.hostname, proxy_parsed.port)
            elif proxy_parsed.scheme == "https":
                proxy = (socks.SOCKS5, proxy_parsed.hostname, proxy_parsed.port)

    client = HttpClient(host, port, proxy=proxy)
    response = client.post(path, data=data, json=json, files=files, headers=headers)
    client.close()
    return response
