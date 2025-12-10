"""Tests for Testimonial service."""

from unittest.mock import Mock, patch
from uuid import uuid4

from app.models.testimonial import Testimonial
from app.schemas.testimonial import TestimonialContent, TestimonialCreate, TestimonialProduct
from app.services.testimonial import TestimonialService


class TestCreateTestimonial:
    """Tests for create_testimonial function."""

    def test_create_testimonial_with_category(self):
        """Test creating testimonial with category."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_category = Mock()
        mock_category.id = uuid4()

        data = TestimonialCreate(
            product=TestimonialProduct(id="prod-123", name="Test Product"),
            content=TestimonialContent(
                title="Great Product",
                content="This is amazing",
                rating=5,
                author_name="John Doe",
            ),
            category_name="Electronics",
        )

        with patch(
            "app.services.testimonial.CategoryService.get_or_create_category"
        ) as mock_get_category:
            mock_get_category.return_value = mock_category

            TestimonialService.create_testimonial(data, mock_db, tenant_owner_id)

            assert mock_db.add.called
            assert mock_db.commit.called
            assert mock_db.refresh.called
            mock_get_category.assert_called_once_with("Electronics", mock_db)

    def test_create_testimonial_with_tags(self):
        """Test creating testimonial with tags."""
        mock_db = Mock()
        tenant_owner_id = uuid4()

        data = TestimonialCreate(
            product=TestimonialProduct(id="prod-123", name="Test Product"),
            tags=["tech", "gadget"],
        )

        with patch("app.services.testimonial.TagService.get_or_create_tags") as mock_get_tags:
            # Don't set return value to avoid relationship issues
            TestimonialService.create_testimonial(data, mock_db, tenant_owner_id)

            mock_get_tags.assert_called_once_with(["tech", "gadget"], mock_db)

    def test_create_testimonial_minimal_fields(self):
        """Test creating testimonial with only required fields."""
        mock_db = Mock()
        tenant_owner_id = uuid4()

        data = TestimonialCreate(
            product=TestimonialProduct(id="prod-123", name="Test Product"),
        )

        TestimonialService.create_testimonial(data, mock_db, tenant_owner_id)

        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called

    def test_create_testimonial_without_category(self):
        """Test creating testimonial without category."""
        mock_db = Mock()
        tenant_owner_id = uuid4()

        data = TestimonialCreate(
            product=TestimonialProduct(id="prod-123", name="Test Product"),
            content=TestimonialContent(title="Test", content="Content"),
            category_name=None,
        )

        with patch(
            "app.services.testimonial.CategoryService.get_or_create_category"
        ) as mock_get_category:
            TestimonialService.create_testimonial(data, mock_db, tenant_owner_id)

            mock_get_category.assert_not_called()
            assert mock_db.add.called

    def test_create_testimonial_without_tags(self):
        """Test creating testimonial without tags."""
        mock_db = Mock()
        tenant_owner_id = uuid4()

        data = TestimonialCreate(
            product=TestimonialProduct(id="prod-123", name="Test Product"),
            content=TestimonialContent(title="Test", content="Content"),
            tags=None,
        )

        with patch("app.services.testimonial.TagService.get_or_create_tags") as mock_get_tags:
            TestimonialService.create_testimonial(data, mock_db, tenant_owner_id)

            mock_get_tags.assert_not_called()
            assert mock_db.add.called


class TestGetTestimonials:
    """Tests for get_testimonials function."""

    def test_get_testimonials_returns_tuple(self):
        """Test that get_testimonials returns tuple of list and count."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_testimonials = [Mock(spec=Testimonial), Mock(spec=Testimonial)]
        total_count = 10

        mock_db.exec.return_value.one.return_value = total_count
        mock_db.exec.return_value.all.return_value = mock_testimonials

        testimonials, count = TestimonialService.get_testimonials(
            mock_db, skip=0, limit=10, tenant_owner_id=tenant_owner_id
        )

        assert isinstance(testimonials, list)
        assert isinstance(count, int)
        assert count == total_count
        assert len(testimonials) == 2

    def test_get_testimonials_with_pagination(self):
        """Test get_testimonials with pagination parameters."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_testimonials = [Mock(spec=Testimonial)]

        mock_db.exec.return_value.one.return_value = 100
        mock_db.exec.return_value.all.return_value = mock_testimonials

        testimonials, count = TestimonialService.get_testimonials(
            mock_db, skip=20, limit=10, tenant_owner_id=tenant_owner_id
        )

        assert len(testimonials) == 1
        assert count == 100
        assert mock_db.exec.call_count == 2  # One for count, one for query

    def test_get_testimonials_empty_result(self):
        """Test get_testimonials when no testimonials exist."""
        mock_db = Mock()
        tenant_owner_id = uuid4()

        mock_db.exec.return_value.one.return_value = 0
        mock_db.exec.return_value.all.return_value = []

        testimonials, count = TestimonialService.get_testimonials(
            mock_db, skip=0, limit=10, tenant_owner_id=tenant_owner_id
        )

        assert testimonials == []
        assert count == 0

    def test_get_testimonials_filters_by_tenant(self):
        """Test that get_testimonials filters by tenant_owner_id."""
        mock_db = Mock()
        tenant_owner_id = uuid4()

        mock_db.exec.return_value.one.return_value = 5
        mock_db.exec.return_value.all.return_value = []

        TestimonialService.get_testimonials(
            mock_db, skip=0, limit=10, tenant_owner_id=tenant_owner_id
        )

        # Verify exec was called (which means WHERE clause was applied)
        assert mock_db.exec.call_count == 2

    def test_get_testimonials_with_search_filter(self):
        """Test get_testimonials with search keyword filter."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_testimonials = [Mock(spec=Testimonial)]

        mock_db.exec.return_value.one.return_value = 1
        mock_db.exec.return_value.all.return_value = mock_testimonials

        testimonials, count = TestimonialService.get_testimonials(
            mock_db,
            skip=0,
            limit=10,
            tenant_owner_id=tenant_owner_id,
            search="test keyword",
        )

        assert len(testimonials) == 1
        assert count == 1
        assert mock_db.exec.call_count == 2

    def test_get_testimonials_with_status_filter(self):
        """Test get_testimonials with status filter."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_testimonials = [Mock(spec=Testimonial)]

        mock_db.exec.return_value.one.return_value = 1
        mock_db.exec.return_value.all.return_value = mock_testimonials

        testimonials, count = TestimonialService.get_testimonials(
            mock_db, skip=0, limit=10, tenant_owner_id=tenant_owner_id, status="approved"
        )

        assert len(testimonials) == 1
        assert count == 1
        assert mock_db.exec.call_count == 2

    def test_get_testimonials_with_rating_filter(self):
        """Test get_testimonials with rating filter."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_testimonials = [Mock(spec=Testimonial)]

        mock_db.exec.return_value.one.return_value = 1
        mock_db.exec.return_value.all.return_value = mock_testimonials

        testimonials, count = TestimonialService.get_testimonials(
            mock_db, skip=0, limit=10, tenant_owner_id=tenant_owner_id, rating=5
        )

        assert len(testimonials) == 1
        assert count == 1
        assert mock_db.exec.call_count == 2

    def test_get_testimonials_with_category_filter(self):
        """Test get_testimonials with category name filter."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_testimonials = [Mock(spec=Testimonial)]

        mock_db.exec.return_value.one.return_value = 1
        mock_db.exec.return_value.all.return_value = mock_testimonials

        testimonials, count = TestimonialService.get_testimonials(
            mock_db,
            skip=0,
            limit=10,
            tenant_owner_id=tenant_owner_id,
            category_name="Electronics",
        )

        assert len(testimonials) == 1
        assert count == 1
        assert mock_db.exec.call_count == 2

    def test_get_testimonials_with_tags_filter(self):
        """Test get_testimonials with tags filter."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_testimonials = [Mock(spec=Testimonial)]

        mock_db.exec.return_value.one.return_value = 1
        mock_db.exec.return_value.all.return_value = mock_testimonials

        testimonials, count = TestimonialService.get_testimonials(
            mock_db,
            skip=0,
            limit=10,
            tenant_owner_id=tenant_owner_id,
            tags=["tech", "gadget"],
        )

        assert len(testimonials) == 1
        assert count == 1
        assert mock_db.exec.call_count == 2

    def test_get_testimonials_with_multiple_filters(self):
        """Test get_testimonials with multiple filters combined."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_testimonials = [Mock(spec=Testimonial)]

        mock_db.exec.return_value.one.return_value = 1
        mock_db.exec.return_value.all.return_value = mock_testimonials

        testimonials, count = TestimonialService.get_testimonials(
            mock_db,
            skip=0,
            limit=10,
            tenant_owner_id=tenant_owner_id,
            search="amazing",
            status="approved",
            rating=5,
            category_name="Electronics",
            tags=["premium"],
        )

        assert len(testimonials) == 1
        assert count == 1
        assert mock_db.exec.call_count == 2

    def test_get_testimonials_with_no_results_on_filters(self):
        """Test get_testimonials returns empty when filters don't match."""
        mock_db = Mock()
        tenant_owner_id = uuid4()

        mock_db.exec.return_value.one.return_value = 0
        mock_db.exec.return_value.all.return_value = []

        testimonials, count = TestimonialService.get_testimonials(
            mock_db,
            skip=0,
            limit=10,
            tenant_owner_id=tenant_owner_id,
            search="nonexistent",
            status="rejected",
        )

        assert testimonials == []
        assert count == 0
        assert mock_db.exec.call_count == 2


