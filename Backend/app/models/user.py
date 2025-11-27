from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship

from .abstract import AbstractActive

if TYPE_CHECKING:
    from .testimonial import Testimonial


class Roles(StrEnum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class User(AbstractActive, table=True):
    email: EmailStr = Field(index=True, nullable=False, unique=True)
    name: str | None = None
    surname: str | None = None
    hashed_password: str
    role: Roles = Field(default=Roles.USER)

    # relationships
    testimonials: list["Testimonial"] = Relationship(back_populates="author")
