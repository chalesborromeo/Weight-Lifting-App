from typing import List
from pydantic import BaseModel

from app.schemas.sets import SetCreate, SetResponse

class ExerciseCreate(BaseModel):
    name: str
    sets: List[SetCreate]
    
class ExerciseResponse(BaseModel):
    id: int
    name: str
    sets: List[SetResponse]

    model_config = {"from_attributes": True}