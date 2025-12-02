from pydantic import BaseModel, EmailStr
from typing import Literal


# -----------------------------------
#       Base schema -- shared 
# -----------------------------------

class UserBase(BaseModel):
    email: EmailStr


# -----------------------------------
#       For creating a user 
# -----------------------------------

class UserCreate(UserBase):
    password: str
    role: Literal["user", "admin"] = "user"


# -----------------------------------
#      For returning user info 
# -----------------------------------

class UserOut(UserBase):
    id: int
    role: Literal["user", "admin"]

    class Config:
        from_attributes = True