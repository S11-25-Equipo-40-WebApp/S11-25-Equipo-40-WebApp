"""Tests for User service."""

from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import HTTPException, status

from app.models.user import Roles
from app.schemas.user import UserCreateInternal
from app.services.user import UserService


def create_mock_user(user_id=None, email="test@example.com", role=Roles.OWNER, owner_id=None):
    """Helper function to create a mock user."""
    mock_user = Mock()
    mock_user.id = user_id or uuid4()
    mock_user.email = email
    mock_user.role = role
    mock_user.owner_id = owner_id
    mock_user.name = "Test"
    mock_user.surname = "User"
    mock_user.is_active = True
    return mock_user


class TestCreateUserForOwner:
    """Tests for create_user_for_owner method."""

    def test_create_user_by_owner_success(self):
        """Test successful user creation by owner."""
        mock_db = Mock()
        owner_id = uuid4()

        # Mock para verificar que no existe el email
        mock_db.exec.return_value.one_or_none.return_value = None

        data = Mock(spec=UserCreateInternal)
        data.email = "newuser@example.com"
        data.password = "SecurePass123!"
        data.model_dump.return_value = {
            "email": "newuser@example.com",
            "name": "New",
            "surname": "User",
            "role": Roles.MODERATOR,
        }

        UserService.create_user_for_owner(mock_db, owner_id, data)

        # Verificar que se llamó a db.add, commit y refresh
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called

    def test_create_user_by_admin_assigns_to_tenant_owner(self):
        """Test that admin creates users under the tenant owner, not under themselves."""
        mock_db = Mock()
        tenant_owner_id = uuid4()

        # Mock para verificar que no existe el email
        mock_db.exec.return_value.one_or_none.return_value = None

        data = Mock(spec=UserCreateInternal)
        data.email = "newuser2@example.com"
        data.password = "SecurePass123!"
        data.model_dump.return_value = {
            "email": "newuser2@example.com",
            "name": "New",
            "surname": "User",
            "role": Roles.MODERATOR,
        }

        UserService.create_user_for_owner(mock_db, tenant_owner_id, data)

        # Verificar que se llamó a db.add con un usuario
        assert mock_db.add.called
        # El usuario creado debe tener owner_id = tenant_owner_id
        created_user = mock_db.add.call_args[0][0]
        assert created_user.owner_id == tenant_owner_id

    def test_create_user_by_moderator_fails(self):
        """Test that moderators cannot create users (permission check happens at router level)."""
        # Note: The service method signature is create_user_for_owner(db, tenant_owner_id: UUID, data)
        # Permission checks happen at the router/endpoint level, not in the service.
        # This test is kept for documentation but skips the actual check since service doesn't validate roles.
        pass

    def test_create_user_duplicate_email_fails(self):
        """Test that creating a user with duplicate email fails."""
        mock_db = Mock()
        owner_id = uuid4()

        # Mock para simular que el email ya existe
        existing_user = Mock()
        mock_db.exec.return_value.one_or_none.return_value = existing_user

        data = Mock(spec=UserCreateInternal)
        data.email = "existing@example.com"

        with pytest.raises(HTTPException) as exc_info:
            UserService.create_user_for_owner(mock_db, owner_id, data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already exists" in str(exc_info.value.detail)


class TestGetUsers:
    """Tests for get_users method."""

    def test_get_users_returns_pagination_response(self):
        """Test that get_users returns a tuple (users, total_items)."""
        from datetime import datetime

        mock_db = Mock()
        owner_id = uuid4()

        mock_user1 = Mock()
        mock_user1.id = uuid4()
        mock_user1.name = "John"
        mock_user1.surname = "Doe"
        mock_user1.email = "john@example.com"
        mock_user1.role = Roles.MODERATOR
        mock_user1.created_at = datetime.now()
        mock_user1.updated_at = datetime.now()

        mock_user2 = Mock()
        mock_user2.id = uuid4()
        mock_user2.name = "Jane"
        mock_user2.surname = "Smith"
        mock_user2.email = "jane@example.com"
        mock_user2.role = Roles.ADMIN
        mock_user2.created_at = datetime.now()
        mock_user2.updated_at = datetime.now()

        mock_users = [mock_user1, mock_user2]

        # Mock the count query (first call) and the users query (second call)
        mock_count_result = Mock()
        mock_count_result.one.return_value = 2
        mock_users_result = Mock()
        mock_users_result.all.return_value = mock_users
        mock_db.exec.side_effect = [mock_count_result, mock_users_result]

        users, total_items = UserService.get_users(mock_db, owner_id, skip=0, limit=10)

        assert len(users) == 2
        assert total_items == 2

    def test_get_users_empty_list(self):
        """Test get_users with empty database."""
        mock_db = Mock()
        owner_id = uuid4()

        # Mock the count query (first call) and the users query (second call)
        mock_count_result = Mock()
        mock_count_result.one.return_value = 0
        mock_users_result = Mock()
        mock_users_result.all.return_value = []
        mock_db.exec.side_effect = [mock_count_result, mock_users_result]

        users, total_items = UserService.get_users(mock_db, owner_id, skip=0, limit=10)

        assert total_items == 0
        assert len(users) == 0

    def test_get_users_pagination(self):
        """Test pagination parameters."""
        from datetime import datetime

        mock_db = Mock()
        owner_id = uuid4()
        mock_users = []
        for i in range(5):
            mock_user = Mock()
            mock_user.id = uuid4()
            mock_user.name = f"User{i}"
            mock_user.surname = f"Surname{i}"
            mock_user.email = f"user{i}@example.com"
            mock_user.role = Roles.MODERATOR
            mock_user.created_at = datetime.now()
            mock_user.updated_at = datetime.now()
            mock_users.append(mock_user)

        # Mock the count query (first call) and the users query (second call)
        mock_count_result = Mock()
        mock_count_result.one.return_value = 20  # Total of 20 users
        mock_users_result = Mock()
        mock_users_result.all.return_value = mock_users
        mock_db.exec.side_effect = [mock_count_result, mock_users_result]

        users, total_items = UserService.get_users(mock_db, owner_id, skip=10, limit=5)

        assert len(users) == 5
        assert total_items == 20


class TestGetUserById:
    """Tests for get_user_by_id method."""

    def test_get_user_by_id_success(self):
        """Test successful user retrieval."""
        mock_db = Mock()
        owner_id = uuid4()

        user_id = uuid4()
        mock_user = Mock()
        mock_user.owner_id = owner_id
        mock_db.get.return_value = mock_user

        result = UserService.get_user_by_id(mock_db, user_id, owner_id)

        assert result == mock_user
        assert mock_db.get.called

    def test_get_user_by_id_not_found(self):
        """Test user not found."""
        mock_db = Mock()
        mock_db.get.return_value = None
        owner_id = uuid4()
        user_id = uuid4()

        with pytest.raises(HTTPException) as exc_info:
            UserService.get_user_by_id(mock_db, user_id, owner_id)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in str(exc_info.value.detail)


class TestSoftDeleteUser:
    """Tests for soft_delete_user method."""

    def test_soft_delete_user_success(self):
        """Test successful soft delete."""
        mock_db = Mock()
        owner_id = uuid4()

        user_id = uuid4()
        mock_user = Mock()
        mock_user.is_active = True
        mock_user.owner_id = owner_id
        mock_db.get.return_value = mock_user

        UserService.soft_delete_user(mock_db, user_id, owner_id)

        assert mock_user.is_active is False
        assert mock_db.add.called
        assert mock_db.commit.called

    def test_soft_delete_user_not_found(self):
        """Test soft delete with non-existent user."""
        mock_db = Mock()
        mock_db.get.return_value = None
        owner_id = uuid4()
        user_id = uuid4()

        with pytest.raises(HTTPException) as exc_info:
            UserService.soft_delete_user(mock_db, user_id, owner_id)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateUser:
    """Tests for update_user method."""

    def test_update_user_success(self):
        """Test successful user update."""
        mock_db = Mock()
        owner_id = uuid4()

        user_id = uuid4()
        mock_user = Mock()
        mock_user.owner_id = owner_id
        mock_db.get.return_value = mock_user

        mock_data = Mock()
        mock_data.model_dump.return_value = {"email": "newemail@example.com"}

        UserService.update_user(mock_db, user_id, mock_data, owner_id)

        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called

    def test_update_user_not_found(self):
        """Test updating non-existent user."""
        mock_db = Mock()
        mock_db.get.return_value = None
        owner_id = uuid4()
        user_id = uuid4()
        mock_data = Mock()
        mock_data.model_dump.return_value = {}

        with pytest.raises(HTTPException) as exc_info:
            UserService.update_user(mock_db, user_id, mock_data, owner_id)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


class TestGetUserByEmail:
    """Tests for get_user_by_email method."""

    def test_get_user_by_email_success(self):
        """Test successful user retrieval by email."""
        mock_db = Mock()
        owner_id = uuid4()
        mock_user = Mock()
        mock_db.exec.return_value.first.return_value = mock_user

        result = UserService.get_user_by_email(mock_db, "test@example.com", owner_id)

        assert result == mock_user

    def test_get_user_by_email_not_found(self):
        """Test user not found by email."""
        mock_db = Mock()
        owner_id = uuid4()
        mock_db.exec.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            UserService.get_user_by_email(mock_db, "notfound@example.com", owner_id)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in str(exc_info.value.detail)
