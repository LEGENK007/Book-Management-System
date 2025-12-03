from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from passlib.context import CryptContext
import jwt 
import os

from app.core.config import settings


# -------- Password Hashing - Argon2id with bcrypt as fallback -------- #

pwd_context = CryptContext(
    schemes = ["argon2", "bcrypt"],
    default = "argon2", 
    # Argon2 parameters
    argon2__time_cost = 2,            # Number of Iterations
    argon2__memory_cost = 102400,     # in KiB -> 100MiB
    argon2__parallelism = 4,
)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def needs_rehash(hashed_password: str) -> bool:
    return pwd_context.needs_update(hashed_password)


# Helper to create and decode JWT token
def create_access_token(subject: int, expire_minutes: Optional[int] = None, extra: Optional[Dict[str, Any]] = None) -> str:
    if expire_minutes is None:
        expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    payload = {
        "exp": expire,
        "sub": str(subject)
    }
    if extra:
        payload.update(extra)
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.pyJWTError as exc:
        raise ValueError("Token decode error") from exc