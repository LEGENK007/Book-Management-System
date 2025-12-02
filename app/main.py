from fastapi import FastAPI 
from app.db.base import Base 
from app.db.session import engine
from app.api.v1.books_api import router as book_router
from app.api.v1.reviews_api import router as review_router

app = FastAPI(title="Intelligent Book Management System")

app.include_router(book_router, prefix="/api/v1")
app.include_router(review_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/", summary="Health Check")
async def root():
    return {"Message": "IBMS running"}