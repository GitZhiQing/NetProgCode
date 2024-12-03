import asyncio
import logging

from flask import Flask

from aptche.wsgi.server import AptcheServer

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


async def main():
    server = AptcheServer(app)
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("服务器被用户终止")
