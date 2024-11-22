import logging
import os
import re

import jieba
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session

from app import settings, utils
from app.core.config import setup_logging
from app.database import crud, SessionLocal

setup_logging()
# 预编译正则表达式
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fa5]+")
ENGLISH_PATTERN = re.compile(r"[a-zA-Z]+")
NON_CHINESE_ENGLISH_PATTERN = re.compile(r"[^\u4e00-\u9fa5a-zA-Z\s]")

# 加载停用词表
STOPWORDS_PATH = os.path.join(
    settings.DATA_DIR,
    "stopwords.txt",
)
STOPWORDS = set()
if os.path.exists(STOPWORDS_PATH):
    with open(STOPWORDS_PATH, "r", encoding="utf-8") as file:
        STOPWORDS = set(file.read().splitlines())


def load_stopwords(file_path):
    """
    加载停用词表
    """
    with open(file_path, "r", encoding="utf-8") as f:
        stopwords = set(f.read().splitlines())
    return stopwords


def tokenize_text(text):
    """
    文本分词
    """
    # 去除 HTML tag
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text().lower()
    # 去除非中文和非英文字符
    text = NON_CHINESE_ENGLISH_PATTERN.sub("", text)

    # 正则分离中文和英文
    chinese_text = CHINESE_PATTERN.findall(text)
    english_text = ENGLISH_PATTERN.findall(text)

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
    words = [word for word in words if word not in STOPWORDS]

    return " ".join(words)


def tokenize_all_odocs():
    """
    查询并处理所有未处理的文档
    """
    logging.info("Start preprocessing all unprocessed ODocs")
    db: Session = SessionLocal()
    odocs = crud.get_unprocessed_odocs(db)
    try:
        for odoc in odocs:
            pdoc = crud.create_pdoc(db, odoc.odid)
            odoc_content = utils.read_odoc_content(odoc)
            pdoc_content = tokenize_text(odoc_content)
            with open(
                    f"{settings.PDOC_DIR}/{pdoc.pdid}.txt", "w", encoding="utf-8"
            ) as f:
                f.write(pdoc_content)
            odoc.is_preprocessed = 1
        db.commit()
        logging.info(f"{len(odocs)} ODocs preprocessed")
    finally:
        db.close()
    logging.info("Finish preprocessing all unprocessed ODocs")
    return len(odocs)


def build_inverted_index():
    """
    构建倒排索引，返回 TF-IDF 矩阵和 TfidfVectorizer 对象
    """
    db: Session = SessionLocal()
    documents = []

    try:
        pdocs = crud.get_all_pdocs(db)
        for pdoc in pdocs:
            content = utils.read_pdoc_content(pdoc)
            documents.append({"content": content})
    finally:
        db.close()

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([doc["content"] for doc in documents])
    feature_names = vectorizer.get_feature_names_out()
    inverted_index = {}

    for doc_id, doc in enumerate(documents):
        feature_index = tfidf_matrix[doc_id, :].nonzero()[1]
        tfidf_scores = zip(
            feature_index, [tfidf_matrix[doc_id, x] for x in feature_index]
        )
        for w, s in tfidf_scores:
            word = feature_names[w]
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append((doc_id, s))
    return tfidf_matrix, vectorizer
