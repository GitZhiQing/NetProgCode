from sqlalchemy.orm import Session

from app.database import models


def create_odoc(db: Session, url: str, title: str, first_100_words: str) -> models.ODoc:
    odoc = models.ODoc(url=url, title=title, first_100_words=first_100_words)
    db.add(odoc)
    db.commit()
    db.refresh(odoc)
    return odoc


def create_pdoc(db: Session, odid: int) -> models.PDoc:
    pdoc = models.PDoc(odid=odid)
    db.add(pdoc)
    db.commit()
    db.refresh(pdoc)
    return pdoc


def get_all_odocs(db: Session):
    return db.query(models.ODoc).all()


def get_unprocessed_odocs(db: Session):
    """
    获取未预处理的文档
    """
    return db.query(models.ODoc).filter(models.ODoc.is_preprocessed == 0).all()  # type: ignore


def get_all_pdocs(db: Session):
    return db.query(models.PDoc).all()
