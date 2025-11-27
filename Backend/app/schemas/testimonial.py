from datetime import datetime
from urllib.parse import urlparse
from uuid import UUID

from pydantic import HttpUrl, field_validator
from sqlmodel import Field, SQLModel


class TestimonialProduct(SQLModel):
    id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=100)


class TestimonialContent(SQLModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    content: str | None = Field(default=None, min_length=2, max_length=1000)
    rating: int | None = Field(default=None, ge=0, le=5)
    author_name: str | None = Field(default=None, max_length=100)


class TestimonialMedia(SQLModel):
    youtube_url: HttpUrl | None = None
    image_urls: list[HttpUrl] | None = None

    @field_validator("youtube_url")
    def validate_youtube(cls, v):
        if v is None:
            return v
        domain = urlparse(v).netloc
        if not ("youtube.com" in domain or "youtu.be" in domain):
            raise ValueError("La URL debe ser de YouTube")
        return v


class TestimonialCreate(SQLModel):
    product: TestimonialProduct
    content: TestimonialContent | None = None
    media: TestimonialMedia | None = None


class TestimonialResponse(TestimonialCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime


class TestimonialUpdate(SQLModel):
    content: TestimonialContent | None = None
    media: TestimonialMedia | None = None
