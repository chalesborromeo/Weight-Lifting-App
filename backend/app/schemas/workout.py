from pydantic import BaseModel
from typing import List
from app.schemas.exercise import ExerciseCreate, ExerciseResponse

class WorkoutCreate(BaseModel):
    user_id: int
    name: str
    type: str
    duration: float
    exercises: List[ExerciseCreate]

class WorkoutResponse(BaseModel):
    id: int
    name: str
    type: str
    duration: float
    exercises: List[ExerciseResponse]

    model_config = {"from_attributes": True}