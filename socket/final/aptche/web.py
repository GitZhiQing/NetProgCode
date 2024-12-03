import asyncio
import logging

from aptche.wsgi.server import AptcheServer


class AptcheWeb:
    def __init__(self, app):
        self.app = app
        self.server = AptcheServer(app)

    def run(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.server.start())
        except KeyboardInterrupt:
            logging.info("服务已停止")
        finally:
            loop.close()
