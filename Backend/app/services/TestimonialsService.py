from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.tag import Tag
from app.models.testimonial import Testimonial
from app.models.testimonial_tag_link import TestimonialTagLink
from app.models.user import User
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate


class TestimonialsService:
    def __init__(self, session):
        self.session = session

    async def create(self, testimonial_data: TestimonialCreate, user_id: str):
        db = self.session

        user = db.get(User, user_id)
        if not user:
            return None

        youtube_url = (
            str(testimonial_data.media.youtube_url)
            if testimonial_data.media and testimonial_data.media.youtube_url
            else None
        )

        image_urls = (
            [str(url) for url in testimonial_data.media.image_urls]
            if testimonial_data.media and testimonial_data.media.image_urls
            else []
        )

        testimonial = Testimonial(
            product_id=testimonial_data.product.id,
            product_name=testimonial_data.product.name,
            title=testimonial_data.content.title if testimonial_data.content else None,
            content=testimonial_data.content.content if testimonial_data.content else None,
            rating=testimonial_data.content.rating if testimonial_data.content else None,
            author_name=testimonial_data.content.author_name if testimonial_data.content else None,
            youtube_url=youtube_url,
            image_urls=image_urls,
            author_id=user_id,
        )

        db.add(testimonial)
        db.commit()
        db.refresh(testimonial)

        tag_objects = []

        for tag_name in testimonial_data.tags:
            result = db.execute(select(Tag).where(Tag.name == tag_name))
            tag = result.scalar_one_or_none()

            if not tag:
                tag = Tag(name=tag_name, slug=tag_name.lower().replace(" ", "-"))
                db.add(tag)
                db.commit()
                db.refresh(tag)

            tag_objects.append(tag)

        for tag in tag_objects:
            link = TestimonialTagLink(testimonial_id=testimonial.id, tag_id=tag.id)
            db.add(link)

        db.commit()
        db.refresh(testimonial)

        return testimonial

    @staticmethod
    async def list_all(db):
        query = select(Testimonial).options(
            selectinload(Testimonial.author), selectinload(Testimonial.tags)
        )

        result = db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update(db, testimonial_data: TestimonialUpdate, user_id: str):
        result = db.execute(select(Testimonial).where(Testimonial.id == testimonial_data.id))
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

        db.commit()
        db.refresh(testimonial)

        return testimonial

    @staticmethod
    async def get(db, id):
        stmt = (
            select(Testimonial)
            .where(Testimonial.id == id)
            .options(selectinload(Testimonial.author), selectinload(Testimonial.tags))
        )
        result = db.execute(stmt)
        testimonial = result.scalar_one_or_none()
        if not testimonial:
            return None

        return testimonial

    @staticmethod
    async def delete(db, id, user_name: str, user_role: str):
        stmt = (
            select(Testimonial)
            .where(Testimonial.id == id)
            .options(selectinload(Testimonial.author), selectinload(Testimonial.tags))
        )
        result = db.execute(stmt)
        if not result:
            return None
        testimonial = result.scalar_one_or_none()
        if not testimonial:
            return "forbidden"
        print(testimonial.author_name)
        print(user_name)
        if testimonial.author_name != user_name:
            """ or user_role != "ADMIN" """
            return "no user"

        db.delete(testimonial)
        db.commit()

        return "deleted"
