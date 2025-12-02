from pydantic import BaseModel
from typing import Optional


# -----------------------------------
#       Base schema -- shared 
# -----------------------------------

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int 


# -----------------------------------
#       For creating a book 
# -----------------------------------

class BookCreate(BookBase):
    summary: Optional[str] = None     # Optional since can be generated using Llama


# -----------------------------------
#       For updating a book 
# -----------------------------------

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None


# -----------------------------------
#      For returning book data 
# -----------------------------------

class BookOut(BookBase):
    id: int
    summary: Optional[str] = None

    class Config:
        from_attributes = True