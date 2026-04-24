from datetime import date
from typing import Optional
from pydantic import BaseModel


class ProfileCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None  # legacy
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    primary_sport: Optional[str] = None
    location: Optional[str] = None  # city
    state: Optional[str] = None
    gym: Optional[str] = None  # legacy
    birthdate: Optional[date] = None
    age: Optional[int] = None  # legacy
    gender: Optional[str] = None
    weight: Optional[float] = None
    goal_weight: Optional[float] = None
    gym_id: Optional[int] = None


class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    primary_sport: Optional[str] = None
    location: Optional[str] = None
    state: Optional[str] = None
    gym: Optional[str] = None
    birthdate: Optional[date] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    goal_weight: Optional[float] = None
    gym_id: Optional[int] = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    primary_sport: Optional[str] = None
    location: Optional[str] = None
    state: Optional[str] = None
    gym: Optional[str] = None
    birthdate: Optional[date] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    goal_weight: Optional[float] = None
    gym_id: Optional[int] = None

    model_config = {"from_attributes": True}
