from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel

from app.models.user import Roles


class UserCreate(SQLModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator("password")
    def validate_password(cls, v: str):
        if not any(c.islower() for c in v):
            raise ValueError("La contraseña debe incluir al menos una letra minúscula.")

        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")

        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe incluir al menos un número.")

        special = "!@#$%^&*()_+-=[]{};':\"\\|,.<>/?"
        if not any(c in special for c in v):
            raise ValueError(f"La contraseña debe incluir al menos un carácter especial: {special}")

        return v


class UserLogin(UserCreate):
    pass


class UserUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    surname: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = Field(default=None)
    role: Roles | None = None


class UserResponse(UserUpdate):
    id: UUID
    created_at: datetime
    updated_at: datetime
