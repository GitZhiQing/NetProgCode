import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("ssl").setLevel(logging.CRITICAL)

CERTS_DIR_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "certs"
)

settings = {
    "APP_NAME": "Aptche HTTP Server",
    "SERVER_NAME": "0.0.0.0",  # 服务器地址
    "HTTP_PORT": 8080,  # HTTP端口
    "HTTPS_PORT": 8443,  # HTTPS端口
    "SERVER_VERSION": "2024.12",  # 服务器版本
    "DEFAULT_ENCODING": "utf-8",  # 默认编码
    "HTTPS": True,  # 是否启用HTTPS
    "CERT_PATH": os.path.join(CERTS_DIR_PATH, "www.aptche.com+4.pem"),  # 证书路径
    "KEY_PATH": os.path.join(CERTS_DIR_PATH, "www.aptche.com+4-key.pem"),  # 私钥路径
}

from aptche.wsgi.server import AptcheServer  # noqa

__all__ = ["AptcheServer", settings]
