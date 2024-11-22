import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import settings

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_STR}/openapi.json",
)

from app import init_app  # noqa

init_app.init_db()
init_app.init_dir()

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

from app.search import preprocess  # noqa

preprocess.tokenize_all_odocs()

tfidf_matrix, vectorizer = preprocess.build_inverted_index()

# 存储 tfidf_matrix 和 vectorizer
joblib.dump(tfidf_matrix, f"{settings.DATA_DIR}/pkls/tfidf_matrix.pkl")
joblib.dump(vectorizer, f"{settings.DATA_DIR}/pkls/vectorizer.pkl")
