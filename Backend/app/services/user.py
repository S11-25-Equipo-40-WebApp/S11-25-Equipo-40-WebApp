from uuid import UUID

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import func, select

from app.core.db import SessionDep
from app.models.user import User
from app.schemas.pagination import PaginationResponse
from app.schemas.user import UserResponse


class UserService:
    @staticmethod
    def get_users(db: SessionDep, skip: int, limit: int) -> PaginationResponse[UserResponse]:
        total_items = db.exec(select(func.count()).select_from(User)).one()

        users = db.exec(select(User).offset(skip).limit(limit)).all()

        user_responses = [UserResponse.model_validate(u) for u in users]

        total_pages = (total_items + limit - 1) // limit

        return PaginationResponse(
            total_items=total_items,
            results=user_responses,
            page=skip // limit + 1,
            size=limit,
            total_pages=total_pages,
            has_next=(skip + limit) < total_items,
            has_prev=skip > 0,
        )

    @staticmethod
    def get_user_by_id(db: SessionDep, id: UUID) -> User:
        user = db.get(User, id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def soft_delete_user(db: SessionDep, id: UUID):
        user = db.get(User, id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.is_active = False
        db.add(user)
        db.commit()
        return

    @staticmethod
    def update_user(db: SessionDep, user_id: UUID, data):
        user = db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        update_data = data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_email(db: SessionDep, email: EmailStr):
        stmt = select(User).where(User.email == email)
        result = db.exec(stmt)
        user = result.first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
