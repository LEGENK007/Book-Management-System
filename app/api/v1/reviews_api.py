from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.db.crud.reviews import get_reviews, create_review
from app.db.crud.books import get_book as _get_book
from app.schemas.review import ReviewCreate, ReviewOut


router = APIRouter(prefix="/books", tags=["reviews"])

def _placeholder_auth_user():
    pass

@router.post("/books/{book_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def add_review_for_book(
    book_id: int,
    payload: ReviewCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(_placeholder_auth_user)
):
    book = await _get_book(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    review = create_review(session, book_id, payload)
    return review


@router.get("/books/{book_id}/reviews", response_model=List[ReviewOut])
async def fetch_reviews(book_id: int, session: AsyncSession = Depends(get_session)):
    reviews = await get_reviews(session, book_id)
    return reviews