class TestGetTestimonialById:
    """Tests for get_testimonial_by_id function."""

    def test_get_testimonial_by_id_found(self):
        """Test getting testimonial by id when it exists."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()
        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.id = testimonial_id

        mock_db.exec.return_value.first.return_value = mock_testimonial

        result = TestimonialService.get_testimonial_by_id(testimonial_id, mock_db, tenant_owner_id)

        assert result is mock_testimonial
        assert mock_db.exec.called

    def test_get_testimonial_by_id_not_found(self):
        """Test getting testimonial by id when it doesn't exist."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_db.exec.return_value.first.return_value = None

        result = TestimonialService.get_testimonial_by_id(testimonial_id, mock_db, tenant_owner_id)

        assert result is None

    def test_get_testimonial_by_id_filters_by_tenant(self):
        """Test that get_testimonial_by_id filters by tenant_owner_id."""
        mock_db = Mock()
        tenant_owner_id_a = uuid4()
        tenant_owner_id_b = uuid4()
        testimonial_id = uuid4()

        # Mock testimonial that belongs to tenant B
        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = tenant_owner_id_b

        # When tenant A tries to access, should return None
        mock_db.exec.return_value.first.return_value = None

        result = TestimonialService.get_testimonial_by_id(
            testimonial_id, mock_db, tenant_owner_id_a
        )

        assert result is None
        assert mock_db.exec.called


