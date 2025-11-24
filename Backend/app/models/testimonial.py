from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.user import User


class Testimonial(SQLModel, table=True):
    __tablename__ = "testimonials"

    id: UUID = Field(default=None, primary_key=True)

    title: str = Field(nullable=False, max_length=200)
    content: str = Field(nullable=False)

    media_type: str = Field(nullable=False, max_length=10)
    media_url: str | None = Field(default=None, max_length=500)

    status: str = Field(nullable=False, max_length=10)

    views_count: int = Field(default=0)

    author_id: UUID = Field(foreign_key="users.id")
    category_id: UUID | None = Field(default=None, foreign_key="categories.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: datetime | None = None

    author: Optional["User"] = Relationship(back_populates="testimonials")
