from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.params import Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlmodel import Session

from app.core.config import settings
from app.core.db import SessionDep, get_session
from app.models.api_key import APIKey
from app.models.user import Roles, User
from app.services.api_keys import APIKeyService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.API + "/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token sin usuario."
            ) from None

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="El token ha expirado."
        ) from None
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido."
        ) from None

    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado."
        ) from None

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo.")

    return user


async def get_refresh_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token sin usuario."
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="El token ha expirado."
        ) from None

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido."
        ) from None

    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo.")

    return user


def require_owner(current_user: User = Depends(get_current_user)):
    if current_user.role != Roles.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Solo los propietarios tienen permisos."
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in [Roles.OWNER, Roles.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los propietarios y administradores tienen permisos.",
        )
    return current_user


def require_moderator(current_user: User = Depends(get_current_user)):
    if current_user.role not in [Roles.OWNER, Roles.ADMIN, Roles.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos.")
    return current_user


def get_api_key_public(
    db: SessionDep,
    x_api_key: str = Header(..., alias="X-API-Key"),  # type: ignore
) -> APIKey:
    """
    Validate API key for public endpoints.
    Does NOT require an authenticated user.
    """
    api_key = APIKeyService.verify_api_key(db, x_api_key)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key.",
        )
    return api_key


OwnerDep = Annotated[User, Depends(require_owner)]
AdminDep = Annotated[User, Depends(require_admin)]
ModeratorDep = Annotated[User, Depends(require_moderator)]
APIKeyPublicDep = Annotated[APIKey, Depends(get_api_key_public)]
