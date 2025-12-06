from uuid import UUID

from fastapi import APIRouter, Query, status
from pydantic import EmailStr

from app.core.db import SessionDep
from app.core.deps import AdminDep, ModeratorDep, UserDep
from app.schemas import AdminUserUpdate, PaginationResponse, UserResponse, UserUpdate
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PaginationResponse[UserResponse],
)
def get_users(
    db: SessionDep,
    current_user: ModeratorDep,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to retrieve"),
):
    return UserService.get_users(db, skip, limit)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user_info(current_user: UserDep):
    return current_user


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_current_user_info(
    data: UserUpdate,
    db: SessionDep,
    current_user: UserDep,
):
    return UserService.update_user(
        db=db,
        user_id=current_user.id,
        data=data,
    )


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def get_user_by_id(user_id: UUID, db: SessionDep, current_user: ModeratorDep):
    return UserService.get_user_by_id(db, user_id)


@router.patch("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_user(user_id: UUID, db: SessionDep, current_user: AdminDep):
    return UserService.soft_delete_user(db, user_id)


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def admin_user_update(
    user_id: UUID,
    data: AdminUserUpdate,
    db: SessionDep,
    current_user: ModeratorDep,
):
    return UserService.update_user(
        db=db,
        user_id=user_id,
        data=data,
    )


@router.get("/email/{email}", response_model=UserResponse)
def get_by_email(
    email: EmailStr,
    db: SessionDep,
    current_user: ModeratorDep,
):
    return UserService.get_user_by_email(db, email)
