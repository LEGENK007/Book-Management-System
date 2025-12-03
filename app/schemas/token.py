from pydantic import BaseModel


class Token(BaseModel):
    access_token: str 
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int | None = None       # User ID
    role: str | None = None      # For RBAC (admin/user)