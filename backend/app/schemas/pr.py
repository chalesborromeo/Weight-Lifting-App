from datetime import datetime
from pydantic import BaseModel


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

    model_config = {"from_attributes": True}
