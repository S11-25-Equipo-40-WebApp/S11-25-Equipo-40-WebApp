from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.core.deps import require_admin
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"], dependencies=[Depends(require_admin)])


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_session)):
    return UserService.get_user_list(db)


@router.get("/{id}", response_model=UserResponse)
def get_by_id(id: UUID, db: Session = Depends(get_session)):
    return UserService.get_user_by_id(db, id)


@router.delete("/delete/{id}")
def delete(id: UUID, db: Session = Depends(get_session)):
    return UserService.delete_user(db, id)


@router.put("/{id}", response_model=UserUpdate)
def update(
    id: UUID,
    data: User,
    session: Session = Depends(get_session),
):
    return UserService.update_user(session, id, data)


@router.get("/email/{email}", response_model=UserResponse)
def get_by_email(email: str, db: Session = Depends(get_session)):
    return UserService.get_user_by_email(db, email)
