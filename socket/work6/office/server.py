import selectors
import socket
import threading
import json
import uuid

from . import DATA_PATH


class TicketServer:
    def __init__(self, host, port):
        self.selector = selectors.DefaultSelector()
        self.host = host
        self.port = port
        self.lock = threading.Lock()
        self.load_tickets()

    def load_tickets(self):
        with open(DATA_PATH, "r") as f:
            self.tickets = json.load(f)

    def save_tickets(self):
        with open(DATA_PATH, "w") as f:
            json.dump(self.tickets, f, indent=4)

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        print(f"建立连接: {addr}")
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        data = conn.recv(1024)
        if data:
            request = json.loads(data.decode("utf-8"))
            response = self.handle_request(request)
            conn.send(json.dumps(response).encode("utf-8"))
        else:
            self.selector.unregister(conn)
            conn.close()

    def handle_request(self, request):
        action = request.get("action", "")
        if action == "buy":
            user = request.get("user")
            return self.buy_ticket(user)
        elif action == "query":
            stiff = request.get("uuid")
            return self.query_ticket(stiff)
        return {"status": "error", "message": "Invalid action"}

    def buy_ticket(self, user):
        with self.lock:
            for ticket in self.tickets:
                if ticket["status"] == "0":
                    ticket["status"] = "1"
                    ticket["name"] = user
                    ticket_uuid = str(uuid.uuid4())
                    ticket["uuid"] = ticket_uuid
                    self.save_tickets()
                    print(
                        f"售出: 窗口号: {threading.current_thread().name}, 票号: {ticket['id']}, 余票数量: {self.get_remaining_tickets()}"
                    )
                    return {
                        "status": "success",
                        "ticket_id": ticket["id"],
                        "uuid": ticket_uuid,
                    }
        return {"status": "error", "message": "没有余票"}

    def query_ticket(self, ticket_uuid):
        for ticket in self.tickets:
            if ticket["uuid"] == ticket_uuid:
                return {"status": "success", "ticket": ticket}
        return {"status": "error", "message": "未找到票"}

    def get_remaining_tickets(self):
        return sum(1 for ticket in self.tickets if ticket["status"] == "0")

    def run(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((self.host, self.port))
        server_sock.listen()
        server_sock.setblocking(False)
        self.selector.register(server_sock, selectors.EVENT_READ, self.accept)
        print(f"售票服务运行在 {self.host}:{self.port}")

        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
