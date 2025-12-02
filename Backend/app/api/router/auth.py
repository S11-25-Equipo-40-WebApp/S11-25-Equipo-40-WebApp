from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate, db: Session = Depends(get_session)):
    try:
        user = AuthService.register_user(db, data)
        return user
    except HTTPException as e:
        raise e from None


@router.post("/login")
async def login(data: UserLogin, db: Session = Depends(get_session)):
    try:
        token = AuthService.login_user(db, data)
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        raise e from None


@router.patch("/update")
async def update(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        user = AuthService.update_user(session, current_user)
        return user
    except HTTPException as e:
        raise e from None


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
