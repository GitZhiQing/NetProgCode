from fastapi import APIRouter

from app.api.routes import docs, tasks

router = APIRouter()

router.include_router(docs.router, prefix="/docs", tags=["docs"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
