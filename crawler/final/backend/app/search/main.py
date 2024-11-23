import os

import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app import schemas, settings
from app.database import models
from app.search import preprocess

# Check if the .joblib files exist before loading
tfidf_matrix_path = settings.TFIDF_MATRIX_PATH
vectorizer_path = settings.VECTORIZER_PATH

if os.path.exists(tfidf_matrix_path) and os.path.exists(vectorizer_path):
    tfidf_matrix = joblib.load(tfidf_matrix_path)
    vectorizer = joblib.load(vectorizer_path)
else:
    raise FileNotFoundError("TF-IDF matrix and vectorizer files not found. Please preprocess the data first.")


def search(query: str, db: Session) -> dict:
    """
    Search relevant documents based on the query
    """
    # Retrieve documents from the database
    odocs = db.query(models.ODoc).all()
    documents = [
        schemas.odocs.ODoc.from_orm(odoc).dict()
        for odoc in odocs
    ]

    # Preprocess the query and convert to TF-IDF vector
    query_vec = vectorizer.transform([preprocess.tokenize_text(query)])
    # Calculate cosine similarity between query vector and document vectors
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    # Sort document indices by similarity
    ranked_indices = similarities.argsort()[::-1]
    # Return documents with similarity greater than 0
    results = [
        schemas.search_results.SearchResult(**documents[i], similarity=similarities[i])
        for i in ranked_indices if similarities[i] > 0
    ]
    search_results = schemas.search_results.SearchResults(results=results)
    return search_results.dict() if search_results.results else {"results": []}
