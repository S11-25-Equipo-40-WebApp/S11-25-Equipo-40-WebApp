from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TestimonialCreate(BaseModel):
    title: str
    content: str
    media_type: str
    media_url: str | None = None
    status: str
    category_id: UUID | None = None


class TestimonialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    media_type: str | None = None
    media_url: str | None = None
    status: str | None = None
    category_id: UUID | None = None


class TestimonialResponse(BaseModel):
    id: UUID
    title: str
    content: str
    media_type: str
    media_url: str | None = None
    status: str
    views_count: int
    author_id: UUID
    category_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True
