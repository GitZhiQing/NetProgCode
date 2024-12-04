import json

from . import DATA_PATH


def generate_tickets():
    tickets = []
    for i in range(1, 101):
        tickets.append({"id": str(i), "status": "0", "name": "", "uuid": ""})
    with open(DATA_PATH, "w") as f:
        json.dump(tickets, f, indent=4)
