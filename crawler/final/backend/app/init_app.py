import logging
import os

import joblib
from sqlalchemy.orm import Session

from app import settings, deps
from app.database import crud, SessionLocal
from app.search import preprocess


def init_db():
    logging.info("初始化数据库...")
    if os.path.exists(settings.DATABASE_URL):
        os.remove(settings.DATABASE_URL)
    from app.database import engine, models

    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        odoc1 = crud.create_odoc(
            db,
            url="https://www.secrss.com/articles/72613",
            title="《密码法》颁布五周年：法治成效、实施难点与未来走向",
            first_100_words="《密码法》颁布五周年，密码法是我国网络安全领域的基础性法律，",
        )
        odoc2 = crud.create_odoc(
            db,
            url="https://www.secrss.com/articles/72602",
            title="美军研发并推出网络威胁监控和检测工具CANDOR和PJ",
            first_100_words="美国国防部研究局（DARPA）的信息创新办公室（I2O）",
        )
        odoc3 = crud.create_odoc(
            db,
            url="https://www.secrss.com/articles/72600",
            title="《互联网广告可识别性执法指南》解读",
            first_100_words="《互联网广告可识别性执法指南》是由国家市场监督管理总",
        )
        logging.info(f"ODoc 1 创建完成: {odoc1.title}")
        logging.info(f"ODoc 2 创建完成: {odoc2.title}")
        logging.info(f"ODoc 3 创建完成: {odoc3.title}")
    finally:
        db.close()
    logging.info("数据库初始化完成.")


def init_dir():
    logging.info("初始化目录...")
    if not os.path.exists(settings.STATIC_DIR):
        os.makedirs(settings.STATIC_DIR, exist_ok=True)

    if not os.path.exists(settings.DATA_DIR):
        os.makedirs(settings.DATA_DIR, exist_ok=True)

    if not os.path.exists(settings.ODOC_DIR):
        os.makedirs(settings.ODOC_DIR, exist_ok=True)

    if not os.path.exists(settings.PDOC_DIR):
        os.makedirs(settings.PDOC_DIR, exist_ok=True)

    if not os.path.exists(settings.JOBLIB_DIR):
        os.makedirs(settings.JOBLIB_DIR, exist_ok=True)
    logging.info("目录初始化完成.")


def init_search_index():
    logging.info("初始化搜索索引...")
    db: Session = next(deps.get_db())
    unprocessed_odocs = crud.get_unprocessed_odocs(db)
    if unprocessed_odocs:
        logging.info("预处理未处理的文档...")
        preprocess.tokenize_all_odocs()
        tfidf_matrix, vectorizer = preprocess.build_inverted_index()
        # 将 tfidf_matrix 和 vectorizer 保存为 .joblib 文件
        joblib.dump(tfidf_matrix, settings.TFIDF_MATRIX_PATH)
        joblib.dump(vectorizer, settings.VECTORIZER_PATH)
        logging.info("预处理完成.")
    logging.info("搜索索引初始化完成.")
