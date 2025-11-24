"""
Pytest configuration and fixtures.

This file contains shared fixtures and configuration for all tests.
"""

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to Testify Backend!"}
