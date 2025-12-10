from datetime import datetime
from uuid import UUID

from pydantic import model_validator
from sqlmodel import Field, SQLModel

from app.utils.validators.slug import generate_slug


class CategoryCreate(SQLModel):
    name: str = Field(min_length=1, max_length=100, description="Name of the category")
    slug: str | None = Field(
        default=None,
        exclude=True,
    )

    @model_validator(mode="after")
    def set_slug(self):
        self.slug = generate_slug(self.name)
        return self


class CategoryResponse(SQLModel):
    id: UUID
    name: str
    slug: str
    created_at: datetime


class CategoryUpdate(SQLModel):
    name: str | None = Field(
        default=None, min_length=1, max_length=100, description="Updated name of the category"
    )
    slug: str | None = Field(
        default=None,
        exclude=True,
    )

    @model_validator(mode="after")
    def set_slug(self):
        if self.name is not None:
            self.slug = generate_slug(self.name)
        return self
