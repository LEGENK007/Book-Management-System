import pytest

async def _register_and_login(client, email: str) -> str:
    await client.post(
        "/auth/register",
        json={"email": email, "password": "pass123", "role": "user"},
    )
    res = await client.post(
        "/auth/login",
        json={"email": email, "password": "pass123"},
    )
    return res.json()["access_token"]

@pytest.mark.anyio
async def test_add_and_list_reviews(client):
    # create owner and book
    owner_token = await _register_and_login(client, "reviewowner@example.com")
    create_res = await client.post(
        "/books/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "title": "Reviewable Book",
            "author": "Author",
            "genre": "Fiction",
            "year_published": 2024,
        },
    )
    assert create_res.status_code == 201
    book_id = create_res.json()["id"]

    # reviewer user
    reviewer_token = await _register_and_login(client, "reviewer@example.com")

    # add review
    add_res = await client.post(
        f"/books/{book_id}/reviews",
        headers={"Authorization": f"Bearer {reviewer_token}"},
        json={"review_text": "Great book!", "rating": 5},
    )
    assert add_res.status_code == 201
    review = add_res.json()
    assert review["rating"] == 5
    assert review["book_id"] == book_id

    # list reviews
    list_res = await client.get(f"/books/{book_id}/reviews")
    assert list_res.status_code == 200
    reviews = list_res.json()
    assert len(reviews) == 1
    assert reviews[0]["review_text"] == "Great book!"
