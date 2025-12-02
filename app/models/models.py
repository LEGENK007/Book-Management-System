from sqlalchemy import Column, Integer, String, Text, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.db.base import Base 


# ---------------------------------
#           USER MODEL
# ---------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")


# ---------------------------------
#           BOOK MODEL
# ---------------------------------

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=False)
    year_published = Column(Integer, nullable=False)
    summary = Column(Text, nullable=True)

    # Relationship to reviews
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")


# ---------------------------------
#          REVIEW MODEL
# ---------------------------------

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    review_text = Column(Text)
    rating = Column(SmallInteger, nullable=False)

    #Relationships
    book = relationship("Book", back_populates="reviews")
    user = relationship("User")