from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field, Relationship

from .abstract import AbstractActive

if TYPE_CHECKING:
    from .api_key import APIKey
    from .testimonial import Testimonial


class Roles(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MODERATOR = "moderator"


class User(AbstractActive, table=True):
    email: EmailStr = Field(index=True, nullable=False, unique=True)
    name: str | None = None
    surname: str | None = None
    hashed_password: str
    role: Roles = Field(
        default=Roles.OWNER,
        sa_type=SQLEnum(Roles, native_enum=True, values_callable=lambda x: [e.value for e in x]),
    )

    # Multitenancy
    owner_id: UUID | None = Field(default=None, foreign_key="user.id")

    # relationships
    testimonials: list["Testimonial"] = Relationship(back_populates="author")
    api_keys: list["APIKey"] = Relationship(back_populates="user")
