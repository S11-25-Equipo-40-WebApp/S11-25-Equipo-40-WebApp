from uuid import UUID

from sqlmodel import Field, SQLModel


class TestimonialTagLink(SQLModel, table=True):
    testimonial_id: UUID = Field(foreign_key="testimonial.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tag.id", primary_key=True)
