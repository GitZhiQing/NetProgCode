import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("ssl").setLevel(logging.CRITICAL)

CERTS_DIR_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "certs")

settings = {
    "APP_NAME": "Aptche HTTP Server",
    "SERVER_NAME": "0.0.0.0",
    "HTTP_PORT": 8080,
    "HTTPS_PORT": 8443,
    "SERVER_VERSION": "2024.12",
    "DEFAULT_ENCODING": "utf-8",
    "HTTPS": True,
    "CERT_PATH": os.path.join(CERTS_DIR_PATH, "www.aptche.com+4.pem"),
    "KEY_PATH": os.path.join(CERTS_DIR_PATH, "www.aptche.com+4-key.pem"),
}

from aptche.wsgi.server import AptcheServer  # noqa

__all__ = ["AptcheServer", settings]
