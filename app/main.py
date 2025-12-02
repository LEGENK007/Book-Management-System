from fastapi import FastAPI 


app = FastAPI(title="Intelligent Book Management System")


@app.get("/", summary="Health Check")
async def root():
    return {"Message": "IBMS running"}