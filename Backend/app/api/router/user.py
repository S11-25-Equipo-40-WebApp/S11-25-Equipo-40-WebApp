from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.core.deps import require_admin
from app.models.user import User
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"], dependencies=[Depends(require_admin)])


@router.get("/")
def get(db: Session = Depends(get_session)):
    return UserService.get_user(db)


@router.get("/{id}")
def get_by_id(id: UUID, db: Session = Depends(get_session)):
    return UserService.get_user_by_id(db, id)


@router.delete("/delete/{id}")
def delete(id: UUID, db: Session = Depends(get_session)):
    return UserService.delete_user(db, id)


@router.put("/update")
def update(
    data: User,
    session: Session = Depends(get_session),
):
    return UserService.update_user(session, data)
