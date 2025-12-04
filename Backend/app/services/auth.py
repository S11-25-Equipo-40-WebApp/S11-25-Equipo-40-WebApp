from datetime import timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.config import settings
from app.core.jwt import create_access_token, create_refresh_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def register_user(db: Session, data: UserCreate):
        stmt = select(User).where(User.email == data.email)
        existing = db.exec(stmt).one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login_user(db: Session, data: OAuth2PasswordRequestForm):
        stmt = select(User).where(User.email == data.username)
        result = db.exec(stmt)
        user = result.one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        access_token = create_access_token(
            {"sub": str(user.id), "role": user.role},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = create_refresh_token(
            {"sub": str(user.id), "role": user.role},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    def create_new_access_token(user: User):
        access_token = create_access_token(
            {"sub": str(user.id), "role": user.role},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = create_refresh_token(
            {"sub": str(user.id), "role": user.role},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
