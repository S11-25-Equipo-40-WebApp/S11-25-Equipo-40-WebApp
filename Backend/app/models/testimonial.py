from enum import StrEnum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
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
    product_id: str
    product_name: str
    title: str | None = None
    content: str | None = None
    youtube_url: str | None = None
    image_url: list[str] | None = Field(default_factory=list, sa_column=Column(JSON))
    status: StatusType = Field(default=StatusType.PENDING)
    rating: int | None = None
    author_name: str | None = None

    # Foreign Keys
    user_id: UUID | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL")
    category_id: UUID | None = Field(default=None, foreign_key="category.id", ondelete="SET NULL")

    # Relationships
    author: "User" = Relationship(back_populates="testimonials")
    category: Optional["Category"] = Relationship(back_populates="testimonials")
    tags: list["Tag"] = Relationship(back_populates="testimonials", link_model=TestimonialTagLink)
