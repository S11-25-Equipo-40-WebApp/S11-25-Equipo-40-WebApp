"""Tests for Auth service."""

from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate
from app.services.auth import AuthService


class TestRegisterUser:
    """Tests for register_user method."""

    def test_register_user_success(self):
        """Test successful user registration."""
        mock_db = Mock()
        mock_db.exec.return_value.one_or_none.return_value = None

        data = UserCreate(email="test@example.com", password="Password123!")

        with patch("app.services.auth.hash_password", return_value="hashed"):
            AuthService.register_user(mock_db, data)

        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called

    def test_register_user_duplicate_email(self):
        """Test registration with existing email."""
        mock_db = Mock()
        existing_user = Mock()
        mock_db.exec.return_value.one_or_none.return_value = existing_user

        data = UserCreate(email="existing@example.com", password="Password123!")

        with pytest.raises(HTTPException) as exc_info:
            AuthService.register_user(mock_db, data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already exists" in str(exc_info.value.detail)


class TestLoginUser:
    """Tests for login_user method."""

    def test_login_user_success(self):
        """Test successful user login."""
        mock_db = Mock()
        mock_user = Mock()
        mock_user.id = "123"
        mock_user.role = "user"
        mock_user.hashed_password = "hashed_password"
        mock_db.exec.return_value.one_or_none.return_value = mock_user

        form_data = OAuth2PasswordRequestForm(
            username="test@example.com", password="password123", scope=""
        )

        with (
            patch("app.services.auth.verify_password", return_value=True),
            patch("app.services.auth.create_access_token", return_value="access_token"),
            patch("app.services.auth.create_refresh_token", return_value="refresh_token"),
        ):
            result = AuthService.login_user(mock_db, form_data)

        assert result["access_token"] == "access_token"
        assert result["refresh_token"] == "refresh_token"
        assert result["token_type"] == "bearer"

    def test_login_user_not_found(self):
        """Test login with non-existent user."""
        mock_db = Mock()
        mock_db.exec.return_value.one_or_none.return_value = None

        form_data = OAuth2PasswordRequestForm(
            username="nonexistent@example.com", password="password123", scope=""
        )

        with pytest.raises(HTTPException) as exc_info:
            AuthService.login_user(mock_db, form_data)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in str(exc_info.value.detail)

    def test_login_user_wrong_password(self):
        """Test login with wrong password."""
        mock_db = Mock()
        mock_user = Mock()
        mock_user.hashed_password = "hashed_password"
        mock_db.exec.return_value.one_or_none.return_value = mock_user

        form_data = OAuth2PasswordRequestForm(
            username="test@example.com", password="wrong_password", scope=""
        )

        with patch("app.services.auth.verify_password", return_value=False):
            with pytest.raises(HTTPException) as exc_info:
                AuthService.login_user(mock_db, form_data)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestCreateNewAccessToken:
    """Tests for create_new_access_token method."""

    def test_create_new_access_token_success(self):
        """Test successful access token creation."""
        mock_user = Mock()
        mock_user.id = "123"
        mock_user.role = "user"

        with (
            patch("app.services.auth.create_access_token", return_value="new_access_token"),
            patch("app.services.auth.create_refresh_token", return_value="new_refresh_token"),
        ):
            result = AuthService.create_new_access_token(mock_user)

        assert result["access_token"] == "new_access_token"
        assert result["refresh_token"] == "new_refresh_token"
        assert result["token_type"] == "bearer"

    def test_create_new_access_token_returns_dict(self):
        """Test that create_new_access_token returns a dictionary."""
        mock_user = Mock()
        mock_user.id = "456"
        mock_user.role = "admin"

        with (
            patch("app.services.auth.create_access_token"),
            patch("app.services.auth.create_refresh_token"),
        ):
            result = AuthService.create_new_access_token(mock_user)

        assert isinstance(result, dict)
        assert "access_token" in result
        assert "refresh_token" in result
        assert "token_type" in result
