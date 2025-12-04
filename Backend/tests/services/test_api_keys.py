"""Tests for API Keys service."""

from unittest.mock import Mock
from uuid import uuid4

from app.services.api_keys import (
    create_api_key,
    generate_api_key_pair,
    list_api_keys,
    revoke_api_key,
    verify_api_key,
)


class TestGenerateAPIKeyPair:
    """Tests for generate_api_key_pair function."""

    def test_generate_api_key_pair_returns_tuple(self):
        """Test that generate_api_key_pair returns a tuple of 3 strings."""
        raw, prefix, digest = generate_api_key_pair()

        assert isinstance(raw, str)
        assert isinstance(prefix, str)
        assert isinstance(digest, str)
        assert len(raw) > 0
        assert len(prefix) > 0
        assert len(digest) > 0

    def test_generate_api_key_pair_unique_keys(self):
        """Test that consecutive calls generate different keys."""
        raw1, prefix1, digest1 = generate_api_key_pair()
        raw2, prefix2, digest2 = generate_api_key_pair()

        assert raw1 != raw2
        assert digest1 != digest2

    def test_generate_api_key_pair_custom_length(self):
        """Test that custom length affects the generated key."""
        raw1, _, _ = generate_api_key_pair(length=24)
        raw2, _, _ = generate_api_key_pair(length=48)

        # Different lengths should produce different size tokens
        assert len(raw1) != len(raw2)


class TestCreateAPIKey:
    """Tests for create_api_key function."""

    def test_create_api_key_success(self):
        """Test successful API key creation."""
        mock_db = Mock()
        name = "Test API Key"

        result = create_api_key(mock_db, name)

        assert result.name == name
        assert result.raw_key is not None
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called

    def test_create_api_key_without_name(self):
        """Test creating API key without a name."""
        mock_db = Mock()

        result = create_api_key(mock_db, None)

        assert result.name is None
        assert result.raw_key is not None
        assert mock_db.add.called


class TestRevokeAPIKey:
    """Tests for revoke_api_key function."""

    def test_revoke_api_key_success(self):
        """Test successful API key revocation."""
        mock_db = Mock()
        key_id = uuid4()
        mock_key = Mock()
        mock_key.revoked = False
        mock_db.get.return_value = mock_key

        result = revoke_api_key(mock_db, key_id)

        assert result is True
        assert mock_key.revoked is True
        assert mock_db.add.called
        assert mock_db.commit.called

    def test_revoke_api_key_not_found(self):
        """Test revoking a non-existent API key."""
        mock_db = Mock()
        mock_db.get.return_value = None
        key_id = uuid4()

        result = revoke_api_key(mock_db, key_id)

        assert result is False


class TestVerifyAPIKey:
    """Tests for verify_api_key function."""

    def test_verify_api_key_invalid_token_too_short(self):
        """Test verification with too short token."""
        mock_db = Mock()

        result = verify_api_key(mock_db, "short")

        assert result is None

    def test_verify_api_key_empty_token(self):
        """Test verification with empty token."""
        mock_db = Mock()

        result = verify_api_key(mock_db, "")

        assert result is None

    def test_verify_api_key_not_found(self):
        """Test verification when key is not found in database."""
        mock_db = Mock()
        mock_db.exec.return_value.first.return_value = None

        result = verify_api_key(mock_db, "testkey_" + "x" * 40)

        assert result is None


class TestListAPIKeys:
    """Tests for list_api_keys function."""

    def test_list_api_keys_returns_list(self):
        """Test that list_api_keys returns a list."""
        mock_db = Mock()
        mock_db.exec.return_value.all.return_value = []

        result = list_api_keys(mock_db)

        assert isinstance(result, list)
        assert mock_db.exec.called

    def test_list_api_keys_with_data(self):
        """Test listing API keys with data."""
        mock_db = Mock()
        mock_keys = [Mock(), Mock()]
        mock_db.exec.return_value.all.return_value = mock_keys

        result = list_api_keys(mock_db)

        assert len(result) == 2
