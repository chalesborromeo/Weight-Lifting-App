from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class GymCreate(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: float
    longitude: float
    hours_open: Optional[str] = None
    hours_close: Optional[str] = None
    rating: Optional[float] = None


class GymResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    latitude: float
    longitude: float
    hours_open: Optional[str] = None
    hours_close: Optional[str] = None
    rating: Optional[float] = None

    model_config = {"from_attributes": True}


class NearbyGymResponse(GymResponse):
    distance_km: float


class GymCheckInCreate(BaseModel):
    gym_name: str
    gym_address: Optional[str] = None


class GymCheckInResponse(BaseModel):
    id: int
    gym_name: str
    gym_address: Optional[str] = None
    checked_in_at: datetime

    model_config = {"from_attributes": True}
