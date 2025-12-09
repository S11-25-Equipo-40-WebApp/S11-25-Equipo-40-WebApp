"""Tests for TagService."""

from unittest.mock import Mock

from app.models.tag import Tag
from app.services.tag import TagService


def test_get_or_create_tags_creates_and_returns_mixed():
    mock_db = Mock()

    # First tag does not exist -> create
    exec_result_1 = Mock()
    exec_result_1.first.return_value = None

    # Second tag exists
    existing = Tag(name="exist", slug="exist")
    exec_result_2 = Mock()
    exec_result_2.first.return_value = existing

    # Configure side_effect of db.exec so each call returns a different exec result
    mock_db.exec.side_effect = [exec_result_1, exec_result_2]

    names = ["NewTag", "Exist"]
    result = TagService.get_or_create_tags(names, mock_db)

    assert len(result) == 2
    # second should be the existing object
    assert result[1] is existing
    # first should be a Tag instance created
    assert isinstance(result[0], Tag)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called()


def test_get_all_tags_returns_list():
    mock_db = Mock()
    t1 = Tag(name="a", slug="a")
    t2 = Tag(name="b", slug="b")

    exec_result = Mock()
    exec_result.all.return_value = [t1, t2]
    mock_db.exec.return_value = exec_result

    result = TagService.get_all_tags(mock_db)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] is t1
    assert result[1] is t2
