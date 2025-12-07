from uuid import UUID

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import func, or_, select

from app.core.db import SessionDep
from app.core.security import hash_password
from app.models.user import Roles, User
from app.schemas.pagination import PaginationResponse
from app.schemas.user import (
    AdminUserUpdate,
    UserCreateInternal,
    UserResponse,
)


class UserService:
    @staticmethod
    def _get_tenant_owner_id(user: User) -> UUID:
        """Get the tenant owner ID for a user.

        Args:
            user: User to get the tenant owner ID for

        Returns:
            UUID: The tenant owner ID (user's owner_id if set, otherwise user's id)
        """
        return user.owner_id if user.owner_id else user.id

    @staticmethod
    def create_user_for_owner(db: SessionDep, owner: User, data: UserCreateInternal) -> User:
        """Create a new user under the owner or admin

        Args:
            db (SessionDep): database session
            owner (User): current user creating the new user
            data (UserCreateInternal): data for creating the new user

        Raises:
            HTTPException: if the owner does not have permission to create users
            HTTPException: if the email already exists

        Returns:
            User: the newly created user
        """
        # Only owner or admin can create users under them
        if owner.role not in (Roles.OWNER, Roles.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="No permission to create users"
            )

        # Validate unique email
        existing = db.exec(select(User).where(User.email == data.email)).one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

        # El nuevo usuario debe pertenecer al tenant owner, no al creador
        tenant_owner_id = UserService._get_tenant_owner_id(owner)

        user = User(
            **data.model_dump(exclude={"password"}),
            hashed_password=hash_password(data.password),
            owner_id=tenant_owner_id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_users(
        db: SessionDep, current_user: User, skip: int, limit: int
    ) -> PaginationResponse[UserResponse]:
        """Retrieve a paginated list of users for the current user's owner

        Args:
            db (SessionDep): database session
            current_user (User): current user making the request
            skip (int): number of items to skip
            limit (int): number of items to retrieve

        Returns:
            PaginationResponse[UserResponse]: paginated list of users
        """
        # Determinar el ID del owner del tenant
        tenant_owner_id = UserService._get_tenant_owner_id(current_user)

        total_items = db.exec(
            select(func.count())
            .select_from(User)
            .where(
                or_(
                    User.owner_id == tenant_owner_id,  # usuarios del tenant
                    User.id == tenant_owner_id,  # incluir al owner
                )
            )
        ).one()

        users = db.exec(
            select(User)
            .where(
                or_(
                    User.owner_id == tenant_owner_id,  # usuarios del tenant
                    User.id == tenant_owner_id,  # incluir al owner
                )
            )
            .offset(skip)
            .limit(limit)
        ).all()

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
    def get_user_by_id(db: SessionDep, id: UUID, current_user: User) -> User:
        """Retrieve a user by ID for the current user's owner

        Args:
            db (SessionDep): database session
            id (UUID): user ID
            current_user (User): current user making the request

        Raises:
            HTTPException: if the user is not found or does not belong to the current user's owner

        Returns:
            User: the retrieved user
        """
        user = db.get(User, id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Validar que pertenece al mismo owner/tenant
        tenant_owner_id = UserService._get_tenant_owner_id(current_user)
        user_tenant_owner_id = UserService._get_tenant_owner_id(user)

        if user_tenant_owner_id != tenant_owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    @staticmethod
    def soft_delete_user(db: SessionDep, id: UUID, current_user: User):
        """Soft delete a user by setting is_active to False

        Args:
            db (SessionDep): database session
            id (UUID): user ID
            current_user (User): current user making the request

        Raises:
            HTTPException: if the current user does not have permission to delete users
            HTTPException: if the user is not found or does not belong to the current user's owner
        """
        user = db.get(User, id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Validar que pertenece al mismo owner/tenant
        tenant_owner_id = UserService._get_tenant_owner_id(current_user)
        user_tenant_owner_id = UserService._get_tenant_owner_id(user)

        if user_tenant_owner_id != tenant_owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.is_active = False
        db.add(user)
        db.commit()

    @staticmethod
    def update_user(
        db: SessionDep,
        user_id: UUID,
        data: AdminUserUpdate,
        current_user: User,
    ) -> User:
        """Update user information (name, surname, email, and role if allowed)

        Args:
            db (SessionDep): database session
            user_id (UUID): ID of user to update
            data: AdminUserUpdate data for updating the user
            current_user (User): current user making the request

        Raises:
            HTTPException: if user not found or permission denied

        Returns:
            User: updated user
        """
        user = db.get(User, user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Determinar el ID del owner del tenant
        tenant_owner_id = UserService._get_tenant_owner_id(current_user)
        user_tenant_owner_id = UserService._get_tenant_owner_id(user)

        # Validar que pertenezca al mismo tenant
        if user_tenant_owner_id != tenant_owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        update_data = data.model_dump(exclude_unset=True)

        # Aplicar actualizaciones
        for key, value in update_data.items():
            setattr(user, key, value)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_user_by_email(db: SessionDep, email: EmailStr, current_user: User):
        """Retrieve a user by email for the current user's owner

        Args:
            db (SessionDep): database session
            email (EmailStr): user email
            current_user (User): current user making the request

        Raises:
            HTTPException: if the user is not found or does not belong to the current user's owner

        Returns:
            User: the retrieved user
        """
        tenant_owner_id = UserService._get_tenant_owner_id(current_user)

        user = db.exec(
            select(User).where(
                User.email == email,
                or_(
                    User.owner_id == tenant_owner_id,
                    User.id == tenant_owner_id,
                ),
            )
        ).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
