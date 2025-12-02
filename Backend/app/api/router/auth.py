from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate, db: Session = Depends(get_session)):
    user = AuthService.register_user(db, data)
    return user


@router.post("/login")
async def login(data: UserLogin, db: Session = Depends(get_session)):
    token = AuthService.login_user(db, data)
    return {"access_token": token, "token_type": "bearer"}


@router.patch("/update")
async def update(
    data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    user = AuthService.update_user(session, data, current_user)
    return user


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
