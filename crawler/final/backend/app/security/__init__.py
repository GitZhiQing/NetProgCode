import time

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import schemas, settings
from app.database import crud

ALGORITHM = "HS256"  # 签名算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    生成密码哈希
    """
    return pwd_context.hash(password)


def authenticate_user(
    db: Session, username: str, password: str
) -> schemas.users.UserInDB | bool:
    """
    通过用户名和密码验证用户
    """
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("sub")
        username: str = payload.get("username")
        if uid is None or username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"uid": uid, "username": username}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: int | None = None):
    """
    生成访问令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = int(time.time()) + expires_delta
    else:
        expire = int(time.time()) + settings.ACCESS_TOKEN_EXPIRE_SECONDS * 60
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
