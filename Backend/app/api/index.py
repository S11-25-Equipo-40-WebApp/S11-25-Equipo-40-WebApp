from fastapi import APIRouter

from app.api.router.api_key import router as api_key_router
from app.api.router.auth import router as auth_router
from app.api.router.testimonial import router as testimonial_router
from app.api.router.user import router as user_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(api_key_router)
router.include_router(testimonial_router)
