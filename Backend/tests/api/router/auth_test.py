def test_register_success(client):
    data = {"email": "test@example.com", "name": "Test", "surname": "User", "password": "12345678"}

    response = client.post("/auth/register", json=data)

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "test@example.com"
    assert body["name"] == "Test"
    assert "id" in body
    assert "roles" in body


def test_register_duplicate_email(client):
    first = {
        "email": "duplicate@example.com",
        "name": "First",
        "surname": "User",
        "password": "123456",
    }
    client.post("/auth/register", json=first)

    second = {
        "email": "duplicate@example.com",
        "name": "Second",
        "surname": "User",
        "password": "abc123",
    }
    response = client.post("/auth/register", json=second)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "email": "login@test.com",
            "name": "John",
            "surname": "Doe",
            "password": "mypassword",
        },
    )

    response = client.post(
        "/auth/login", json={"email": "login@test.com", "password": "mypassword"}
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "wrongpass@test.com",
            "name": "John",
            "surname": "Doe",
            "password": "correctpass",
        },
    )

    response = client.post(
        "/auth/login", json={"email": "wrongpass@test.com", "password": "incorrect"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_user_not_found(client):
    response = client.post(
        "/auth/login", json={"email": "notfound@example.com", "password": "anything"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
