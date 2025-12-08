from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import EmailStr

from app.core.db import SessionDep
from app.core.deps import AdminDep, ModeratorDep
from app.models.user import Roles
from app.schemas import AdminUserUpdate, PaginationResponse, UserCreateInternal, UserResponse
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
    - current_user (AdminDep): current user making the request (guaranteed to be owner or admin by AdminDep)

    Returns:
    - UserResponse: the newly created user
    """
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    user = UserService.create_user_for_owner(db, tenant_owner_id, data)
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
    role: Roles | None = Query(None, description="Filter by user role"),
    search: str | None = Query(None, description="Search by first name or last name"),
):
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    users, total_items = UserService.get_users(db, tenant_owner_id, skip, limit, role, search)

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

    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    return UserService.update_user(
        db=db,
        user_id=current_user.id,
        data=data,
        tenant_owner_id=tenant_owner_id,
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
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    return UserService.get_user_by_id(db, user_id, tenant_owner_id)


@router.patch("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_user(
    user_id: UUID,
    db: SessionDep,
    current_user: AdminDep,
):
    # No permitir auto-eliminación
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete your own account",
        )

    tenant_owner_id = UserService._get_tenant_owner_id(current_user)

    # Obtener el usuario a eliminar para validar permisos
    user = UserService.get_user_by_id(db, user_id, tenant_owner_id)

    # Admin NO puede borrar owners
    if current_user.role == Roles.ADMIN and user.role == Roles.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins cannot delete owners",
        )

    return UserService.soft_delete_user(db, user_id, tenant_owner_id)


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
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)

    # Obtener el usuario a editar para validar permisos
    user_to_update = UserService.get_user_by_id(db, user_id, tenant_owner_id)

    # Admin NO puede editar owners
    if current_user.role == Roles.ADMIN and user_to_update.role == Roles.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins cannot edit owners",
        )

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
        tenant_owner_id=tenant_owner_id,
        user=user_to_update,  # Pasar el usuario ya obtenido para evitar query duplicada
    )


@router.get("/email/{email}", response_model=UserResponse)
def get_by_email(
    email: EmailStr,
    db: SessionDep,
    current_user: ModeratorDep,
):
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    return UserService.get_user_by_email(db, email, tenant_owner_id)
