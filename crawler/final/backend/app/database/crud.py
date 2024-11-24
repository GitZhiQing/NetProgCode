from sqlalchemy.orm import Session

from app.database import models


def create_odoc(
    db: Session, url: str, title: str, site: str, first_100_words: str
) -> models.ODoc:
    """
    创建原始文档
    """
    odoc = models.ODoc(url=url, title=title, site=site, first_100_words=first_100_words)
    db.add(odoc)
    db.commit()
    db.refresh(odoc)
    return odoc


def create_pdoc(db: Session, odid: int) -> models.PDoc:
    """
    创建预处理文档
    """
    pdoc = models.PDoc(odid=odid)
    db.add(pdoc)
    db.commit()
    db.refresh(pdoc)
    return pdoc


def get_all_odocs(db: Session):
    """
    获取所有原始文档
    """
    return db.query(models.ODoc).all()


def get_odoc_by_odid(db: Session, odid: int):
    """
    根据 odid 获取原始文档
    """
    return db.query(models.ODoc).filter(models.ODoc.odid == odid).first()  # type: ignore


def get_odoc_by_url(db: Session, url: str):
    """
    根据 url 获取原始文档
    """
    return db.query(models.ODoc).filter(models.ODoc.url == url).first()  # type: ignore


def get_unprocessed_odocs(db: Session):
    """
    获取未预处理的原始文档
    """
    return db.query(models.ODoc).filter(models.ODoc.is_preprocessed == 0).all()  # type: ignore


def get_all_pdocs(db: Session):
    """
    获取所有预处理文档
    """
    return db.query(models.PDoc).all()
