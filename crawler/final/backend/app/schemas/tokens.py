from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: int
    username: str


class TokenData(BaseModel):
    uid: int
    username: str
    exp: int
