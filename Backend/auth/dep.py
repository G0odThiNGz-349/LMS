from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.models import User
from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) :
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) :
    return pwd_context.verify(plain, hashed)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def _make_token(data: dict, expires_delta: timedelta):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id: int):
    return _make_token(
        {"sub": str(user_id), "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

def create_refresh_token(user_id: int):
    return _make_token(
        {"sub": str(user_id), "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )


def _decode(token: str, expected_type: str):
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            raise credentials_exc
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exc
        return int(user_id)
    except InvalidTokenError:
        raise credentials_exc


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user_id = _decode(token, "access")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive account")
    return current_user


def get_refresh_user( token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user_id = _decode(token, "refresh")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user