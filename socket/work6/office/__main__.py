from . import utils
from office.server import TicketServer
import threading


def start_server(host, port):
    server = TicketServer(host, port)
    server.run()


if __name__ == "__main__":
    utils.generate_tickets()
    threads = []
    try:
        for i in range(4):
            t = threading.Thread(
                target=start_server, args=("localhost", 9999 + i), name=f"窗口{i+1}"
            )
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        for t in threads:
            t.join()
        print("服务已停止")
