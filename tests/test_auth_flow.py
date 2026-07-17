from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_register_login_and_get_current_user():
    email = f"test-{uuid4()}@example.com"
    password = "StrongPass123!"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Test User",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"

    access_token = login_data["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert me_response.status_code == 200

    me_data = me_response.json()

    assert me_data["email"] == email
    assert me_data["full_name"] == "Test User"
    assert me_data["role"] == "user"
    assert me_data["is_active"] is True


def test_get_current_user_without_token_fails():
    response = client.get("/auth/me")

    assert response.status_code == 401