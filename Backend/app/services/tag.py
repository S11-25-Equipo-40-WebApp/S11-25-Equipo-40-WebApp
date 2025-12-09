from sqlmodel import select

from app.core.db import SessionDep
from app.models.tag import Tag
from app.utils.validators.slug import generate_slug


class TagService:
    @staticmethod
    def get_or_create_tags(tag_names: list[str], db: SessionDep) -> list[Tag]:
        tags = []
        for name in tag_names:
            slug = generate_slug(name)
            tag = db.exec(select(Tag).where(Tag.slug == slug)).first()
            if not tag:
                tag = Tag(name=name.strip().lower(), slug=slug)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            tags.append(tag)
        return tags

    @staticmethod
    def get_all_tags(db: SessionDep) -> list[Tag]:
        """Retrieve all tags from the database.

        Args:
            db (SessionDep): database session
        Returns:
            list[Tag]: list of all tags
        """
        tags = db.exec(select(Tag)).all()
        return list(tags)
