import asyncio
import ssl
from io import BytesIO

from aptche.wsgi import logging, settings, utils
from aptche.wsgi.environ import get_environ


class AptcheServer:
    def __init__(self, app):
        self.app = app
        self.host = settings.get("SERVER_NAME", "127.0.0.1")
        self.http_port = settings.get("HTTP_PORT", 8080)
        self.https_port = settings.get("HTTPS_PORT", 8443)
        self.certfile = settings.get("CERT_PATH")
        self.keyfile = settings.get("KEY_PATH")
        self.servers = []

    async def handle_client(self, reader, writer):
        try:
            request = b""
            while True:
                chunk = await reader.read(1024)
                if not chunk:
                    break
                request += chunk
                if b"\r\n\r\n" in request:
                    break
                if len(request) > 10 * 1024 * 1024:  # 限制请求大小为10MB
                    raise ValueError("请求体过大")
            environ = get_environ(request)
            response = self.get_response(environ)
            writer.write(response)
            await writer.drain()
        except Exception as e:
            logging.error(f"处理请求失败: {e}")
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                logging.error(f"客户端连接关闭失败: {e}")

    def get_response(self, environ):
        headers_set = []
        headers_sent = []

        def write(data):
            if not headers_sent:
                # 发送响应头
                status, response_headers = headers_set
                response = f"{environ.get('SERVER_PROTOCOL', 'HTTP/1.1')} {status}\r\n"
                for header in response_headers:
                    response += f"{header[0]}: {header[1]}\r\n"
                response += "\r\n"
                writer.write(response.encode("latin1"))
                headers_sent[:] = [status, response_headers]
            writer.write(data)

        def start_response(status, response_headers):
            headers_set[:] = [status, response_headers]
            return write

        result = self.app(environ, start_response)
        response_body = b"".join(result)
        writer = BytesIO()
        write(response_body)
        return writer.getvalue()

    async def run(self):
        try:
            if settings.get("HTTPS", "False"):
                if not self.certfile or not self.keyfile:
                    raise ValueError("SSL 证书文件和密钥文件必须提供")
                ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                ssl_context.load_cert_chain(
                    certfile=self.certfile, keyfile=self.keyfile
                )
                https_server = await asyncio.start_server(
                    self.handle_client, self.host, self.https_port, ssl=ssl_context
                )
                self.servers.append(https_server)
            else:
                http_server = await asyncio.start_server(
                    self.handle_client, self.host, self.http_port
                )
                self.servers.append(http_server)

            utils.print_banner(self.host)
            await asyncio.gather(*(server.serve_forever() for server in self.servers))
        except Exception as e:
            logging.error(f"服务器启动失败: {e}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        for server in self.servers:
            server.close()
            await server.wait_closed()
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        await asyncio.gather(*tasks, return_exceptions=True)
