from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.tag import Tag
from app.models.testimonial import Testimonial
from app.models.testimonial_tag_link import TestimonialTagLink
from app.models.user import User
from app.schemas.testimonials import TestimonialCreate, TestimonialUpdate


class TestimonialsService:
    def __init__(self, session):
        self.session = session

    async def create(self, testimonial_data: TestimonialCreate, user_id: str):
        db = self.session

        user = await db.get(User, user_id)
        if not user:
            return None

        testimonial = Testimonial(
            title=testimonial_data.title,
            content=testimonial_data.content,
            media_type=testimonial_data.media_type,
            media_url=testimonial_data.media_url,
            author_id=user_id,
        )

        db.add(testimonial)
        await db.commit()
        await db.refresh(testimonial)

        tag_objects = []

        for tag_name in testimonial_data.tags:
            result = await db.execute(select(Tag).where(Tag.name == tag_name))
            tag = result.scalar_one_or_none()

            if not tag:
                tag = Tag(name=tag_name, slug=tag_name.lower().replace(" ", "-"))
                db.add(tag)
                await db.commit()
                await db.refresh(tag)

            tag_objects.append(tag)

        for tag in tag_objects:
            link = TestimonialTagLink(testimonial_id=testimonial.id, tag_id=tag.id)
            db.add(link)

        await db.commit()
        await db.refresh(testimonial)

        return testimonial

    @staticmethod
    async def list_all(db):
        query = select(Testimonial).options(
            selectinload(Testimonial.author), selectinload(Testimonial.tags)
        )

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update(db, testimonial_data: TestimonialUpdate, user_id: str):
        result = await db.execute(select(Testimonial).where(Testimonial.id == testimonial_data.id))
        testimonial = result.scalar_one_or_none()
        if not testimonial:
            return None
        testimonial.title = testimonial_data.title
        testimonial.content = testimonial_data.content
        testimonial.media_type = testimonial_data.media_type
        testimonial.media_url = testimonial_data.media_url
        testimonial.status = testimonial_data.status
        testimonial.author_id = user_id
        testimonial.category_id = testimonial_data.category_id

        tag_objects = []

        for tag_name in testimonial_data.tags:
            result = await db.execute(select(Tag).where(Tag.name == tag_name))
            tag = result.scalar_one_or_none()

            if not tag:
                tag = Tag(name=tag_name, slug=tag_name.lower().replace(" ", "-"))
                db.add(tag)
                await db.commit()
                await db.refresh(tag)

            tag_objects.append(tag)

        for tag in tag_objects:
            link = TestimonialTagLink(testimonial_id=testimonial.id, tag_id=tag.id)
            db.add(link)

        await db.commit()
        await db.refresh(testimonial)

        return testimonial

    @staticmethod
    async def get(db, id):
        stmt = (
            select(Testimonial)
            .where(Testimonial.id == id)
            .options(selectinload(Testimonial.author), selectinload(Testimonial.tags))
        )
        result = await db.execute(stmt)
        testimonial = result.scalar_one_or_none()
        if not testimonial:
            return None

        return testimonial

    @staticmethod
    async def delete(db, id, user_id: str, user_role: str):
        stmt = (
            select(Testimonial)
            .where(Testimonial.id == id)
            .options(selectinload(Testimonial.author), selectinload(Testimonial.tags))
        )
        result = await db.execute(stmt)
        if not result:
            return None
        testimonial = result.scalar_one_or_none()
        if not testimonial:
            return None
        if testimonial.author_id != user_id:
            """ or user_role != "ADMIN" """
            return None

        await db.delete(testimonial)
        await db.commit()

        return testimonial
