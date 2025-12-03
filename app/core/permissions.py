from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.api.v1.auth_service import get_current_user
from app.db.session import get_session
from app.models.models import User

def _forbidden(detail: str = "Forbidden"):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


async def require_authenticated(current_user: User = Depends(get_current_user)) -> User:
    return current_user

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if getattr(current_user, "role", None) != "admin":
        _forbidden("Admin privileges required")
    return current_user

def require_role(role: str):
    async def _require(current_user: User = Depends(get_current_user)):
        if getattr(current_user, "role", None) != role:
            _forbidden(f"{role} privileges required")
        return current_user
    return _require


