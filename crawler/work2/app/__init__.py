from flask import Flask, jsonify, render_template
from . import crawler

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/book/<int:b_id>/info")
def get_book_info(b_id):
    """
    获取书籍信息接口
    """
    try:
        print(f"获取书籍信息：{b_id}")
        b_info = crawler.get_b_info(b_id)
        if b_info:
            return jsonify(b_info)
        else:
            return jsonify({}), 404
    except Exception as e:
        print(f"获取书籍信息错误：{e}")
        return jsonify({"error": "获取书籍信息错误"}), 500


@app.route("/book/<int:b_id>/chapter/<int:start>/<int:end>")
def get_book_chapter(b_id, start, end):
    """
    获取章节信息接口
    """
    try:
        print(f"获取章节信息：{b_id} {start} {end}")
        b_chapters = crawler.get_b_chapter(b_id, start, end)
        if b_chapters:
            return jsonify(b_chapters)
        else:
            return jsonify({}), 404
    except Exception as e:
        print(f"获取章节信息错误：{e}")
        return jsonify({"error": "获取章节信息错误"}), 500
