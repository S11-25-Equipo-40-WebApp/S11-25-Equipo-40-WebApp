from fastapi import status


def test_root(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to Testify Backend!"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND)
