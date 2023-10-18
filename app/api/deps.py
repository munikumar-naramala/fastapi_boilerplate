import secrets
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from app.config import settings
from app.db.session import SessionLocal

security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.USER_NAME)
    correct_password = secrets.compare_digest(credentials.password, settings.PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
