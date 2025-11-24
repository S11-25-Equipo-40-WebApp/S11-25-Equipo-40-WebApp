from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.0.1",
)


@app.get("/")
async def root():
    return {"message": "Welcome to Testify Backend!"}
