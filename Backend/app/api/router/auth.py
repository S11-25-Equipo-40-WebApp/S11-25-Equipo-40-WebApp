from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.db import get_session
from app.core.deps import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.services.authService import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate, db: Session = Depends(get_session)):
    try:
        user = AuthService.register_user(db, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.post("/login")
async def login(data: UserLogin, db: Session = Depends(get_session)):
    try:
        token = AuthService.login_user(db, data)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from None


@router.put("/update")
async def update(
    data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        user = AuthService.update_user(session, data, current_user)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.get("/", dependencies=[Depends(require_admin)])
async def get(db: Session = Depends(get_session)):
    try:
        user = AuthService.get_user(db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{id}", dependencies=[Depends(require_admin)])
async def get_by_id(id: UUID, db: Session = Depends(get_session)):
    try:
        user = AuthService.get_user_by_id(db, id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None
