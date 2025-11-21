from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.api.router.auth import router as auth_router
from app.core.config import settings
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.0.1",
    lifespan=lifespan,
)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Testify Backend!"}
