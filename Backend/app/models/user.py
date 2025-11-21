import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    email: str = Field(nullable=False, unique=True, max_length=255)
    name: str | None = Field(default=None, max_length=255)
    surname: str | None = Field(default=None, max_length=255)

    is_active: bool = Field(default=True)

    # JSONB CORRECTO
    roles: dict | None = Field(default=None, sa_column=Column(JSONB))

    hashed_password: str = Field(nullable=False, max_length=255)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
