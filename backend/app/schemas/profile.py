from pydantic import BaseModel
from typing import Optional


class ProfileCreate(BaseModel):
    name: str
    age: Optional[int] = None
    gym: Optional[str] = None
    bio: Optional[str] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    gym_id: Optional[int] = None


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gym: Optional[str] = None
    bio: Optional[str] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    gym_id: Optional[int] = None


class ProfileResponse(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    gym: Optional[str] = None
    bio: Optional[str] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    gym_id: Optional[int] = None
    user_id: int

    model_config = {"from_attributes": True}
