import asyncio
import json
import os

from aptche import Aptche, Response

app = Aptche()

TODO_FILE = os.path.join(os.path.dirname(__file__), "data", "data.json")

if not os.path.exists(TODO_FILE):
    os.makedirs(os.path.dirname(TODO_FILE), exist_ok=True)
    with open(TODO_FILE, "w") as f:
        json.dump([], f)


def load_todos():
    with open(TODO_FILE, "r") as f:
        return json.load(f)


def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f)


@app.route("/", methods=["GET"])
def index(request):
    todos = load_todos()
    return app.render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add(request):
    todos = load_todos()
    new_todo = {
        "id": len(todos) + 1,
        "title": request.data.get("title", [""])[0],
        "completed": False,
    }
    todos.append(new_todo)
    save_todos(todos)
    return Response("Added", status="302 Found", headers=[("Location", "/")])


@app.route("/delete", methods=["POST"])
def delete(request):
    todos = load_todos()
    todo_id = int(request.data.get("id", [0])[0])
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)
    return Response("Deleted", status="302 Found", headers=[("Location", "/")])


@app.route("/toggle", methods=["POST"])
def toggle(request):
    todos = load_todos()
    todo_id = int(request.data.get("id", [0])[0])
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            break
    save_todos(todos)
    return Response("Toggled", status="302 Found", headers=[("Location", "/")])


async def main():
    from aptche.wsgi import AptcheServer

    server = AptcheServer(app)
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("服务器被用户终止")
