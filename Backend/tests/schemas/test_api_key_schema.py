from datetime import datetime
from uuid import UUID

from app.schemas import APIKeyCreate, APIKeyListResponse, APIKeyResponse


def test_apikeycreate_default_name():
    c = APIKeyCreate()
    assert c.name == "Secret Key"


def test_apikeyresponse_contains_raw_key():
    r = APIKeyResponse(name="MyKey", raw_key="tsy_abc123")
    assert r.raw_key.startswith("tsy_")
    assert r.name == "MyKey"


def test_apikeylistresponse_fields():
    # ensure schema has the expected fields and types
    list_response = APIKeyListResponse(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        name=None,
        prefix="tsy_abcd",
        revoked=False,
        created_at=datetime.now(),
    )
    assert list_response.prefix.startswith("tsy_")
    assert isinstance(list_response.revoked, bool)
