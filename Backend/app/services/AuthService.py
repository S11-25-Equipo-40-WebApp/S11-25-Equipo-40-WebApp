from fastapi import HTTPException
from sqlalchemy import select

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin


class AuthService:
    @staticmethod
    async def register_user(db, data: UserCreate):
        stmt = select(User).where(User.email == data.email)
        result = db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            raise ValueError("El correo ya está registrado")
        hashed = hash_password(data.password)
        user = User(
            email=data.email,
            hashed_password=hashed,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    async def login_user(db, data: UserLogin):
        stmt = select(User).where(User.email == data.email)
        result = db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = create_access_token({"sub": str(user.id), "roles": user.role})
        return token

    @staticmethod
    async def get_user(db, email: str):
        result = db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError("User not found")
        return user

    @staticmethod
    async def update_user(db, email: str, data):
        stmt = select(User).where(User.email == email)
        result = db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
