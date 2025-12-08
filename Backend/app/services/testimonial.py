from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import func, or_, select

from app.core.db import SessionDep
from app.models.category import Category
from app.models.tag import Tag
from app.models.testimonial import StatusType, Testimonial
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate
from app.services.category import CategoryService
from app.services.tag import TagService


class TestimonialService:
    @staticmethod
    def create_testimonial(
        data: TestimonialCreate,
        db: SessionDep,
        tenant_owner_id: UUID | None,
    ) -> Testimonial:
        testimonial = Testimonial(
            product_id=data.product.id,
            product_name=data.product.name,
            title=data.content.title if data.content else None,
            content=data.content.content if data.content else None,
            rating=data.content.rating if data.content else None,
            author_name=data.content.author_name if data.content else None,
            youtube_url=data.media.youtube_url if data.media else None,  # type: ignore
            image_url=data.media.image_url if data.media else [],  # type: ignore
            user_id=tenant_owner_id,
        )

        if data.category_name:
            category = CategoryService.get_or_create_category(data.category_name, db)
            testimonial.category_id = category.id

        if data.tags:
            tags = TagService.get_or_create_tags(data.tags, db)
            testimonial.tags = tags

        db.add(testimonial)
        db.commit()
        db.refresh(testimonial, attribute_names=["category", "tags"])
        return testimonial

    @staticmethod
    def get_testimonials(
        db: SessionDep,
        skip: int,
        limit: int,
        tenant_owner_id: UUID,
        search: str | None = None,
        status: str | None = None,
        rating: int | None = None,
        category_name: str | None = None,
        tags: list[str] | None = None,
    ) -> tuple[list[Testimonial], int]:
        """Get testimonials with pagination and filters.

        Args:
            db (SessionDep): database session
            skip (int): number of items to skip
            limit (int): number of items to retrieve
            tenant_owner_id (UUID): tenant owner ID for filtering
            search (str | None): keyword search in title, product_name or content
            status (str | None): filter by status (pending, approved, rejected)
            rating (int | None): filter by rating
            category_name (str | None): filter by category name
            tags (list[str] | None): filter by tag names (testimonials must have all tags)

        Returns:
            tuple: (list of testimonials, total count)
        """

        # Base filter for tenant
        filters = [Testimonial.user_id == tenant_owner_id]

        # Keyword search in title, product_name or content
        if search:
            search_filter = or_(
                Testimonial.title.ilike(f"%{search}%"),  # type: ignore
                Testimonial.product_name.ilike(f"%{search}%"),  # type: ignore
                Testimonial.content.ilike(f"%{search}%"),  # type: ignore
            )
            filters.append(search_filter)  # type: ignore

        # Filter by status
        if status:
            filters.append(Testimonial.status == status)  # type: ignore

        # Filter by rating
        if rating is not None:
            filters.append(Testimonial.rating >= rating)  # type: ignore

        # Build base query
        query = select(Testimonial).where(*filters)

        # Filter by category name (requires join)
        if category_name:
            query = query.join(Category).where(
                Category.name.ilike(f"%{category_name}%")  # type: ignore
            )

        # Filter by tags (requires join - testimonials must have ALL specified tags)
        if tags:
            for tag_name in tags:
                query = query.join(Testimonial.tags.and_(Tag.name == tag_name))  # type: ignore

        # Count total items with filters
        count_query = select(func.count()).select_from(query.subquery())
        total_items = db.exec(count_query).one()

        # Get testimonials with eager loading
        testimonials = db.exec(
            query.options(selectinload(Testimonial.category), selectinload(Testimonial.tags))  # type: ignore
            .offset(skip)
            .limit(limit)
            .order_by(Testimonial.created_at.desc())  # type: ignore
        ).all()

        return list(testimonials), total_items

    @staticmethod
    def get_testimonial_by_id(
        testimonial_id: UUID,
        db: SessionDep,
        tenant_owner_id: UUID,
    ) -> Testimonial | None:
        testimonial = db.exec(
            select(Testimonial).where(
                Testimonial.id == testimonial_id,
                Testimonial.user_id == tenant_owner_id,
            )
        ).first()
        return testimonial

    @staticmethod
    def update_testimonial(
        data: TestimonialUpdate,
        db: SessionDep,
        tenant_owner_id: UUID,
        testimonial_id: UUID,
    ) -> Testimonial:
        testimonial = db.get(Testimonial, testimonial_id)
        if not testimonial or testimonial.user_id != tenant_owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Testimonial not found",
            )

        # Update content fields if provided
        if data.content:
            content_data = data.content.model_dump(exclude_unset=True)
            for field, value in content_data.items():
                setattr(testimonial, field, value)

        # Update media fields if provided
        if data.media:
            media_data = data.media.model_dump(exclude_unset=True)
            for field, value in media_data.items():
                setattr(testimonial, field, value)

        # Update category if provided
        if data.category_name:
            category = CategoryService.get_or_create_category(data.category_name, db)
            testimonial.category_id = category.id

        # Update tags if provided
        if data.tags:
            tags = TagService.get_or_create_tags(data.tags, db)
            testimonial.tags = tags

        db.add(testimonial)
        db.commit()
        db.refresh(testimonial, attribute_names=["category", "tags"])
        return testimonial

    @staticmethod
    def soft_delete_testimonial(
        testimonial_id: UUID,
        db: SessionDep,
        tenant_owner_id: UUID,
    ) -> bool:
        testimonial = db.get(Testimonial, testimonial_id)
        if not testimonial or testimonial.user_id != tenant_owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found"
            )

        testimonial.is_active = False
        db.add(testimonial)
        db.commit()
        return True

    @staticmethod
    def update_status(
        testimonial_id: UUID,
        new_status: StatusType,
        db: SessionDep,
        tenant_owner_id: UUID,
    ) -> bool:
        testimonial = db.get(Testimonial, testimonial_id)
        if not testimonial or testimonial.user_id != tenant_owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found"
            )

        testimonial.status = new_status  # type: ignore
        db.add(testimonial)
        db.commit()
        return True
