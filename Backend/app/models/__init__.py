"""
Models package.

Import all models here to ensure they are registered with SQLModel/SQLAlchemy.
This is important for relationships to work correctly.
"""

# Import link table first, then other models
from .abstract import Abstract, AbstractActive
from .api_key import APIKey
from .category import Category
from .tag import Tag
from .testimonial import Testimonial
from .testimonial_tag_link import TestimonialTagLink
from .user import User

__all__ = [
    "Abstract",
    "AbstractActive",
    "APIKey",
    "User",
    "Category",
    "Tag",
    "Testimonial",
    "TestimonialTagLink",
]
