from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from .abstract import Abstract

if TYPE_CHECKING:
    from .testimonial import Testimonial


class Category(Abstract, table=True):
    name: str = Field(index=True)
    slug: str = Field(index=True, unique=True)

    # relationships
    testimonials: list["Testimonial"] = Relationship(back_populates="category")
