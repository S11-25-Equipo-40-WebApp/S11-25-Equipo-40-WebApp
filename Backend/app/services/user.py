from uuid import UUID

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import select

from app.core.db import SessionDep
from app.models.user import User
from app.schemas.pagination import PaginationResponse
from app.schemas.user import UserResponse


class UserService:
    @staticmethod
    def get_users(db: SessionDep, skip: int, limit: int) -> PaginationResponse[UserResponse]:
        stmt = select(User).offset(skip).limit(limit)
        result = db.exec(stmt)
        user = result.all()

        user_responses = [UserResponse.model_validate(u) for u in user]

        return PaginationResponse(
            total_items=len(user_responses),
            results=user_responses,
            page=skip // limit + 1,
            size=limit,
            total_pages=(len(user_responses) + limit - 1) // limit,
            has_next=(skip + limit) < len(user_responses),
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

        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="User soft deleted successfully"
        )

    @staticmethod
    def update_user(db: SessionDep, user_id: UUID, data):
        user = db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

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

    # @staticmethod
    # def update_user_role(
    #     user_id: UUID,
    #     new_role: AdminUserUpdate,
    #     db: SessionDep,
    # ) -> User:
    #     user = db.get(User, user_id)

    #     if not user:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    #     user.role = new_role.new_role
    #     db.add(user)
    #     db.commit()
    #     db.refresh(user)
    #     return user