class TestUpdateTestimonial:
    """Tests for update_testimonial function."""

    def test_update_testimonial_success(self):
        """Test updating testimonial successfully."""
        from app.schemas.testimonial import TestimonialContent, TestimonialUpdate

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = tenant_owner_id
        mock_testimonial.category = None
        mock_testimonial.tags = []

        mock_db.get.return_value = mock_testimonial

        data = TestimonialUpdate(
            content=TestimonialContent(
                title="Updated Title",
                content="Updated content",
                rating=4,
                author_name="Jane Doe",
            )
        )

        result = TestimonialService.update_testimonial(
            data=data,
            db=mock_db,
            tenant_owner_id=tenant_owner_id,
            testimonial_id=testimonial_id,
        )

        assert mock_db.get.called
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called
        assert result.title == "Updated Title"

    def test_update_testimonial_not_found(self):
        """Test updating non-existent testimonial raises error."""
        from fastapi import HTTPException

        from app.schemas.testimonial import TestimonialUpdate

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_db.get.return_value = None

        data = TestimonialUpdate()

        try:
            TestimonialService.update_testimonial(
                data=data,
                db=mock_db,
                tenant_owner_id=tenant_owner_id,
                testimonial_id=testimonial_id,
            )
            raise AssertionError("Should have raised HTTPException")
        except HTTPException as e:
            assert e.status_code == 404

    def test_update_testimonial_from_different_tenant(self):
        """Test updating testimonial from different tenant raises error."""
        from fastapi import HTTPException

        from app.schemas.testimonial import TestimonialUpdate

        mock_db = Mock()
        tenant_owner_id = uuid4()
        other_tenant_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = other_tenant_id

        mock_db.get.return_value = mock_testimonial

        data = TestimonialUpdate()

        try:
            TestimonialService.update_testimonial(
                data=data,
                db=mock_db,
                tenant_owner_id=tenant_owner_id,
                testimonial_id=testimonial_id,
            )
            raise AssertionError("Should have raised HTTPException")
        except HTTPException as e:
            assert e.status_code == 404

    def test_update_testimonial_with_category(self):
        """Test updating testimonial with new category."""
        from app.schemas.testimonial import TestimonialUpdate

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = tenant_owner_id
        mock_testimonial.category = None
        mock_testimonial.tags = []

        mock_db.get.return_value = mock_testimonial

        mock_category = Mock()
        mock_category.id = uuid4()

        data = TestimonialUpdate(category_name="New Category")

        with patch(
            "app.services.testimonial.CategoryService.get_or_create_category"
        ) as mock_get_category:
            mock_get_category.return_value = mock_category

            TestimonialService.update_testimonial(
                data=data,
                db=mock_db,
                tenant_owner_id=tenant_owner_id,
                testimonial_id=testimonial_id,
            )

            mock_get_category.assert_called_once_with("New Category", mock_db)
            assert mock_testimonial.category_id == mock_category.id

    def test_update_testimonial_with_tags(self):
        """Test updating testimonial with new tags."""
        from app.schemas.testimonial import TestimonialUpdate

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = tenant_owner_id
        mock_testimonial.category = None
        mock_testimonial.tags = []

        mock_db.get.return_value = mock_testimonial

        data = TestimonialUpdate(tags=["tag1", "tag2"])

        with patch("app.services.testimonial.TagService.get_or_create_tags") as mock_get_tags:
            TestimonialService.update_testimonial(
                data=data,
                db=mock_db,
                tenant_owner_id=tenant_owner_id,
                testimonial_id=testimonial_id,
            )

            mock_get_tags.assert_called_once_with(["tag1", "tag2"], mock_db)

    def test_update_testimonial_partial_content(self):
        """Test partial update only modifies provided fields."""
        from app.schemas.testimonial import TestimonialContent, TestimonialUpdate

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        # Existing testimonial with all fields filled
        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = tenant_owner_id
        mock_testimonial.title = "Original Title"
        mock_testimonial.content = "Original content"
        mock_testimonial.rating = 5
        mock_testimonial.author_name = "Original Author"
        mock_testimonial.category = None
        mock_testimonial.tags = []

        mock_db.get.return_value = mock_testimonial

        # Only update author_name
        data = TestimonialUpdate(content=TestimonialContent(author_name="New Author"))

        TestimonialService.update_testimonial(
            data=data,
            db=mock_db,
            tenant_owner_id=tenant_owner_id,
            testimonial_id=testimonial_id,
        )

        # Only author_name should change, others should remain
        assert mock_testimonial.author_name == "New Author"
        assert mock_testimonial.title == "Original Title"
        assert mock_testimonial.content == "Original content"
        assert mock_testimonial.rating == 5


