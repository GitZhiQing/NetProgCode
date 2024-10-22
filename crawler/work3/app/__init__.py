from flask import Flask, render_template, request
from app import crawler, search
from rich.logging import RichHandler
import logging
from threading import Thread

app = Flask(__name__)

# 配置日志处理器
logging.basicConfig(level="INFO", handlers=[RichHandler()])
logger = logging.getLogger("flask.app")


@app.route("/")
def index():
    keyword = request.args.get("keyword", "")
    if keyword:
        return render_template(
            "index.html", keyword=keyword, urls=search.search(keyword)
        )
    return render_template("index.html")


@app.route("/crawler")
def crawler_index():
    target = request.args.get("target", "")
    if target:
        t = Thread(target=crawler.main, args=(target,))
        t.start()
        return render_template("crawler.html", target=target)
    return render_template("crawler.html")
