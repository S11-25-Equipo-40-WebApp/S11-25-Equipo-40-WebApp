from datetime import datetime
from uuid import UUID

from pydantic import model_validator
from sqlmodel import Field, SQLModel

from app.models.testimonial import MediaType


class TestimonialCreate(SQLModel):
    title: str = Field(min_length=5, max_length=200)
    content: str = Field(min_length=10, max_length=1000)
    media_type: MediaType = Field(default=MediaType.TEXT)
    media_url: str | None = None
    tags: list[str] = []

    @model_validator(mode="after")
    def validate_media(cls, values):
        if values.media_type == MediaType.TEXT:
            values.media_url = None
        else:
            if not values.media_url:
                raise ValueError("media_url es obligatorio.")
        return values

    model_config = {"from_attributes": True}


class TestimonialAuthor(SQLModel):
    name: str
    surname: str

    model_config = {"from_attributes": True}


class TestimonialResponse(SQLModel):
    id: UUID
    title: str
    content: str
    media_type: MediaType
    media_url: str | None
    created_at: datetime
    updated_at: datetime
    views_count: int
    author: TestimonialAuthor

    # ⬅️ IMPORTANTE
    model_config = {"from_attributes": True}


class TestimonialUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=5, max_length=200)
    content: str | None = Field(default=None, min_length=10, max_length=1000)
    media_type: MediaType | None = None
    media_url: str | None = None

    model_config = {"from_attributes": True}
