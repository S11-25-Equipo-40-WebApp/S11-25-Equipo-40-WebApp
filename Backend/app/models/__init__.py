"""
Models package.

Import all models here to ensure they are registered with SQLModel/SQLAlchemy.
This is important for relationships to work correctly.
"""

# Import link table first, then other models
from .category import Category
from .tag import Tag
from .testimonial import Testimonial
from .testimonial_tag_link import TestimonialTagLink
from .user import User

__all__ = [
    "User",
    "Category",
    "Tag",
    "Testimonial",
    "TestimonialTagLink",
]
