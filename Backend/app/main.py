from fastapi import FastAPI

from app.api.index import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.0.1",
)

app.include_router(api_router, prefix=settings.API)


@app.get("/")
async def root():
    return {"message": "Welcome to Testify Backend!"}
