from pydantic import BaseModel


class ODocBase(BaseModel):
    url: str
    title: str
    site: str
    first_100_words: str


class ODocCreate(ODocBase):
    pass


class ODoc(ODocBase):
    odid: int
    crawl_time: str
    is_preprocessed: int

    class Config:
        from_attributes = True
