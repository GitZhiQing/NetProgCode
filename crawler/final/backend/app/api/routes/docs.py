from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_db
from app.search import main

router = APIRouter()


@router.get("/", response_model=schemas.search_results.SearchResults)
async def search(query: str, db: Session = Depends(get_db)):
    """
    搜索
    """
    return main.search(query, db)
