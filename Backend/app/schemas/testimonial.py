from datetime import datetime
from urllib.parse import urlparse
from uuid import UUID

from pydantic import HttpUrl, field_validator, model_serializer
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
    image_url: list[HttpUrl] | None = None

    @field_validator("youtube_url", mode="after")
    def validate_youtube(cls, v):
        if v is None:
            return v
        domain = urlparse(str(v)).netloc
        if not ("youtube.com" in domain or "youtu.be" in domain):
            raise ValueError("La URL debe ser de YouTube")
        return str(v)

    @field_validator("image_url", mode="after")
    def convert_urls_to_str(cls, v):
        if v is None:
            return v
        return [str(url) for url in v]


class TestimonialCreate(SQLModel):
    product: TestimonialProduct
    content: TestimonialContent | None = None
    media: TestimonialMedia | None = None


class TestimonialResponse(SQLModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    product_id: str
    product_name: str

    title: str | None = None
    content: str | None = None
    rating: int | None = None
    author_name: str | None = None

    youtube_url: str | None = None
    image_url: list[str] | None = None

    @model_serializer()
    def to_response(self):
        return {
            "id": self.id,
            "product": {
                "id": self.product_id,
                "name": self.product_name,
            },
            "content": {
                "title": self.title,
                "content": self.content,
                "rating": self.rating,
                "author_name": self.author_name,
            }
            if any([self.title, self.content, self.rating, self.author_name])
            else None,
            "media": {
                "youtube_url": self.youtube_url,
                "image_url": self.image_url,
            }
            if self.youtube_url or self.image_url
            else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class TestimonialUpdate(SQLModel):
    content: TestimonialContent | None = None
    media: TestimonialMedia | None = None
