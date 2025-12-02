from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.models.models import Book
from app.schemas.book import BookCreate, BookUpdate 



# Creating a book
async def create_book(session: AsyncSession, book_in: BookCreate) -> Book:
    new_book = Book(**book_in.dict())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book


# Get one book
async def get_book(session: AsyncSession, book_id: int) -> Optional[Book]:
    result = await session.execute(
        select(Book).where(Book.id == book_id)
    )
    return result.scalar_one_or_none()


# Get all books
async def get_books(session: AsyncSession) -> List[Book]:
    result = await session.execute(select(Book))
    return result.scalars().all()


# Update a book
async def update_book(session: AsyncSession, book_id: int, book_in: BookUpdate) -> Optional[Book]:
    book = await get_book(session, book_id)
    if not book:
        return None
    
    for field, value in book_in.dict(exclude_unset=True).items():
        setattr(book, field, value)
    
    await session.commit()
    await session.refresh(book)
    return book


# Delete a book
async def delete_book(session: AsyncSession, book_id: int) -> bool:
    book = await get_book(session, book_id)
    if not book:
        return False
    
    await session.delete(book)
    await session.commit()

    return True