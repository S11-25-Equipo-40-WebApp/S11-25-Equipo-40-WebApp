from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserRegister


class AuthService:
    @staticmethod
    async def register_user(db, data: UserRegister):
        stmt = select(User).where(User.email == data.email)
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        password = hash_password(data.password)

        if existing:
            raise ValueError("El correo ya está registrado")
        user = User(
            email=data.email, name=data.name, surname=data.surname, hashed_password=password
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def login_user(db: Session, email: str, password: str):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = create_access_token({"sub": str(user.id), "roles": user.roles})
        return token
