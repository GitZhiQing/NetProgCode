from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app import schemas, security, settings
from app.database import SessionLocal, crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/tokens")


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        uid: str = payload.get("sub")
        username: str = payload.get("username")
        exp: int = payload.get("exp")
        if uid is None or username is None:
            raise credentials_exception
        token_data = schemas.tokens.TokenData(uid=uid, username=username, exp=exp)
    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_by_uid(db, token_data.uid)
    if user is None:
        raise credentials_exception
    return user
