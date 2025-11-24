"""
Pytest configuration and fixtures.

This file contains shared fixtures and configuration for all tests.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Provide a TestClient for testing endpoints."""
    return TestClient(app)
