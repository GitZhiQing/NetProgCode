from pydantic import BaseModel


class SearchResultBase(BaseModel):
    url: str
    title: str


class SearchResult(SearchResultBase):
    odid: int
    similarity: float
    first_100_words: str

    class Config:
        from_attributes = True


class SearchResults(BaseModel):
    results: list[SearchResult]
