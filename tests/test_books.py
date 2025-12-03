import pytest

async def _register_and_login(client, email: str, password: str, role: str = "user") -> str:
    await client.post(
        "/auth/register",
        json={"email": email, "password": password, "role": role},
    )
    res = await client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert res.status_code == 200
    return res.json()["access_token"]

@pytest.mark.anyio
async def test_create_book_requires_auth(client):
    res = await client.post(
        "/books/",
        json={
            "title": "NoAuth",
            "author": "Nobody",
            "genre": "Fiction",
            "year_published": 2024,
        },
    )
    assert res.status_code == 401  # Not authenticated [web:75]

@pytest.mark.anyio
async def test_create_and_list_books(client):
    token = await _register_and_login(client, "owner1@example.com", "pass123")

    res = await client.post(
        "/books/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "My Book",
            "author": "Owner1",
            "genre": "Sci-Fi",
            "year_published": 2023,
        },
    )
    assert res.status_code == 201
    created = res.json()
    assert created["title"] == "My Book"
    assert created["owner_id"] == 1

    res2 = await client.get("/books/")
    assert res2.status_code == 200
    books = res2.json()
    assert len(books) == 1
    assert books[0]["title"] == "My Book"

@pytest.mark.anyio
async def test_user_cannot_edit_others_book(client):
    # owner creates a book
    owner_token = await _register_and_login(client, "owner2@example.com", "pass123")
    other_token = await _register_and_login(client, "other@example.com", "pass123")

    create_res = await client.post(
        "/books/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "title": "Owned Book",
            "author": "Owner2",
            "genre": "Drama",
            "year_published": 2022,
        },
    )
    assert create_res.status_code == 201
    book_id = create_res.json()["id"]

    # other user tries to update
    update_res = await client.put(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {other_token}"},
        json={"title": "Hacked Title"},
    )
    assert update_res.status_code == 403  # forbidden – ownership enforced [web:75]

@pytest.mark.anyio
async def test_admin_can_edit_others_book(client):
    owner_token = await _register_and_login(client, "owner3@example.com", "pass123")
    admin_token = await _register_and_login(client, "admin@example.com", "pass123", role="admin")

    create_res = await client.post(
        "/books/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "title": "Admin Editable",
            "author": "Owner3",
            "genre": "Tech",
            "year_published": 2025,
        },
    )
    book_id = create_res.json()["id"]

    # admin updates successfully
    update_res = await client.put(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"title": "Admin Edited"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Admin Edited"
