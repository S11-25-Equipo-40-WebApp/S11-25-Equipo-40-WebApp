import uuid

from sqlalchemy import select

from app.models.testimonial import Testimonial
from app.models.user import User
from app.schemas.testimonials import TestimonialCreate


class TestimonialsService:
    @staticmethod
    async def create(db, testimonial_data: TestimonialCreate, user_id: str):
        user = await db.get(User, user_id)
        if not user:
            return None
        testimonial = Testimonial(
            id=uuid.uuid4(),
            title=testimonial_data.title,
            content=testimonial_data.content,
            media_type=testimonial_data.media_type,
            media_url=testimonial_data.media_url,
            status=testimonial_data.status,
            author_id=user_id,
            category_id=testimonial_data.category_id,
        )

        db.add(testimonial)
        await db.commit()
        await db.refresh(testimonial)

        return testimonial

    @staticmethod
    async def list_testimonials(db):
        result = await db.execute(select(Testimonial))
        return result.scalars().all()
