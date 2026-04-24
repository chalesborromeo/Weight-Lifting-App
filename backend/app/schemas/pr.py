from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import UserResponse


class PRCreate(BaseModel):
    exercise_name: str
    weight: float
    reps: int


class PRResponse(BaseModel):
    id: int
    exercise_name: str
    weight: float
    reps: int
    date: datetime
    user_id: int
    user: UserResponse

    model_config = {"from_attributes": True}
