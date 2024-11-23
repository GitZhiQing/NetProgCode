from fastapi import APIRouter

from app.api.routes import docs

router = APIRouter()

router.include_router(docs.router, prefix="/docs", tags=["docs"])
