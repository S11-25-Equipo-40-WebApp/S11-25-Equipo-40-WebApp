from datetime import timedelta

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.core.jwt import create_access_token, create_refresh_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserUpdate

PROHIBITED_FIELDS = ["role", "id"]


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
    def login_user(db: Session, data: UserLogin):
        stmt = select(User).where(User.email == data.email)
        result = db.exec(stmt)
        user = result.one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        access_token = create_access_token(
            {"sub": str(user.id), "role": user.role}, expires_delta=timedelta(minutes=30)
        )
        refresh_token = create_refresh_token(
            {"sub": str(user.id), "role": user.role}, expires_delta=timedelta(days=30)
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    def update_user(db: Session, current_user: User, data: UserUpdate):
        stmt = select(User).where(User.email == current_user.email)
        result = db.exec(stmt)
        user = result.one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        payload = data.model_dump(exclude_unset=True)
        for field in PROHIBITED_FIELDS:
            if field in payload:
                raise HTTPException(
                    status_code=403, detail=f"No puedes modificar el campo '{field}'."
                )
        for key, value in payload.items():
            setattr(user, key, value)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_new_access_token(user: User):
        access_token = create_access_token(
            {"sub": str(user.id), "role": user.role}, expires_delta=timedelta(minutes=30)
        )
        refresh_token = create_refresh_token(
            {"sub": str(user.id), "role": user.role}, expires_delta=timedelta(days=30)
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
