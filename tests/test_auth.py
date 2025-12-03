import pytest

@pytest.mark.anyio
async def test_register_and_login(client):
    # Register user
    res = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "pass123", "role": "user"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"

    # Login
    res2 = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "pass123"},
    )
    assert res2.status_code == 200
    token_data = res2.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
