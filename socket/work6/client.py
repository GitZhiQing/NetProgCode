import socket
import json
import threading
import logging
import time

# 预定义4个服务窗口端口
PORTS = [9999, 10000, 10001, 10002]

# 每个窗口的人数
WINDOW_QUEUES = [20, 20, 30, 30]


def send_request(port, data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", port))
            s.send(json.dumps(data).encode("utf-8"))
            response = s.recv(1024).decode("utf-8")
            logging.info(f"操作成功: {response}")
    except Exception as e:
        logging.error(f"发送请求时出错: {e}")


def buy_ticket(user, port):
    request = {"action": "buy", "user": user}
    time.sleep(0.1)
    send_request(port, request)


def query_ticket(ticket_uuid, port):
    request = {"action": "query", "uuid": ticket_uuid}
    send_request(port, request)


def worker(port, users):
    for user in users:
        buy_ticket(user, port)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s"
    )

    # 生成100个用户
    users = [f"user{i+1}" for i in range(100)]

    # 分配用户到各个窗口
    user_queues = []
    start = 0
    for count in WINDOW_QUEUES:
        user_queues.append(users[start : start + count])
        start += count

    # 启动4个线程，每个线程处理一个窗口的用户
    threads = []
    for i in range(4):
        t = threading.Thread(
            target=worker, args=(PORTS[i], user_queues[i]), name=f"窗口{i+1}"
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
