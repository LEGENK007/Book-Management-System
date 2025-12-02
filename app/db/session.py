from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings


# Creating Async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo = True,                       # Turn to OFF in Production
    future = True
)


# Creating Async session
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit = False,
    autoflush = False
    autocommit = False
)


# FastAPI Dependency
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session