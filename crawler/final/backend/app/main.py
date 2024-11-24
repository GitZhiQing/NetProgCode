import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import settings

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_STR}/openapi.json",
)

from app import init_app  # noqa

logging.info("应用初始化中...")
init_app.init_dir()
init_app.init_db()
init_app.init_search_index()
logging.info("应用初始化完成.")

# CORS
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

from app.api import api_router  # noqa

app.include_router(api_router, prefix=settings.API_STR)
