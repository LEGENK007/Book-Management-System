from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.models.models import Review
from app.schemas.review import ReviewCreate
from app.crud.books import get_book


# Add a review
async def create_review(session: AsyncSession, book_id: int, review_in: ReviewCreate) -> Review:
    new_review = Review(
        book_id = book_id,
        user_id = review_in.user_id,
        review_text = review_in.review_text,
        rating = review_in.rating,
    )
    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)
    return new_review


# Get all reviews of a book
async def get_reviews(session: AsyncSession, book_id: int) -> List[Review]:
    result = await session.execute(
        select(Review).where(Review.book_id == book_id)
    )
    return result.scalars().all()


# Get average rating summary
async def get_rating_stats(session: AsyncSession, book_id: int) -> Optional[dict]:
    book = await get_book(session, book_id)
    if not book:
        return None
    
    reviews = await get_reviews(session, book_id)
    if reviews:
        avg_rating = sum(r.rating for r in reviews)/len(reviews)
    else:
        avg_rating = 0.0
    
    return {
        "book": book,
        "average rating": round(avg_rating, 2),
        "review count": len(reviews),
    }
