from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from app.core.deps import require_admin
from app.models.user import User
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"], dependencies=[Depends(require_admin)])


@router.get("/")
async def get(db: Session = Depends(get_session)):
    try:
        user = UserService.get_user(db)
        return user
    except HTTPException as e:
        raise e from None


@router.get("/{id}")
async def get_by_id(id: UUID, db: Session = Depends(get_session)):
    try:
        user = UserService.get_user_by_id(db, id)
        return user
    except HTTPException as e:
        raise e from None


@router.delete("/delete/{id}")
async def delete(id: UUID, db: Session = Depends(get_session)):
    try:
        user = UserService.delete_user(db, id)
        return user
    except HTTPException as e:
        raise e from None


@router.put("/update")
async def update(
    data: User,
    session: Session = Depends(get_session),
):
    try:
        user = UserService.update_user(session, data)
        return user
    except HTTPException as e:
        raise e from None
