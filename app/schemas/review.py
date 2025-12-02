from pydantic import BaseModel, Field
from typing import Optional


# -----------------------------------
#       Base schema -- shared 
# -----------------------------------

class ReviewBase(BaseModel):
    review_text: Optional[str] = None
    rating: int = Field(ge=1, le=5)



# -----------------------------------
#       For creating a Review 
# -----------------------------------

class ReviewCreate(ReviewBase):
    user_id: int                       # User leaving the review



# -----------------------------------
#      For returning review data 
# -----------------------------------

class ReviewOut(ReviewBase):
    id: int
    book_id: int
    user_id: int

    class Config:
        from_attributes = True