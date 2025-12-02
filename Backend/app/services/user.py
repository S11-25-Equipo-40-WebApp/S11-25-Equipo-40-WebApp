from fastapi import HTTPException, status
from sqlmodel import select

from app.models.user import User


class UserService:
    @staticmethod
    def get_user(db):
        stmt = select(User)
        result = db.exec(stmt)
        user = result.all()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def get_user_by_id(db, id):
        stmt = select(User).where(User.id == id)
        result = db.exec(stmt)
        user = result.one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def delete_user(db, id):
        stmt = select(User).where(User.id == id)
        result = db.exec(stmt)
        user = result.one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db.delete(user)
        db.commit()
        return user

    @staticmethod
    def update_user(db, data):
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
