from uuid import UUID

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

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
from app.services.cloudinary import CloudinaryService
from app.services.testimonial import TestimonialService
from app.services.user import UserService

router = APIRouter(
    prefix="/testimonials",
    tags=["Testimonial"],
)


@router.post(
    "/upload-images",
    status_code=status.HTTP_200_OK,
    summary="Upload images to Cloudinary",
    description="Upload images and receive URLs to use in testimonial creation",
)
def upload_images(
    api_key: APIKeyPublicDep,
    images: list[UploadFile] | None = File(default=None, description="Images to upload (max 5)"),
):
    """Upload images to Cloudinary and return their secure URLs.

    Use this endpoint before creating a testimonial to get image URLs.
    Then include those URLs in the `media.image_url` field when creating the testimonial.
    """
    if not images:
        return {"image_url": []}

    if len(images) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 5 images allowed per upload",
        )

    image_urls = CloudinaryService.upload_images(images)
    return {"image_url": image_urls}


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
    """Create a new testimonial with JSON body.

    If you need to upload images, use POST /testimonials/upload-images first
    to get the URLs, then include them in `media.image_url`.

    Args:
    - data (TestimonialCreate): data for creating the testimonial
    - db (SessionDep): database session
    - api_key (APIKeyPublicDep): API key for authentication

    Returns:
    - TestimonialResponse: the newly created testimonial
    """
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
    """Get testimonials with pagination and optional filters.

    Args:
    - db (SessionDep): database session
    - current_user (ModeratorDep): current user making the request (guaranteed to be moderator or higher by ModeratorDep)
    - skip (int, optional): Number of items to skip. Defaults to Query(0, ge=0, description="Number of items to skip").
    - limit (int, optional): Number of items to retrieve. Defaults to Query(10, ge=1, le=100, description="Number of items to retrieve").
    - search (str | None, optional): Search in title, product name or content. Defaults to Query(None, description="Search in title, product name or content").
    - status (StatusType | None, optional): Filter by status (pending, approved, rejected). Defaults to Query( None, description="Filter by status (pending, approved, rejected)" ).
    - rating (int | None, optional): Filter by rating (0-5). Defaults to Query(None, ge=0, le=5, description="Filter by rating (0-5)").
    - category_name (str | None, optional): Filter by category name. Defaults to Query(None, description="Filter by category name").
    - tags (list[str] | None, optional): Filter by tags (must match all). Defaults to Query(None, description="Filter by tags (must match all)").

    Returns:
    - PaginationResponse[TestimonialResponse]: Paginated response containing testimonials
    """
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
    """Get a testimonial by its ID.

    Args:
    - testimonial_id (UUID): ID of the testimonial to retrieve
    - db (SessionDep): database session
    - current_user (ModeratorDep): current user making the request (guaranteed to be moderator or higher by ModeratorDep)

    Raises:
    - HTTPException: if the testimonial is not found

    Returns:
    - TestimonialResponse: the retrieved testimonial
    """
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
    """Update a testimonial by its ID.

    Args:
    - testimonial_id (UUID): ID of the testimonial to update
    - data (TestimonialUpdate): data to update the testimonial with
    - db (SessionDep): database session
    - current_user (ModeratorDep): current user making the request (guaranteed to be moderator or higher by ModeratorDep)

    Returns:
    - TestimonialResponse: the updated testimonial
    """
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
    """Soft delete a testimonial by its ID.

    Args:
    - testimonial_id (UUID): ID of the testimonial to soft delete
    - db (SessionDep): database session
    - current_user (ModeratorDep): current user making the request (guaranteed to be moderator or higher by ModeratorDep)

    Returns:
    - None
    """
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
    """Update the status of a testimonial.

    Args:
    - testimonial_id (UUID): ID of the testimonial to update the status for
    - data (TestimonialStatusUpdate): data containing the new status
    - db (SessionDep): database session
    - current_user (ModeratorDep): current user making the request (guaranteed to be moderator or higher by ModeratorDep)

    Returns:
    - None
    """
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    TestimonialService.update_status(testimonial_id, data.status, db, tenant_owner_id)
    return {"message": f"Testimonial status updated to {data.status.value}"}
