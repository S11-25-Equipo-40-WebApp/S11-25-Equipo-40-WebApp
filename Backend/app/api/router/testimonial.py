from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.core.db import SessionDep
from app.core.deps import APIKeyPublicDep, ModeratorDep
from app.models.testimonial import StatusType
from app.schemas.pagination import PaginationResponse
from app.schemas.testimonial import (
    TestimonialCreate,
    TestimonialResponse,
    TestimonialStatusUpdate,
    TestimonialUpdate,
)
from app.services.api_keys import APIKeyService
from app.services.testimonial import TestimonialService
from app.services.user import UserService

router = APIRouter(
    prefix="/testimonials",
    tags=["Testimonial"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TestimonialResponse,
)
def create_testimonial(
    data: TestimonialCreate,
    db: SessionDep,
    api_key: APIKeyPublicDep,
):
    tenant_owner_id = APIKeyService.get_tenant_owner_id_from_api_key(api_key)
    testimonial = TestimonialService.create_testimonial(data, db, tenant_owner_id)
    return TestimonialResponse(
        **testimonial.model_dump(),
        category_name=testimonial.category.name if testimonial.category else None,
        tags=[tag.name for tag in testimonial.tags] if testimonial.tags else None,
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PaginationResponse[TestimonialResponse],
)
def get_testimonials(
    db: SessionDep,
    current_user: ModeratorDep,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to retrieve"),
    search: str | None = Query(None, description="Search in title, product name or content"),
    status: StatusType | None = Query(
        None, description="Filter by status (pending, approved, rejected)"
    ),
    rating: int | None = Query(None, ge=0, le=5, description="Filter by rating (0-5)"),
    category_name: str | None = Query(None, description="Filter by category name"),
    tags: list[str] | None = Query(None, description="Filter by tags (must match all)"),
):
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    testimonials, total_items = TestimonialService.get_testimonials(
        db=db,
        skip=skip,
        limit=limit,
        tenant_owner_id=tenant_owner_id,
        search=search,
        status=status,
        rating=rating,
        category_name=category_name,
        tags=tags,
    )

    testimonial_responses = [
        TestimonialResponse(
            **t.model_dump(),
            category_name=t.category.name if t.category else None,
            tags=[tag.name for tag in t.tags] if t.tags else None,
        )
        for t in testimonials
    ]

    total_pages = (total_items + limit - 1) // limit
    return PaginationResponse(
        total_items=total_items,
        results=testimonial_responses,
        page=skip // limit + 1,
        size=limit,
        total_pages=total_pages,
        has_next=(skip + limit) < total_items,
        has_prev=skip > 0,
    )


@router.get(
    "/{testimonial_id}",
    status_code=status.HTTP_200_OK,
    response_model=TestimonialResponse,
)
def get_testimonial_by_id(
    testimonial_id: UUID,
    db: SessionDep,
    current_user: ModeratorDep,
):
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    testimonial = TestimonialService.get_testimonial_by_id(testimonial_id, db, tenant_owner_id)
    if not testimonial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found")
    return TestimonialResponse(
        **testimonial.model_dump(),
        category_name=testimonial.category.name if testimonial.category else None,
        tags=[tag.name for tag in testimonial.tags] if testimonial.tags else None,
    )


@router.patch(
    "/{testimonial_id}",
    status_code=status.HTTP_200_OK,
    response_model=TestimonialResponse,
)
def update_testimonial(
    testimonial_id: UUID,
    data: TestimonialUpdate,
    db: SessionDep,
    current_user: ModeratorDep,
):
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    testimonial = TestimonialService.update_testimonial(
        data=data,
        db=db,
        tenant_owner_id=tenant_owner_id,
        testimonial_id=testimonial_id,
    )
    return TestimonialResponse(
        **testimonial.model_dump(),
        category_name=testimonial.category.name if testimonial.category else None,
        tags=[tag.name for tag in testimonial.tags] if testimonial.tags else None,
    )


@router.patch(
    "/delete/{testimonial_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def soft_delete_testimonial(
    testimonial_id: UUID,
    db: SessionDep,
    current_user: ModeratorDep,
):
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    return TestimonialService.soft_delete_testimonial(testimonial_id, db, tenant_owner_id)


@router.patch(
    "/{testimonial_id}/status",
    status_code=status.HTTP_200_OK,
)
def update_testimonial_status(
    testimonial_id: UUID,
    data: TestimonialStatusUpdate,
    db: SessionDep,
    current_user: ModeratorDep,
):
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    TestimonialService.update_status(testimonial_id, data.status, db, tenant_owner_id)
    return {"message": f"Testimonial status updated to {data.status.value}"}
