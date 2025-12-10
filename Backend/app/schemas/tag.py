from datetime import datetime
from uuid import UUID

from pydantic import model_validator
from sqlmodel import Field, SQLModel

from app.utils.validators.slug import generate_slug


class TagCreate(SQLModel):
    name: str = Field(min_length=1, max_length=100, description="The name of the tag")
    slug: str | None = Field(
        default=None,
        exclude=True,
    )

    @model_validator(mode="after")
    def set_slug(self):
        self.slug = generate_slug(self.name)
        return self


class TagResponse(SQLModel):
    id: UUID
    name: str
    slug: str
    created_at: datetime


class TagUpdate(SQLModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="The updated name of the tag",
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
