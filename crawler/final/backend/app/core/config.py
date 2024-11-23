import logging
import os
import sys
from functools import lru_cache

from pydantic_settings import BaseSettings


def get_database_url():
    win = sys.platform.startswith("win")
    prefix = "sqlite:///" if win else "sqlite:////"
    return prefix + os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "data.db"
    )


class Settings(BaseSettings):
    APP_ENV: str = "dev"
    APP_NAME: str = "Search Engine API"
    API_STR: str = "/api"
    SECRET_KEY: str = "seek2geek"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 天

    DATABASE_URL: str = get_database_url()
    STATIC_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static"
    )
    DATA_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"
    )
    JOBLIB_DIR: str = os.path.join(DATA_DIR, "joblibs")
    TFIDF_MATRIX_PATH: str = os.path.join(JOBLIB_DIR, "tfidf_matrix.joblib")
    VECTORIZER_PATH: str = os.path.join(JOBLIB_DIR, "vectorizer.joblib")
    ODOC_DIR: str = os.path.join(DATA_DIR, "odocs")
    PDOC_DIR: str = os.path.join(DATA_DIR, "pdocs")

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
