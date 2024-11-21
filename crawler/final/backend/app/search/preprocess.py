import re
import jieba
import os
import nltk
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


def load_stopwords(file_path):
    """
    加载停用词表
    """
    with open(file_path, "r", encoding="utf-8") as file:
        stopwords = set(file.read().splitlines())
    return stopwords


def tokenize_html(text):
    """
    html 文本分词
    """

    # 去除 HTML tag
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text().lower()
    # 去除非中文和非英文字符
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z\s]", "", text)

    # 正则分离中文和英文
    chinese_text = re.findall(r"[\u4e00-\u9fa5]+", text)
    english_text = re.findall(r"[a-zA-Z]+", text)

    # 中文分词
    chinese_words = []
    for sentence in chinese_text:
        chinese_words.extend(jieba.lcut(sentence))

    # 英文分词
    english_words = []
    for sentence in english_text:
        english_words.extend(word_tokenize(sentence))

    words = chinese_words + english_words

    # 去除停用词
    stopwords = load_stopwords("stopwords.txt")
    words = [word for word in words if word not in stopwords]

    return " ".join(words)
