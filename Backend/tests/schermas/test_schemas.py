import pytest
from pydantic import ValidationError

from app.models.testimonial import MediaType
from app.schemas import CategoryCreate, TagCreate, TestimonialCreate, UserCreate
from app.utils.validators.slug import generate_slug


def test_categorycreate_generates_slug():
    cat = CategoryCreate(name=" --Nueva Categoría.")
    assert cat.slug == generate_slug(" --Nueva Categoría.")


def test_tagcreate_generates_slug():
    cat = TagCreate(name=" --Nuevo Tag.")
    assert cat.slug == generate_slug(" --Nuevo Tag.")


def test_testimonial_create_text_clears_media_url():
    t = TestimonialCreate(
        title="Titulo valido",
        content="Contenido suficientemente largo",
        media_type=MediaType.TEXT,
        media_url="http://example.com/video.mp4",
    )
    assert t.media_url is None


def test_testimonial_create_nontext_requires_media_url():
    with pytest.raises(ValidationError):
        TestimonialCreate(
            title="Titulo valido",
            content="Contenido suficientemente largo",
            media_type=MediaType.VIDEO,
        )


def test_usercreate_password_less_8_characters():
    with pytest.raises(ValidationError):
        UserCreate(
            email="testuser@example.com",
            password="short",
        )


def test_usercreate_password_no_number():
    with pytest.raises(ValidationError):
        UserCreate(
            email="testuser@example.com",
            password="NoNumbersHere!",
        )
