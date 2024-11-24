import json

import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app import schemas, settings
from app.database import models
from app.search import preprocess


def load_data():
    """
    加载 inverted_index, tfidf_matrix, vectorizer 并同时返回
    """
    with open(settings.INVERTED_INDEX_PATH, "rb") as file:
        inverted_index = json.load(file)
    tfidf_matrix = joblib.load(settings.TFIDF_MATRIX_PATH)
    vectorizer = joblib.load(settings.VECTORIZER_PATH)
    return inverted_index, tfidf_matrix, vectorizer


def search(query: str, db: Session) -> dict:
    """
    根据查询词搜索相关文件
    """
    inverted_index, tfidf_matrix, vectorizer = load_data()

    # 预处理查询词并转换为 TF-IDF 向量
    query_tokens = preprocess.tokenize_text(query).split()
    query_vec = vectorizer.transform([preprocess.tokenize_text(query)])

    # 使用倒排索引初步筛选文档
    candidate_docs = set()
    for token in query_tokens:
        if token in inverted_index:
            candidate_docs.update(inverted_index[token])

    if not candidate_docs:
        return {"results": []}

    # 计算查询向量与候选文档向量之间的余弦相似度
    candidate_docs = list(candidate_docs)
    candidate_tfidf_matrix = tfidf_matrix[candidate_docs]
    similarities = cosine_similarity(query_vec, candidate_tfidf_matrix).flatten()

    # 按相似度对文档索引进行排序
    ranked_indices = similarities.argsort()[::-1]

    # 从数据库检索文件
    odocs = db.query(models.ODoc).all()
    documents = [schemas.odocs.ODoc.from_orm(odoc).dict() for odoc in odocs]

    # 返回相似度大于 0 的文档
    results = [
        schemas.search_results.SearchResult(
            **documents[candidate_docs[i]], similarity=similarities[i]
        )
        for i in ranked_indices
        if similarities[i] > 0
    ]
    search_results = schemas.search_results.SearchResults(results=results)
    return search_results.dict() if search_results.results else {"results": []}
