import logging
import os

from sqlalchemy.orm import Session

from app import settings, deps, utils
from app.database import crud
from app.search import preprocess


def init_db():
    logging.info("初始化数据库...")
    if os.path.exists(settings.DATABASE_URL):
        os.remove(settings.DATABASE_URL)
    from app.database import engine, models

    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    logging.info("Done.")


def init_dir():
    logging.info("初始化目录...")
    utils.recreate_dir(settings.STATIC_DIR)
    utils.recreate_dir(settings.ODOC_DIR)
    utils.recreate_dir(settings.PDOC_DIR)
    utils.recreate_dir(settings.JOBLIB_DIR)
    if os.path.exists(settings.INVERTED_INDEX_PATH):
        os.remove(settings.INVERTED_INDEX_PATH)
    logging.info("Done.")


def init_search_index():
    logging.info("初始化搜索索引...")
    db: Session = next(deps.get_db())
    # 检查是否未爬取文档
    odocs = crud.get_all_odocs(db)
    if not odocs:
        logging.info("未找到任何原始文档...")
        default_crawl_target_id = 0
        default_crawl_count = 10
        from app import crawler

        crawler.crawl_range_count(default_crawl_count, default_crawl_target_id)
        logging.info("Done.")

    # 检查是否有未处理的文档
    unprocessed_odocs = crud.get_unprocessed_odocs(db)
    if unprocessed_odocs:
        logging.info("预处理原始文档...")
        preprocess.preprocess_all_odocs()
        logging.info("Done.")
    logging.info("Done.")
