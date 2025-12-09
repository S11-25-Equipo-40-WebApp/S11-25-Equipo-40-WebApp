"""Tests for CategoryService."""

from unittest.mock import Mock

from app.models.category import Category
from app.services.category import CategoryService


def test_get_or_create_category_returns_existing():
    mock_db = Mock()
    existing = Category(name="existing", slug="existing")

    # Simulate existing category found
    exec_result = Mock()
    exec_result.first.return_value = existing
    mock_db.exec.return_value = exec_result

    result = CategoryService.get_or_create_category("Existing", mock_db)

    assert result is existing
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()


def test_get_or_create_category_creates_new():
    mock_db = Mock()

    # No existing category
    exec_result = Mock()
    exec_result.first.return_value = None
    mock_db.exec.return_value = exec_result

    result = CategoryService.get_or_create_category("  New Category  ", mock_db)

    assert result.name == "new category"
    assert result.slug == "new-category"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(result)


def test_get_all_categories_returns_list():
    mock_db = Mock()
    c1 = Category(name="one", slug="one")
    c2 = Category(name="two", slug="two")

    exec_result = Mock()
    exec_result.all.return_value = [c1, c2]
    mock_db.exec.return_value = exec_result

    result = CategoryService.get_all_categories(mock_db)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] is c1
    assert result[1] is c2
