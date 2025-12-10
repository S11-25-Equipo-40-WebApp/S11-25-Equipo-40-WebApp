"""Tests for API Keys service."""

from unittest.mock import Mock
from uuid import uuid4

from app.services.api_keys import APIKeyService


class TestGenerateAPIKeyPair:
    """Tests for generate_api_key_pair function."""

    def test_generate_api_key_pair_returns_tuple(self):
        """Test that generate_api_key_pair returns a tuple of 3 strings."""
        raw, prefix, digest = APIKeyService.generate_api_key_pair()

        assert isinstance(raw, str)
        assert isinstance(prefix, str)
        assert isinstance(digest, str)
        assert len(raw) > 0
        assert len(prefix) > 0
        assert len(digest) > 0

    def test_generate_api_key_pair_unique_keys(self):
        """Test that consecutive calls generate different keys."""
        raw1, prefix1, digest1 = APIKeyService.generate_api_key_pair()
        raw2, prefix2, digest2 = APIKeyService.generate_api_key_pair()

        assert raw1 != raw2
        assert digest1 != digest2

    def test_generate_api_key_pair_custom_length(self):
        """Test that custom length affects the generated key."""
        raw1, _, _ = APIKeyService.generate_api_key_pair(length=24)
        raw2, _, _ = APIKeyService.generate_api_key_pair(length=48)

        # Different lengths should produce different size tokens
        assert len(raw1) != len(raw2)


class TestCreateAPIKey:
    """Tests for create_api_key function."""

    def test_create_api_key_success(self):
        """Test successful API key creation."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        name = "Test API Key"

        result = APIKeyService.create_api_key(mock_db, tenant_owner_id, name)

        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called
        assert isinstance(result, dict)
        assert result["name"] == name
        assert "raw_key" in result
        assert isinstance(result["raw_key"], str)
        assert len(result["raw_key"]) > 0

    def test_create_api_key_without_name(self):
        """Test creating API key without a name."""
        mock_db = Mock()
        tenant_owner_id = uuid4()

        result = APIKeyService.create_api_key(mock_db, tenant_owner_id, None)

        assert mock_db.add.called
        assert isinstance(result, dict)
        assert result["name"] is None
        assert "raw_key" in result


class TestRevokeAPIKey:
    """Tests for revoke_api_key function."""

    def test_revoke_api_key_success(self):
        """Test successful API key revocation."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        key_id = uuid4()
        mock_key = Mock()
        mock_key.revoked = False
        mock_key.user_id = tenant_owner_id
        mock_db.get.return_value = mock_key

        result = APIKeyService.revoke_api_key(mock_db, key_id, tenant_owner_id)

        assert result is True
        assert mock_key.revoked is True
        assert mock_db.add.called
        assert mock_db.commit.called

    def test_revoke_api_key_not_found(self):
        """Test revoking a non-existent API key."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_db.get.return_value = None
        key_id = uuid4()

        result = APIKeyService.revoke_api_key(mock_db, key_id, tenant_owner_id)

        assert result is False

    def test_revoke_api_key_from_different_tenant(self):
        """Test that a user cannot revoke API key from another tenant."""
        mock_db = Mock()
        tenant_owner_id = uuid4()  # Tenant A
        key_id = uuid4()
        mock_key = Mock()
        mock_key.revoked = False
        mock_key.user_id = uuid4()  # Tenant B (different owner)
        mock_db.get.return_value = mock_key

        result = APIKeyService.revoke_api_key(mock_db, key_id, tenant_owner_id)

        assert result is False
        assert mock_key.revoked is False  # Should not be revoked
        assert not mock_db.add.called  # Should not save


class TestVerifyAPIKey:
    """Tests for verify_api_key function."""

    def test_verify_api_key_invalid_token_too_short(self):
        """Test verification with too short token."""
        mock_db = Mock()

        result = APIKeyService.verify_api_key(mock_db, "short")

        assert result is None

    def test_verify_api_key_empty_token(self):
        """Test verification with empty token."""
        mock_db = Mock()

        result = APIKeyService.verify_api_key(mock_db, "")

        assert result is None

    def test_verify_api_key_not_found(self):
        """Test verification when key is not found in database."""
        mock_db = Mock()
        mock_db.exec.return_value.first.return_value = None

        result = APIKeyService.verify_api_key(mock_db, "testkey_" + "x" * 40)

        assert result is None


class TestListAPIKeys:
    """Tests for list_api_keys function."""

    def test_list_api_keys_returns_list(self):
        """Test that list_api_keys returns a list."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_db.exec.return_value.all.return_value = []

        result = APIKeyService.list_api_keys(mock_db, tenant_owner_id)

        assert isinstance(result, list)
        assert mock_db.exec.called

    def test_list_api_keys_with_data(self):
        """Test listing API keys with data."""
        mock_db = Mock()
        tenant_owner_id = uuid4()
        mock_keys = [Mock(), Mock()]
        mock_db.exec.return_value.all.return_value = mock_keys

        result = APIKeyService.list_api_keys(mock_db, tenant_owner_id)

        assert len(result) == 2
