from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import crud
from app.deps import get_db
from app.search import main

router = APIRouter()


@router.get("/", response_model=schemas.search_results.SearchResults)
async def search(query: str, db: Session = Depends(get_db)):
    """
    搜索
    """
    return main.search(query, db)


@router.get("/odocs/count")
async def get_odocs_count(db: Session = Depends(get_db)):
    """
    获取原始文档数量
    """
    count = len(crud.get_all_odocs(db))
    return {"count": count}


@router.get("/pdocs/count")
def get_pdocs_count(db: Session = Depends(get_db)):
    """
    获取预处理文档数量
    """
    count = len(crud.get_all_pdocs(db))
    return {"count": count}
