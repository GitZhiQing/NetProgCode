from .http_client import HttpClient


def get(url, params=None, headers=None):
    parsed_url = url.split("/")
    host = parsed_url[2]
    path = "/" + "/".join(parsed_url[3:])
    client = HttpClient(host)
    response = client.get(path, params=params, headers=headers)
    client.close()
    return response


def post(url, data=None, json=None, files=None, headers=None):
    parsed_url = url.split("/")
    host = parsed_url[2]
    path = "/" + "/".join(parsed_url[3:])
    client = HttpClient(host)
    response = client.post(path, data=data, json=json, files=files, headers=headers)
    client.close()
    return response
