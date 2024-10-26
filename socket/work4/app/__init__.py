import os
import logging


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] - %(message)s")


class Config:
    HOST = "127.0.0.1"
    PORT = 9999
    WEB_ROOT = os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "html"
    )
    SERVER_NAME = "Seeker dev"
    DEFAULT_INDEX = "index.html"


def run():
    from app import server

    server.start()
