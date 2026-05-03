from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.exercise import ExerciseCreate, ExerciseResponse

class WorkoutCreate(BaseModel):
    user_id: int
    name: str
    type: str
    duration: float
    is_public: bool = True
    exercises: List[ExerciseCreate]

class WorkoutResponse(BaseModel):
    id: int
    name: str
    type: str
    duration: float
    created_at: datetime
    is_public: bool = True
    exercises: List[ExerciseResponse]

    model_config = {"from_attributes": True}