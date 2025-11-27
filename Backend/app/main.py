from fastapi import FastAPI

from app.api.router.auth import router as auth_router
from app.api.router.testimonials import router as testimonials_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.0.1",
)
app.include_router(auth_router)
app.include_router(testimonials_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Testify Backend!"}
