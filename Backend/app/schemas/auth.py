from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str | None = None
    roles: list[str] | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str | None = None
    surname: str | None = None
    is_active: bool
    roles: Any | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
