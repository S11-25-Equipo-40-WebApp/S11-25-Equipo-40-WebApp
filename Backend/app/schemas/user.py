from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.models.user import Roles


class UserCreate(SQLModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])[A-Za-z\d!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]{8,}$",
    )


class UserLogin(UserCreate):
    pass


class UserUpdate(SQLModel):
    name: str | None = Field(min_length=2, max_length=50)
    surname: str | None = Field(min_length=2, max_length=50)
    email: EmailStr | None = None
    role: Roles | None = None


class UserResponse(UserUpdate):
    id: str
    created_at: datetime
    updated_at: datetime
