from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,  # 增加连接池大小
    max_overflow=20,  # 增加最大溢出连接数
    pool_timeout=30,  # 设置连接超时时间
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
