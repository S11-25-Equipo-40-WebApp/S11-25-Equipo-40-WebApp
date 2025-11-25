from enum import StrEnum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from .abstract import AbstractActive
from .testimonial_tag_link import TestimonialTagLink

if TYPE_CHECKING:
    from .category import Category
    from .tag import Tag
    from .user import User


class MediaType(StrEnum):
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"


class StatusType(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Testimonial(AbstractActive, table=True):
    title: str
    content: str
    media_type: MediaType = Field(default=MediaType.TEXT)
    media_url: str | None = None
    status: StatusType = Field(default=StatusType.PENDING)
    views_count: int = Field(default=0)
    author_id: UUID = Field(foreign_key="user.id")
    category_id: UUID | None = Field(default=None, foreign_key="category.id")

    # Relationships
    author: "User" = Relationship(back_populates="testimonials")
    category: Optional["Category"] = Relationship(back_populates="testimonials")
    tags: list["Tag"] = Relationship(back_populates="testimonials", link_model=TestimonialTagLink)
