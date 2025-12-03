from uuid import uuid4 as UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.user import UserUpdate


class UserService:
    @staticmethod
    def get_user(db=Session):
        stmt = select(User)
        result = db.exec(stmt)
        user = result.all()
        return user

    @staticmethod
    def get_user_by_id(db=Session, id=UUID):
        stmt = select(User).where(User.id == id)
        result = db.exec(stmt)
        user = result.one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def delete_user(db=Session, id=UUID):
        stmt = select(User).where(User.id == id)
        result = db.exec(stmt)
        user = result.one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db.delete(user)
        db.commit()
        return user

    @staticmethod
    def update_user(db=Session, data=UserUpdate):
        stmt = select(User).where(User.email == data.email)
        result = db.exec(stmt)
        user = result.one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
