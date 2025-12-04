from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.db import get_session
from app.core.deps import get_refresh_user
from app.models.user import User
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(data: UserCreate, db: Session = Depends(get_session)):
    user = AuthService.register_user(db, data)
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_session),
):
    return AuthService.login_user(db, form_data)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(current_user: User = Depends(get_refresh_user)):
    return AuthService.create_new_access_token(current_user)
