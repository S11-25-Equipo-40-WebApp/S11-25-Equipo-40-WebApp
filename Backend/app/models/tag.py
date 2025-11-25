from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from .abstract import Abstract
from .testimonial_tag_link import TestimonialTagLink

if TYPE_CHECKING:
    from .testimonial import Testimonial


class Tag(Abstract, table=True):
    name: str = Field(index=True, unique=True)
    slug: str = Field(index=True, unique=True)

    # relationships
    testimonials: list["Testimonial"] = Relationship(
        back_populates="tags", link_model=TestimonialTagLink
    )
