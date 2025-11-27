from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from app.schemas.auth import UserCreate, UserLogin, UserResponse, UserUpdate
from app.services.AuthService import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate, db: Session = Depends(get_session)):
    try:
        user = await AuthService.register_user(db, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/login")
async def login(data: UserLogin, db: Session = Depends(get_session)):
    try:
        token = await AuthService.login_user(db, data)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from None


@router.get("/me")
async def get_user(data: UserLogin, db: Session = Depends(get_session)):
    try:
        user = await AuthService.get_user(db, data.email)
        return user
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from None


@router.put("/me")
async def update_user(data: UserUpdate, db: Session = Depends(get_session)):
    try:
        user = await AuthService.update_user(db, data.email, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from None
