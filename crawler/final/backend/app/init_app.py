import logging
import os
import shutil

from sqlalchemy.orm import Session

from app import settings
from app.database import crud, SessionLocal


def init_db():
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
        logging.info(f"ODoc 1 created: {odoc1.title}")
        logging.info(f"ODoc 2 created: {odoc2.title}")
        logging.info(f"ODoc 3 created: {odoc3.title}")
    finally:
        db.close()


def init_dir():
    if os.path.exists(settings.STATIC_DIR):
        shutil.rmtree(settings.STATIC_DIR)
    os.makedirs(settings.STATIC_DIR, exist_ok=True)

    if not os.path.exists(settings.DATA_DIR):
        os.makedirs(settings.DATA_DIR, exist_ok=True)
