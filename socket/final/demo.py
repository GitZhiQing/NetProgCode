from aptche.server import AptcheServer
from aptche.web import Aptche, render_template

app = Aptche()


@app.route("/<name>")
def index(name):
    if name:
        return render_template("index.html", name=name, app="Aptche")


@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"


server = AptcheServer(app)
server.run(host="0.0.0.0", port=8888)
