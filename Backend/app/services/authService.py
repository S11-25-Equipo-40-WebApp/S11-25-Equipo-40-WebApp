from sqlmodel import Session, select

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


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
