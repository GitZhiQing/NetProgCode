import logging
import os
import sys
from functools import lru_cache

from pydantic_settings import BaseSettings


def get_database_url():
    win = sys.platform.startswith("win")

    if win:
        prefix = "sqlite:///"
    else:
        prefix = "sqlite:////"
    return prefix + os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data/data.db"
    )


class Settings(BaseSettings):
    APP_ENV: str = "dev"
    APP_NAME: str = "Search Engine API"
    API_STR: str = "/api"
    SECRET_KEY: str = "seek2geek"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 一周

    DATABASE_URL: str = get_database_url()
    STATIC_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static"
    )
    # 数据存储目录
    DATA_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"
    )
    # PKL 存储目录
    PKLS_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data/pkls"
    )
    # 原始文档存储目录
    ODOC_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data/odocs"
    )
    # 预处理文档存储目录
    PDOC_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data/pdocs"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
    logging.getLogger("passlib").setLevel(logging.ERROR)
    logging.getLogger("jieba").setLevel(logging.ERROR)
