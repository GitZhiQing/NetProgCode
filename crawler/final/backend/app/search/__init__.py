import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app import schemas, settings
from app.database import models, SessionLocal
from app.search import preprocess

# 加载 TF-IDF 矩阵和向量化器
tfidf_matrix = joblib.load(f"{settings.PKLS_DIR}/tfidf_matrix.pkl")
vectorizer = joblib.load(f"{settings.PKLS_DIR}/vectorizer.pkl")


def search(q: str, docs: list) -> schemas.search_results.SearchResults:
    """
    搜索
    """
    # 预处理查询文本
    query_vec = vectorizer.transform([preprocess.tokenize_text(q)])
    # 计算查询文本与所有文档的余弦相似度
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    # 根据相似度排序
    ranked_indices = similarities.argsort()[::-1]
    # 构建搜索结果，只返回相似度大于 0 的结果
    results = [
        schemas.search_results.SearchResult(**docs[i], similarity=similarities[i])
        for i in ranked_indices
        if similarities[i] > 0
    ]
    return schemas.search_results.SearchResults(results=results)


def main(query: str) -> dict:
    db: Session = SessionLocal()
    try:
        odocs = db.query(models.ODoc).all()
        documents = [
            schemas.odocs.ODoc.from_orm(odoc).dict()
            for odoc in odocs
        ]
    finally:
        db.close()

    search_results = search(query, documents)
    if search_results.results:
        return search_results.dict()
    else:
        return {"results": []}
