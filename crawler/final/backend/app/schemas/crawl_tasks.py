from pydantic import BaseModel
from pydantic.networks import HttpUrl


class CrawlTaskBase(BaseModel):
    target: HttpUrl
