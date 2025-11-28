from datetime import timedelta

from sqlmodel import Session, select

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin


class AuthService:
    @staticmethod
    def register_user(db: Session, data: UserCreate):
        stmt = select(User).where(User.email == data.email)
        existing = db.exec(stmt).one_or_none()

        if existing:
            raise ValueError("El correo ya está registrado")

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
            raise ValueError("Invalid credentials")

        token = create_access_token(
            {"sub": str(user.id), "role": user.role}, expires_delta=timedelta(minutes=30)
        )
        return token
