from pydantic import BaseModel, EmailStr
from typing import Optional


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None


class AuthResponse(BaseModel):
    message: str
    token: TokenResponse
