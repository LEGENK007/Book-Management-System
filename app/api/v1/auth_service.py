from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.session import get_session
from app.db.crud.users import get_user_by_email, create_user
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    decode_access_token,
    needs_rehash,
)
from app.schemas.token import Token, TokenPayload
from app.schemas.user import UserCreate, UserOut


router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_session)) -> UserOut:
    # Check if user existing
    existing = await get_user_by_email(session, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    password_hash = get_password_hash(user_in.password)
    user = await create_user(session, user_in, password_hash)
    return user


@router.post("/auth/login", response_model=Token)
async def login(payload: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(session, payload.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    try:
        if needs_rehash(user.password_hash):
            new_hash = get_password_hash(payload.password)
            user.password_hash = new_hash
            session.add(user)
            await session.commit()
            await session.refresh(user)
    except Exception:
        pass 
    
    token = create_access_token(subject=user.id, extra={"role": user.role})
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    

    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    try:
        user_id = int(sub)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")
    
    user = await session.get(__import__("app.models.models", fromlist=["User"]).User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user
