from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from app.schemas.auth import UserLogin, UserRegister, UserResponse
from app.services.AuthService import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(data: UserRegister, db: Session = Depends(get_session)):
    try:
        user = await AuthService.register_user(db, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/login")
async def login(data: UserLogin, db: Session = Depends(get_session)):
    try:
        token = await AuthService.login_user(db, data.email, data.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from None
