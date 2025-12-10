from sqlmodel import select

from app.core.db import SessionDep
from app.models import Category
from app.utils.validators.slug import generate_slug


class CategoryService:
    @staticmethod
    def get_or_create_category(name: str, db: SessionDep) -> Category:
        slug = generate_slug(name)

        category = db.exec(select(Category).where(Category.slug == slug)).first()

        if category:
            return category

        # Crear si no existe
        new_category = Category(name=name.strip().lower(), slug=slug)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    @staticmethod
    def get_all_categories(db: SessionDep) -> list[Category]:
        """Retrieve all categories from the database.

        Args:
            db (SessionDep): database session
        Returns:
            list[Category]: list of all categories
        """
        categories = db.exec(select(Category)).all()
        return list(categories)
