from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.models.models import User
from app.schemas.user import UserCreate

# Get user by email
async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    result = await session.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


# Create user
async def create_user(session: AsyncSession, user_in: UserCreate, password_hash: str) -> User:
    new_user = User(
        email = user_in.email,
        password_hash = password_hash,
        role = user_in.role,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user