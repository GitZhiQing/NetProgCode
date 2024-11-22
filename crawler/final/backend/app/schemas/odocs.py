from pydantic import BaseModel


class ODocBase(BaseModel):
    url: str
    title: str


class ODocCreate(ODocBase):
    first_100_words: str


class ODoc(ODocBase):
    odid: int
    crawl_time: str
    is_preprocessed: int
    first_100_words: str

    class Config:
        from_attributes = True
