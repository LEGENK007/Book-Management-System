from fastapi import FastAPI 
from app.db.base import Base 
from app.db.session import engine

app = FastAPI(title="Intelligent Book Management System")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/", summary="Health Check")
async def root():
    return {"Message": "IBMS running"}