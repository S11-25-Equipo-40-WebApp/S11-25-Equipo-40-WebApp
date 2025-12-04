import pytest
from pydantic import ValidationError

from app.schemas import CategoryCreate, TagCreate, TestimonialCreate, UserCreate
from app.utils.validators.slug import generate_slug


def test_categorycreate_generates_slug():
    cat = CategoryCreate(name=" --Nueva Categoría.")
    assert cat.slug == generate_slug(" --Nueva Categoría.")


def test_tagcreate_generates_slug():
    tag = TagCreate(name=" --Nuevo Tag.")
    assert tag.slug == generate_slug(" --Nuevo Tag.")


def test_testimonial_create():
    t = TestimonialCreate(
        product={"id": "123", "name": "Producto de prueba"},
        content={"title": "Titulo valido", "content": "Contenido suficientemente largo"},
    )
    assert t.product.id == "123"
    assert t.content.content == "Contenido suficientemente largo"


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
