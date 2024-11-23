import json
import logging
import os
import re

import jieba
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session

from app import settings, utils, deps
from app.database import crud

# 预编译正则表达式模式
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fa5]+")
ENGLISH_PATTERN = re.compile(r"[a-zA-Z]+")
NON_CHINESE_ENGLISH_PATTERN = re.compile(r"[^\u4e00-\u9fa5a-zA-Z\s]")

# 加载停用词
STOPWORDS_PATH = os.path.join(settings.DATA_DIR, "stopwords.txt")
STOPWORDS = set()
if os.path.exists(STOPWORDS_PATH):
    with open(STOPWORDS_PATH, "r", encoding="utf-8") as file:
        STOPWORDS = set(file.read().splitlines())


def tokenize_text(text):
    """
    分词文本
    """
    # 移除HTML标签
    text = BeautifulSoup(text, "html.parser").get_text().lower()
    # 移除非中文和非英文字符
    text = NON_CHINESE_ENGLISH_PATTERN.sub("", text)

    # 分离中文和英文文本
    chinese_words = [
        word
        for sentence in CHINESE_PATTERN.findall(text)
        for word in jieba.lcut(sentence)
    ]
    english_words = [
        word
        for sentence in ENGLISH_PATTERN.findall(text)
        for word in word_tokenize(sentence)
    ]

    # 移除停用词
    words = [word for word in chinese_words + english_words if word not in STOPWORDS]

    return " ".join(words)


def preprocess_all_odocs():
    """
    预处理所有未处理的原始文档
    """
    logging.info("Start preprocessing all unprocessed ODocs")
    db: Session = next(deps.get_db())
    odocs = crud.get_unprocessed_odocs(db)
    for odoc in odocs:
        pdoc = crud.create_pdoc(db, odoc.odid)
        pdoc_content = tokenize_text(utils.read_odoc_content(odoc))
        with open(
                f"{settings.PDOC_DIR}/{pdoc.pdid}.txt", "w", encoding="utf-8"
        ) as f:
            f.write(pdoc_content)
        odoc.is_preprocessed = 1
    db.commit()
    logging.info(f"{len(odocs)} ODocs preprocessed")
    logging.info("Finish preprocessing all unprocessed ODocs")
    return len(odocs)


def build_inverted_index(documents):
    """
    构建倒排索引
    """
    inverted_index = {}
    for doc_id, content in enumerate(documents):
        words = content.split()
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = set()
            inverted_index[word].add(doc_id)
    return inverted_index


def build_tfidf_matrix():
    """
    构建 TF-IDF 矩阵，返回 TF-IDF 矩阵、TfidfVectorizer 对象和倒排索引
    """
    db: Session = next(deps.get_db())
    documents = [utils.read_pdoc_content(pdoc) for pdoc in crud.get_all_pdocs(db)]

    # 构建 TF-IDF 矩阵
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 构建倒排索引
    inverted_index = build_inverted_index(documents)

    # 保存倒排索引
    with open(settings.INVERTED_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {k: list(v) for k, v in inverted_index.items()}, f, ensure_ascii=False
        )

    return tfidf_matrix, vectorizer
