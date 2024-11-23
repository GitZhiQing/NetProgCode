from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    uid: int
    register_time: str

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str
