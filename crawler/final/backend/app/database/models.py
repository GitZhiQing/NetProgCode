import time

from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class ODoc(Base):
    """
    原始文档表
    """

    __tablename__ = "odoc"

    odid = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True, index=True)
    site = Column(String, nullable=False)
    title = Column(String, nullable=False)
    first_100_words = Column(String, nullable=False)
    crawl_time = Column(String, default=str(int(time.time())))
    is_preprocessed = Column(Integer, default=0)


class PDoc(Base):
    """
    预处理后的文档表
    """

    __tablename__ = "pdoc"

    pdid = Column(Integer, primary_key=True, autoincrement=True)
    odid = Column(Integer, ForeignKey("odoc.odid", ondelete="CASCADE"), nullable=False)
    preprocess_time = Column(String, default=str(int(time.time())))
