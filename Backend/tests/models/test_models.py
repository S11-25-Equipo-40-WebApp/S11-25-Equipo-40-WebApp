from sqlmodel import Session, SQLModel, create_engine

from app.models import Category, Tag, Testimonial, User
from app.schemas import CategoryCreate
from app.utils.validators.slug import generate_slug


def test_category_schema_generates_slug():
    cat = CategoryCreate(name="Mi Categoria")
    assert cat.slug == generate_slug("Mi Categoria")


def test_testimonial_author_relationship_and_m2m():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # create user and category
        user = User(name="usuario", email="u@example.com", password="pw")
        category = Category(name="cat", slug="cat")
        session.add_all([user, category])
        session.commit()
        session.refresh(user)
        session.refresh(category)

        # create testimonial and tags
        testimonial = Testimonial(
            title="Titulo",
            content="Contenido",
            author_id=user.id,
            category_id=category.id,
        )
        tag1 = Tag(name="tag1", slug="tag1")
        tag2 = Tag(name="tag2", slug="tag2")

        session.add_all([testimonial, tag1, tag2])
        session.commit()
        session.refresh(testimonial)
        session.refresh(tag1)
        session.refresh(tag2)

        # associate tags (many-to-many)
        testimonial.tags.append(tag1)
        testimonial.tags.append(tag2)
        session.add(testimonial)
        session.commit()

        # reload
        session.refresh(testimonial)
        session.refresh(tag1)

        # checks
        assert testimonial.author_id == user.id
        assert len(testimonial.tags) == 2
        assert testimonial in tag1.testimonials
