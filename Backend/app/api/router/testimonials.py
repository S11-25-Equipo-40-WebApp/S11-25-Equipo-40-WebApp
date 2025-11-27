from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.router.dependencies import get_current_user
from app.core.db import get_session
from app.models.user import User
from app.schemas.testimonials import TestimonialCreate, TestimonialResponse
from app.services.TestimonialsService import TestimonialsService

router = APIRouter(prefix="/testimonials", tags=["testimonials"])


@router.post("/", response_model=TestimonialResponse, status_code=201)
async def create_testimonial(
    testimonial_data: TestimonialCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    return await service.create(testimonial_data, user_id=current_user.id)


@router.get("/", response_model=list[TestimonialResponse])
async def list_testimonials(
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    return await service.list_all(session)


@router.get("/{id}", response_model=TestimonialResponse)
async def get_testimonial(
    id: UUID,
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    return await service.get(session, id)


@router.put("/{id}", response_model=TestimonialResponse)
async def update_testimonial(
    id: int,
    testimonial_data: TestimonialCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    return await service.update(id, testimonial_data, current_user.id)


@router.delete("/{id}")
async def delete_testimonial(
    id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = TestimonialsService(session)
    return await service.delete(session, id, current_user.id, current_user.roles)
