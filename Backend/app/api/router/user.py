from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import EmailStr

from app.core.db import SessionDep
from app.core.deps import AdminDep, ModeratorDep
from app.models.user import Roles
from app.schemas import (
    AdminUserUpdate,
    PaginationResponse,
    UserCreateInternal,
    UserResponse,
)
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def create_user_for_owner(
    data: UserCreateInternal,
    db: SessionDep,
    current_user: AdminDep,
):
    """Create a new user under the owner or admin

    Args:
    - data (UserCreateInternal): data for creating the new user
    - db (SessionDep): database session
    - current_user (AdminDep): current user making the request

    Returns:
    - UserResponse: the newly created user
    """
    user = UserService.create_user_for_owner(db, current_user, data)
    return UserResponse.model_validate(user)


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
    return UserService.get_users(db, current_user, skip, limit)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user_info(current_user: ModeratorDep):
    return current_user


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_current_user_info(
    data: AdminUserUpdate,
    db: SessionDep,
    current_user: ModeratorDep,
):
    if current_user.role == Roles.MODERATOR:
        if data.role in (Roles.OWNER, Roles.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Moderators cannot change their own roles to owner or admin",
            )

    if current_user.role == Roles.ADMIN:
        if data.role == Roles.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins cannot assign themselves owner role",
            )

    return UserService.update_user(
        db=db,
        user_id=current_user.id,
        data=data,
        current_user=current_user,
    )


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def get_user_by_id(
    user_id: UUID,
    db: SessionDep,
    current_user: ModeratorDep,
):
    return UserService.get_user_by_id(db, user_id, current_user)


@router.patch("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_user(
    user_id: UUID,
    db: SessionDep,
    current_user: AdminDep,
):
    # Obtener el usuario a eliminar para validar permisos
    user = UserService.get_user_by_id(db, user_id, current_user)

    # Admin NO puede borrar owners
    if current_user.role == Roles.ADMIN and user.role == Roles.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins cannot delete owners",
        )

    return UserService.soft_delete_user(db, user_id, current_user)


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(
    user_id: UUID,
    data: AdminUserUpdate,
    db: SessionDep,
    current_user: ModeratorDep,
):
    """Update user information

    - Owners and Admins can update: name, surname, email, role
    - Moderators can only update: name, surname, email (no role)
    """
    # Si el campo role está presente y no es None, validar permisos
    if data.role is not None:
        # Moderadores no pueden cambiar roles
        if current_user.role == Roles.MODERATOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Moderators cannot change user roles",
            )

        # Admins no pueden asignar owner
        if current_user.role == Roles.ADMIN and data.role == Roles.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins cannot assign owner role",
            )

    return UserService.update_user(
        db=db,
        user_id=user_id,
        data=data,
        current_user=current_user,
    )


@router.get("/email/{email}", response_model=UserResponse)
def get_by_email(
    email: EmailStr,
    db: SessionDep,
    current_user: ModeratorDep,
):
    return UserService.get_user_by_email(db, email, current_user)
