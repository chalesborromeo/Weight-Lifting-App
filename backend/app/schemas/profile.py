from pydantic import BaseModel
from typing import Optional


class ProfileCreate(BaseModel):
    name: str
    age: Optional[int] = None
    gym: Optional[str] = None
    bio: Optional[str] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    goal: Optional[str] = None
    experience: Optional[str] = None
    days_per_week: Optional[int] = None


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gym: Optional[str] = None
    bio: Optional[str] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    goal: Optional[str] = None
    experience: Optional[str] = None
    days_per_week: Optional[int] = None


class ProfileResponse(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    gym: Optional[str] = None
    bio: Optional[str] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    goal: Optional[str] = None
    experience: Optional[str] = None
    days_per_week: Optional[int] = None

    model_config = {"from_attributes": True}
