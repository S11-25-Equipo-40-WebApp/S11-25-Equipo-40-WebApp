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

    @model_validator(mode="after")
    def validate_media(cls, values):
        if values.media_type == MediaType.TEXT:
            # Si es texto, NO debe tener media_url
            values.media_url = None
        else:
            # Si NO es texto, debe existir una URL válida
            if not values.media_url:
                raise ValueError("media_url es obligatorio.")
        return values


class TestimonialAuthor(SQLModel):
    name: str
    surname: str


class TestimonialResponse(TestimonialCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    views_count: int
    author: TestimonialAuthor


class TestimonialUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=5, max_length=200)
    content: str | None = Field(default=None, min_length=10, max_length=1000)
    media_type: MediaType | None = None
    media_url: str | None = None
