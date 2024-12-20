import os
import shutil

from app import settings
from app.database import models


def read_odoc_content(odoc: models.ODoc) -> str:
    """
    读取 ODoc 的内容
    """
    with open(f"{settings.ODOC_DIR}/{odoc.odid}.html", "r", encoding="utf-8") as f:
        return f.read()


def read_pdoc_content(pdoc: models.PDoc) -> str:
    """
    读取 PDoc 的内容
    """
    with open(f"{settings.PDOC_DIR}/{pdoc.pdid}.txt", "r", encoding="utf-8") as f:
        return f.read()


def recreate_dir(dir_path: str):
    """
    删除并重新创建文件夹
    """
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)
