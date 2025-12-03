from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.db.crud.books import create_book, get_book, get_books, update_book, delete_book
from app.db.crud.reviews import get_rating_stats
from app.schemas.book import BookCreate, BookUpdate, BookOut
from app.core.permissions import require_admin


router = APIRouter(tags=["books"])

@router.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def add_book(
    payload: BookCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(require_admin)
):
    # Only admin can create books
    book = await create_book(session, payload)
    return book

@router.get("/books", response_model=List[BookOut])
async def list_books(session: AsyncSession = Depends(get_session)):
    books = await get_books(session)
    return books


@router.get("/books/{book_id}", response_model=BookOut)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await get_book(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{book_id}", response_model=BookOut)
async def update_book_by_id(
    book_id: int,
    payload: BookUpdate, 
    session: AsyncSession = Depends(get_session),
    current_user = Depends(require_admin)
):
    # Only Admin can update books
    updated = await update_book(session, book_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@router.delete("/books/{book_id}", status_code=HTTP_204_NO_CONTENT)
async def book_delete(
    book_id: int, 
    session: AsyncSession = Depends(get_session), 
    current_user = Depends(require_admin)
):
    # Only admin can delete books
    ok = await delete_book(session, book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return None


@router.get("/books/{book_id}/summary")
async def get_book_summary(book_id: int, session: AsyncSession = Depends(get_session)):
    # Aggregated rating
    stats = await get_rating_stats(session, book_id)

    # Load book summary
    book = await get_book(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {
        "title": book.title,
        "summary": book.summary, 
        "rating": stats["average rating"], 
        "review_count": stats["review count"], 
    }