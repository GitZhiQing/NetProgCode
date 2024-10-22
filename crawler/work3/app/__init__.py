from flask import Flask, render_template, request
from app import crawler, search
import concurrent.futures

app = Flask(__name__)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)


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
        # 提交任务到线程池
        executor.submit(crawler.main, target)
        return render_template("crawler.html", target=target)
    return render_template("crawler.html")