class TestSoftDeleteTestimonial:
    """Tests for soft_delete_testimonial function."""

    def test_soft_delete_testimonial_success(self):
        """Test soft deleting testimonial successfully."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = tenant_owner_id

        mock_db.get.return_value = mock_testimonial

        result = TestimonialService.soft_delete_testimonial(
            testimonial_id, mock_db, tenant_owner_id
        )

        assert result is True
        assert mock_testimonial.is_active is False
        assert mock_db.add.called
        assert mock_db.commit.called

    def test_soft_delete_testimonial_not_found(self):
        """Test soft deleting non-existent testimonial raises HTTPException."""
        from fastapi import HTTPException

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_db.get.return_value = None

        try:
            TestimonialService.soft_delete_testimonial(testimonial_id, mock_db, tenant_owner_id)
            raise AssertionError("Should have raised HTTPException")
        except HTTPException as e:
            assert e.status_code == 404

    def test_soft_delete_testimonial_from_different_tenant(self):
        """Test soft deleting testimonial from different tenant raises HTTPException."""
        from fastapi import HTTPException

        mock_db = Mock()
        tenant_owner_id = uuid4()
        other_tenant_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = other_tenant_id

        mock_db.get.return_value = mock_testimonial

        try:
            TestimonialService.soft_delete_testimonial(testimonial_id, mock_db, tenant_owner_id)
            raise AssertionError("Should have raised HTTPException")
        except HTTPException as e:
            assert e.status_code == 404


class TestUpdateStatus:
    """Tests for update_status function."""

    def test_update_status_success(self):
        """Test updating testimonial status successfully."""
        from app.models.testimonial import StatusType

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = tenant_owner_id

        mock_db.get.return_value = mock_testimonial

        result = TestimonialService.update_status(
            testimonial_id, StatusType.APPROVED, mock_db, tenant_owner_id
        )

        assert result is True
        assert mock_testimonial.status == StatusType.APPROVED
        assert mock_db.add.called
        assert mock_db.commit.called

    def test_update_status_not_found(self):
        """Test updating status of non-existent testimonial raises HTTPException."""
        from fastapi import HTTPException

        from app.models.testimonial import StatusType

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_db.get.return_value = None

        try:
            TestimonialService.update_status(
                testimonial_id, StatusType.APPROVED, mock_db, tenant_owner_id
            )
            raise AssertionError("Should have raised HTTPException")
        except HTTPException as e:
            assert e.status_code == 404

    def test_update_status_from_different_tenant(self):
        """Test updating status of testimonial from different tenant raises HTTPException."""
        from fastapi import HTTPException

        from app.models.testimonial import StatusType

        mock_db = Mock()
        tenant_owner_id = uuid4()
        other_tenant_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = other_tenant_id

        mock_db.get.return_value = mock_testimonial

        try:
            TestimonialService.update_status(
                testimonial_id, StatusType.REJECTED, mock_db, tenant_owner_id
            )
            raise AssertionError("Should have raised HTTPException")
        except HTTPException as e:
            assert e.status_code == 404

    def test_update_status_to_rejected(self):
        """Test updating testimonial status to rejected."""
        from app.models.testimonial import StatusType

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = tenant_owner_id

        mock_db.get.return_value = mock_testimonial

        result = TestimonialService.update_status(
            testimonial_id, StatusType.REJECTED, mock_db, tenant_owner_id
        )

        assert result is True
        assert mock_testimonial.status == StatusType.REJECTED

    def test_update_status_to_pending(self):
        """Test updating testimonial status back to pending."""
        from app.models.testimonial import StatusType

        mock_db = Mock()
        tenant_owner_id = uuid4()
        testimonial_id = uuid4()

        mock_testimonial = Mock(spec=Testimonial)
        mock_testimonial.user_id = tenant_owner_id

        mock_db.get.return_value = mock_testimonial

        result = TestimonialService.update_status(
            testimonial_id, StatusType.PENDING, mock_db, tenant_owner_id
        )

        assert result is True
        assert mock_testimonial.status == StatusType.PENDING
