from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.router.dependencies import get_current_user
from app.core.db import get_session
from app.models.user import User
from app.schemas.testimonial import TestimonialCreate, TestimonialResponse
from app.services.TestimonialsService import TestimonialsService

router = APIRouter(prefix="/testimonials", tags=["testimonials"])


@router.post("/", response_model=TestimonialResponse, status_code=201)
async def create_testimonial(
    testimonial_data: TestimonialCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    testimonial = await service.create(testimonial_data, user_id=current_user.id)
    response = {
        "id": testimonial.id,
        "created_at": testimonial.created_at,
        "updated_at": testimonial.updated_at,
        "tags": testimonial.tags or [],
        "product": {
            "id": testimonial.product_id,
            "name": testimonial.product_name,
        },
        "content": {
            "title": testimonial.title,
            "content": testimonial.content,
            "rating": testimonial.rating,
            "author_name": testimonial.author_name,
        },
        "media": {
            "youtube_url": testimonial.youtube_url,
            "image_urls": testimonial.image_url,
        },
    }

    return response


@router.get("/", response_model=list[TestimonialResponse])
async def list_testimonials(
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    testimonials = await service.list_all(session)

    # 🔥 Mapeamos cada testimonial igual que en el POST
    response_list = []
    for t in testimonials:
        mapped = {
            "id": t.id,
            "created_at": t.created_at,
            "updated_at": t.updated_at,
            "tags": t.tags or [],
            "product": {
                "id": t.product_id,
                "name": t.product_name,
            },
            "content": {
                "title": t.title,
                "content": t.content,
                "rating": t.rating,
                "author_name": t.author_name,
            },
            "media": {
                "youtube_url": t.youtube_url,
                "image_urls": t.image_url,
            },
        }
        response_list.append(mapped)

    return response_list


@router.get("/{id}", response_model=TestimonialResponse)
async def get_testimonial(
    id: UUID,
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    testimonial = await service.get(session, id)
    response = {
        "id": testimonial.id,
        "created_at": testimonial.created_at,
        "updated_at": testimonial.updated_at,
        "tags": testimonial.tags or [],
        "product": {
            "id": testimonial.product_id,
            "name": testimonial.product_name,
        },
        "content": {
            "title": testimonial.title,
            "content": testimonial.content,
            "rating": testimonial.rating,
            "author_name": testimonial.author_name,
        },
        "media": {
            "youtube_url": testimonial.youtube_url,
            "image_urls": testimonial.image_url,
        },
    }
    return response


@router.put("/{id}", response_model=TestimonialResponse)
async def update_testimonial(
    id: int,
    testimonial_data: TestimonialCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    testimonial = await service.update(id, testimonial_data, current_user.id)
    response = {
        "id": testimonial.id,
        "created_at": testimonial.created_at,
        "updated_at": testimonial.updated_at,
        "tags": testimonial.tags or [],
        "product": {
            "id": testimonial.product_id,
            "name": testimonial.product_name,
        },
        "content": {
            "title": testimonial.title,
            "content": testimonial.content,
            "rating": testimonial.rating,
            "author_name": testimonial.author_name,
        },
        "media": {
            "youtube_url": testimonial.youtube_url,
            "image_urls": testimonial.image_url,
        },
    }
    return response


@router.delete("/{id}")
async def delete_testimonial(
    id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    print(current_user.name)
    return await service.delete(session, id, current_user.name, current_user.role)
