from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BodyMetricCreate(BaseModel):
    weight: float
    height: Optional[float] = None
    body_fat_pct: Optional[float] = None


class BodyMetricResponse(BaseModel):
    id: int
    weight: float
    height: Optional[float] = None
    body_fat_pct: Optional[float] = None
    date: datetime
    user_id: int

    model_config = {"from_attributes": True}
