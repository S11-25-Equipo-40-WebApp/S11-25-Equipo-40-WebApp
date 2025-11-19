from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User


class AuthService:
    @staticmethod
    def register_user(db: Session, data):
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise ValueError("Email already registered")

        new_user = User(
            email=data.email,
            name=data.name,
            surname=data.surname,
            hashed_password=hash_password(data.password),
            roles=["user"],
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def login_user(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = create_access_token({"sub": str(user.id), "roles": user.roles})
        return token
